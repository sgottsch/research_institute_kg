import logging
import pickle
from pathlib import Path
from typing import Set, Tuple, List
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup
from scholarly import scholarly

import kgcreation.extractors.dblp as dblp
from config import google_scholar_institute_id, google_scholar_additional_person_ids, \
    google_scholar_person_ids_to_be_removed, research_interest_matches
from kgcreation.extractors.conference_index import conference_index
from kgcreation.extractors.journal_index import journal_index
from kgcreation.extractors.paper_index import paper_index
from kgcreation.extractors.person_index import person_index, Identifier
from kgcreation.models.person import Person

scholar_files = "kgcreation/data/input/scholar/"
scholar_output_files = Path("kgcreation/data/output/scholar/")
scholar_output_files.mkdir(parents=True, exist_ok=True)

logging.basicConfig()
_logger = logging.getLogger(__name__)
_logger.setLevel(logging.DEBUG)


def get_all_people_from_scholar(institute_id: str) -> Set[str]:
    ids = set()

    scholar_institue_url = (
            "https://scholar.google.com/citations?view_op=view_org&hl=de&org="
            + institute_id
    )
    ids, after_author, astart = extract_authors_from_html_page(
        scholar_institue_url, ids
    )

    while after_author:
        ids, after_author, astart = extract_authors_from_html_page(
            scholar_institue_url
            + "&after_author="
            + after_author
            + "&astart="
            + astart,
            ids,
        )

    # from Google forms
    ids |= google_scholar_additional_person_ids
    for id_to_remove in google_scholar_person_ids_to_be_removed:
        ids.remove(id_to_remove)  # TODO: Automatically fix error with persons without citations instead

    _logger.info(f"Scholar IDs: {len(ids)}")

    return ids


def get_author_from_scholar(scholar_id: str) -> Person:
    _logger.info(scholar_id)

    scholar_file = (scholar_output_files / scholar_id).with_suffix(".pickle")

    if scholar_file.exists():
        _logger.debug("load from pickle")
        with open(scholar_file, "rb") as handle:
            author = pickle.load(handle)
    else:
        _logger.debug("load from scholarly")
        author = scholarly.search_author_id(scholar_id)
        scholarly.fill(author, sections=["publications"])  # , 'coauthors'])
        with open(scholar_file, "wb") as handle:
            pickle.dump(author, handle, protocol=pickle.HIGHEST_PROTOCOL)

    person = person_index.get_person_by_id_or_name(
        Identifier.SCHOLAR, scholar_id, author["name"]
    )

    person.interests = set(
        [
            research_interest_matches.get(interest.strip(), interest.strip())
            for interest in author["interests"]
        ]
    )

    for publication in author.get("publications", []):
        paper = paper_index.get_paper_by_title(publication["bib"]["title"])
        paper_info = dblp.search(publication["bib"]["title"])

        if 'citation' in publication['bib']:
            paper.citation = publication['bib']['citation']

        if paper_info:
            _logger.info(paper_info)
            if paper_info.is_conference():
                conference = conference_index.get_conference_by_name(
                    paper_info.venue
                )
                paper.conference = conference
            if paper_info.is_journal():
                journal = journal_index.get_journal_by_name(paper_info.venue)
                paper.journal = journal
        else:
            _logger.warning(f'No paper info found for {publication["bib"]["title"]}')
            # FIXME: add some fallback here
        person.papers.append(paper)
        paper.authors.append(person)

    return person


def extract_authors_from_html_page(url: str, ids: Set[str]) -> Tuple[Set[str], str, str]:
    req = Request(url)
    html_page = urlopen(req).read()
    soup = BeautifulSoup(html_page, "html.parser")

    for a in soup.find_all("a", href=True):
        # print(a)
        id = a.attrs["href"]
        id = id.replace("view-source:", "")

        if id.startswith("/citations?hl=de&user="):
            id = id.replace("/citations?hl=de&user=", "")
            ids.add(id)

    after_author, astart = None, None
    for button in soup.find_all("button", onclick=True):
        button_link = (
            button.attrs["onclick"].replace("\\x3d", "=").replace("\\x26", "&")
        )
        if "after_author" in button_link:
            button_id = button_link.split("after_author=")[1]
            after_author = button_id.split("&")[0]
            astart = button_id.split("&")[1].replace("astart=", "").replace("'", "")

    return ids, after_author, astart


def get_all_persons_from_scholar() -> List[Person]:
    persons = []

    ids = get_all_people_from_scholar(google_scholar_institute_id)
    for id in ids:
        persons.append(get_author_from_scholar(id))
    return persons


if __name__ == "__main__":
    persons = get_all_persons_from_scholar()
    for person in persons:
        print(person.name)

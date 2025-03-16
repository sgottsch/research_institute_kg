import dataclasses
import hashlib
import json
import time
from pathlib import Path
from typing import Optional, Dict, List
from urllib.parse import urlencode

import requests

from config import dblp_cache_directory

CACHE_DIR = Path(dblp_cache_directory)
CACHE_DIR.mkdir(parents=True, exist_ok=True)
DBLP_PUBL_SEARCH_API = "https://dblp.org/search/publ/api"

session = requests.session()

publication_types = [
    "Conference and Workshop Papers",
    "Journal Articles",
]


@dataclasses.dataclass
class DBLPPublication:
    title: str
    year: str
    venue: str
    doi: str
    url: str
    type: str
    volume: str
    key: str
    authors: List[str] = dataclasses.field(default_factory=list)

    def __str__(self):
        return f"<Publication>: {self.title} ({self.year}), {self.venue}"

    def is_conference(self):
        return self.type == publication_types[0]

    def is_journal(self):
        return self.type == publication_types[1]


def hash_title(title: str):
    return hashlib.sha1(title.encode()).hexdigest()


def load_from_cache(query: str) -> Optional[Dict]:
    title_hash = hash_title(query)
    try:
        with open(CACHE_DIR / f"{title_hash}.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return None


def save_to_cache(query: str, data) -> None:
    title_hash = hash_title(query)
    with open(CACHE_DIR / f"{title_hash}.json", "w") as f:
        json.dump(data, f)


def fetch_results(query: str) -> Optional[Dict]:
    time.sleep(3)  # dont stress dblp
    options = {"q": query, "format": "json", "h": 1}
    wait_secs = 20
    while True:
        try:
            r = session.get(f"{DBLP_PUBL_SEARCH_API}?{urlencode(options)}")
        except requests.exceptions.ConnectionError:
            print("dblp protocol error")
            time.sleep(5)
            continue
        if not r.ok:
            print(f"waiting {wait_secs}s for dblp to unblock us...")
            time.sleep(wait_secs)
        else:
            break
    # save result to cache
    try:
        return r.json()
    except requests.exceptions.JSONDecodeError:
        print("dblp json decode error")


def search(query: str) -> Optional[DBLPPublication]:
    j = load_from_cache(query)
    if j is None:
        j = fetch_results(query)
        save_to_cache(query, j)

    hit = j.get("result").get("hits").get("hit")
    if hit is not None:
        info = hit[0].get("info")
        # sometimes the venue is a list
        venue = info.get("venue")
        if isinstance(venue, list):
            venue = venue[0]
        authors = list()
        if "authors" in info:
            authors_list = info.get("authors").get("author")
            if not isinstance(authors_list, list):
                # single author, wrap in list
                authors_list = [authors_list]
            for author in authors_list:
                if isinstance(author, dict):
                    authors.append(author.get("text"))
                else:
                    print("author not a dict", author)
        # fixme: check if publication belongs to our author
        return DBLPPublication(
            title=info.get("title"),
            year=info.get("year"),
            venue=venue,
            doi=info.get("doi"),
            url=info.get("ee"),
            type=info.get("type"),
            volume=info.get("volume"),
            key=info.get("key"),
            authors=authors,
        )
    return None

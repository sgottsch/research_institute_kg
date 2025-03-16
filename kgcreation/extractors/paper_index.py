from typing import Iterable

from kgcreation.models.paper import Paper


class PaperIndex:
    def __init__(self):
        self.papers_by_title = {}

    def get_paper_by_title(self, title: str) -> Paper:
        if title in self.papers_by_title:
            return self.papers_by_title[title]
        else:
            paper = Paper(title=title)
            self.papers_by_title[title] = paper
            return paper

    def get_papers(self) -> Iterable[Paper]:
        return self.papers_by_title.values()


paper_index = PaperIndex()

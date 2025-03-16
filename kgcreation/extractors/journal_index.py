from kgcreation.models.journal import Journal


class JournalIndex:
    def __init__(self):
        self.journals_by_name = {}

    def get_journal_by_name(self, journal_name) -> Journal:
        if journal_name in self.journals_by_name:
            return self.journals_by_name[journal_name]
        journal = Journal(journal_name)
        self.journals_by_name[journal_name] = journal
        return journal

    def get_journals(self):
        return self.journals_by_name.values()


journal_index = JournalIndex()

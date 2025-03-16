from kgcreation.models.conference import Conference


class ConferenceIndex:
    def __init__(self):
        self.conferences_by_name = {}

    def get_conference_by_name(self, conference_name: str) -> Conference:
        if conference_name in self.conferences_by_name:
            return self.conferences_by_name[conference_name]
        conference = Conference(conference_name)
        self.conferences_by_name[conference_name] = conference
        return conference

    def get_conferences(self):
        return self.conferences_by_name.values()


conference_index = ConferenceIndex()

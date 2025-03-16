import pandas as pd

from config import google_forms_answers_file_name, building_matches, research_interest_matches
from kgcreation.extractors.city_index import city_index
from kgcreation.extractors.person_index import Identifier, person_index

def value_or_none(cell_value):
    if pd.isnull(cell_value):
        return None
    else:
        return cell_value


def get_all_persons_from_google_forms():
    persons = []
    df = pd.read_excel(google_forms_answers_file_name, header=0)

    for index, row in df.iterrows():
        name = row["Full Name"]
        email = row["Institute Email Address"]
        institute_id = email.split("@")[0]
        buildings = value_or_none(row[13])
        # Added new features
        birth_date = value_or_none(row[7])
        languages = row[8]
        places = value_or_none(row[9])
        work_position = row[10]
        project = row[11]
        starting_date = value_or_none(row[12])
        building_floor = row[14]
        office_number = row[15]
        participate_history = row[16]
        participated_retreat = row[17]
        personal_webpage = row[18]
        google_scholar = value_or_none(row[19])
        orcid = value_or_none(row[20])
        researchlab = row[21]
        companies = row[22]
        managing_skill_Mobilise = row[23]
        managing_skill_manage_project = row[24]
        managing_skill_negotiate = row[25]
        managing_skill_evaluate = row[26]
        managing_skill_promote = row[27]
        doing_research_having_deciplinary = row[28]
        doing_research_scientific = row[29]
        doing_research_conduct_deciplinary = row[30]
        research_fields = value_or_none(row[112])

        person = person_index.get_person_by_id_or_name(Identifier.INST, institute_id, name)
        # print(date_of_birth)
        if birth_date:
            person.date_of_birth = birth_date.date()
        if starting_date:
            person.starting_date = starting_date.date()

        # Added new features on person
        for language in languages.split(","):
            person.languages.add(language.title().strip())

        if buildings:
            for building in buildings.split(","):
                building = building.title().strip()
                for building_name_old, building_name_new in building_matches.items():
                    if building == building_name_old:
                        building = building_name_new
                person.buildings.add(building)

        person.email = email
        person.institute_id = institute_id

        if places and "http" in places:
            for place in places.split("\n"):
                if not place:
                    continue
                place = place.strip()

                name = place.rsplit("/", 1)[1].replace("_", " ")
                city = city_index.get_city_by_id_or_name(place, name)
                person.cities.add(city)

        person.work_position = work_position
        person.project = project
        person.building_floor = building_floor
        person.office_number = office_number
        person.participate_history = participate_history
        person.participated_retreat = participated_retreat
        person.personal_webpage = personal_webpage

        if google_scholar and "user=" in google_scholar:
            person.google_scholar_id = google_scholar.split("user=")[1].split("&")[0]

        person.orcid = orcid
        person.researchlab = researchlab
        person.companies = companies
        person.managing_skill_Mobilise = managing_skill_Mobilise
        person.managing_skill_manage_project = managing_skill_manage_project
        person.managing_skill_negotiate = managing_skill_negotiate
        person.managing_skill_evaluate = managing_skill_evaluate
        person.managing_skill_promote = managing_skill_promote
        person.doing_research_having_deciplinary = doing_research_having_deciplinary
        person.doing_research_scientific = doing_research_scientific
        person.doing_research_conduct_deciplinary = doing_research_conduct_deciplinary

        if research_fields:
            person.interests.update(
                [
                    research_interest_matches.get(interest.strip(), interest.strip())
                    for interest in research_fields.split(",")
                ]
            )

        # print("buildings...", building)
        persons.append(person)

        # print("person..", person.name, person.buildings, person.languages,
        #    person.email, person.l3s_id, person.place, person.work_position,
        #    person.project, person.starting_date, person.building_floor,
        #    person.building_floor,person.office_number, person.participate_history,
        #    person.participated_retreat, person.personal_webpage, person.google_scholar_id,
        #    person.orcid)

    return persons


if __name__ == "__main__":
    print(len(get_all_persons_from_google_forms()))

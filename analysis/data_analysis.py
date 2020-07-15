import requests
import csv


def analyse_names():
    for year in ["2016", "2017", "2018", "2019", "2020"]:
        reader = csv.reader(open(year+'.csv'))
        population = 0
        for name in reader:
            first_name, last_name = extract_name(name)
            if first_name is not None:
                # print(first_name)
                population += 1  # Count the number of participants.

        # Create a csv file with each year's of data.
        writer = csv.writer(open("population_data.csv", 'a+'))
        writer.writerow([year, population])

    # return population



# Helpers
def extract_name(name):
    """
    Reads the csv and extracts names by splitting them as first/last name so that
    it can be passed to the API call.
    Note: The extra cases could have been avoided while forming the CSV i.e.
    improving on the design and structure of web scraper.
    """
    if "Keynote" not in name[0] and "Members" not in name[0] and "" != name[0]:
        if "prof." in name[0].lower() or "dr." in name[0].lower().strip():
            full_name = name[0].split(".")[1].strip()
            first_name = full_name.split(' ')[0]
            last_name = full_name.split(' ')[1]
        else:
            full_name = name[0].strip().split(' ')
            first_name = full_name[0]
            last_name = full_name[1]
        return first_name,last_name
    return None,None


if __name__ == "__main__":
    a = analyse_names()
    print(a)


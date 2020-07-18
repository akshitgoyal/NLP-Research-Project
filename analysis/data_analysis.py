import requests
import csv

import requests as requests

from analysis_helper import *

def analyse_names():
    """
    This function uses Namsor API to analyse the names, and generate the results
    in form of csv files. These  files are further used for a statistical
    analysis. The pdf report of this analysis is available in the analysis
    directory.
    """
    year_num = 0  # Years starting with 2016 as 0. Makes analysis easier.

    # for year in ["2016", "2017", "2018", "2019", "2020"]:
    for year in ["2016", "2017", "20"]:
        reader = csv.reader(open(year + '.csv'))
        population, male, female, other_gender, A, B_NL, HL, W_NL = 0,0,0,0,0,0,0,0
        gender_dict = {}
        random_list = []
        for name in reader:
            first_name, last_name = extract_name(name)
            if first_name is not None:
                population += 1  # Count the number of participants.
                random_list.append((first_name,last_name))
                # Extract Genders of participants using Namsor API.
                # name_dict = {"id": 1,
                #              "name": first_name + ' ' + last_name}


                # r = requests.get(
                #     'http://v2.namsor.com/NamSorAPIv2/api2/json/gender/' +
                #     first_name + '/' + last_name,
                #     headers={'X-API-KEY': '61f8c3dc68d36e701dd558f668eb4fb9'})
                # gender = r.json()['likelyGender']
                # if gender == 'male':
                #     male += 1
                # elif gender == 'female':
                #     female += 1
                # else:
                #     other_gender += 1

                # Extract Ethnicity of participants using Namsor API.
                # r1 = requests.get(
                #     'http://v2.namsor.com/NamSorAPIv2/api2/json/usRaceEthnicity/' +
                #     first_name + '/' + last_name,
                #     headers={'X-API-KEY': '61f8c3dc68d36e701dd558f668eb4fb9'})
                # raceEthnicity = r1.json()['raceEthnicity']
                # if raceEthnicity == "A":
                #     A += 1
                # elif raceEthnicity == "B_NL":
                #     B_NL += 1
                # elif raceEthnicity == "HL":
                #     HL += 1
                # elif raceEthnicity == "W_NL":
                #     W_NL += 1


        # Create a csv file with each year's of data.
        # Population Data
        # writer = csv.writer(open("population_data.csv", 'a+'))
        # writer.writerow([year_num, population])

        # # Gender Data
        # writer = csv.writer(open("gender_data.csv", 'a+'))
        # writer.writerow([year_num, male, female, other_gender])
        #
        # # Ethnicity Data
        # writer = csv.writer(open("ethnicity_data.csv", 'a+'))
        # writer.writerow([year_num, A, B_NL, HL, W_NL])
        # year_num += 1
    return random_list


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
            first_name = full_name.split(' ')[0].strip()
            last_name = full_name.split(' ')[1].strip()
        else:
            full_name = name[0].strip().split(' ')
            first_name = full_name[0].strip()
            last_name = full_name[1].strip()
        return first_name, last_name
    return None, None


if __name__ == "__main__":
    a = analyse_names()
    # print(a)
    gender_list = run(a)[0]


    l = {
  "personalNames": [
    {
      "id": "string",
      "firstName": "Akshit",
      "lastName": "Goyal"
    },
      {
          "id": "string",
          "firstName": "Vishnu",
          "lastName": "Varma"
      }
  ]
    }

    r = requests.post(
        'http://v2.namsor.com/NamSorAPIv2/api2/json/genderBatch', data=l, headers={'X-API-KEY': '453b1821ba92a90e1006418f8f1b1fad', "accept": "application/json",'Content-Type': "application/json"})
    print(r.text)



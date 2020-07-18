from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint
import csv
import pickle
import os

# Configure API key authorization: api_key
configuration = openapi_client.Configuration()
configuration.api_key['X-API-KEY'] = '61f8c3dc68d36e701dd558f668eb4fb9'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-API-KEY'] = 'Bearer'

# create an instance of the API class
api_instance = openapi_client.PersonalApi(
    openapi_client.ApiClient(configuration))


def generate_namsor_data():
    """
    This function calls NamSor API and extracts the required information about
    gender and ethnicity. The produced results are put into csv files and used
    for analysis using various statsmodel, pandas and numpy library. Other details
    can be found in the pdf report.

    """
    # Loading the cached data
    if os.path.isfile("extracted.pkl"):
        file = open('extracted.pkl', 'rb')
        names_dict = pickle.load(file)
        file.close()
    else:
        names_dict = {}
    year_num = 0
    for year in ["2016", "2017", "2018", "2019", "2020"]:
        reader = csv.reader(open(year + '.csv'))

        # Initializing the counters
        population, male, female, other_gender, A, B_NL, HL, W_NL = 0, 0, 0, 0, 0, 0, 0, 0

        # We need to setup 5 batches to make batch request to Namsor API.
        batch1 = openapi_client.BatchFirstLastNameIn()
        batch1.personal_names = []
        batch2 = openapi_client.BatchFirstLastNameIn()
        batch2.personal_names = []
        batch3 = openapi_client.BatchFirstLastNameIn()
        batch3.personal_names = []
        batch4 = openapi_client.BatchFirstLastNameIn()
        batch4.personal_names = []
        batch5 = openapi_client.BatchFirstLastNameIn()
        batch5.personal_names = []

        for fullname in reader:
            first_name, last_name = extract_name(fullname)
            if first_name is not None:
                new_fullname = first_name + " " + last_name
                if new_fullname not in names_dict.keys():
                    name = openapi_client.FirstLastNameIn()
                    names_dict[new_fullname] = [None, None]  # Gender, Ethnicity
                    name.first_name = first_name
                    name.last_name = last_name
                    if population < 100:
                        batch1.personal_names.append(name)
                    elif 100 <= population < 200:
                        batch2.personal_names.append(name)
                    elif 200 <= population < 300:
                        batch3.personal_names.append(name)
                    elif 300 <= population < 400:
                        batch4.personal_names.append(name)
                    elif 400 <= population < 500:
                        batch5.personal_names.append(name)
                else:
                    if names_dict[new_fullname][0] == 'male':
                        male += 1
                    else:
                        female += 1

                population += 1  # Count the number of participants.

        # API call for gender.
        for batch in [batch1, batch2, batch3, batch4, batch5]:
            try:
                api_response = api_instance.gender_batch(
                    batch_first_last_name_in=batch)
                pprint(api_response)
                for gender_dict in api_response.personal_names:
                    names_dict[gender_dict.first_name + " " +
                               gender_dict.last_name][0] = gender_dict.likely_gender
                    if gender_dict.likely_gender == 'male':
                        male += 1
                    else:
                        female += 1
            except ApiException as e:
                print(
                    "Exception when calling PersonalApi->gender_batch: %s\n" % e)

            # API call for race ethnicity.
            try:
                api_response2 = api_instance.us_race_ethnicity_batch(
                    batch_first_last_name_geo_in=batch)
                pprint(api_response2)
                for ethnicity_dict in api_response2.personal_names:
                    names_dict[ethnicity_dict.first_name + " " + ethnicity_dict.last_name][1] = ethnicity_dict.race_ethnicity
                    if ethnicity_dict.race_ethnicity  == 'A':
                        A += 1
                    elif ethnicity_dict.race_ethnicity == 'B_NL':
                        B_NL += 1
                    elif ethnicity_dict.race_ethnicity == 'HL':
                        HL += 1
                    elif ethnicity_dict.race_ethnicity == 'W_NL':
                        W_NL += 1

            except ApiException as e:
                print(
                    "Exception when calling PersonalApi->us_race_ethnicity_batch: %s\n" % e)

        # Create a csv file with each year's of data.
        # Population Data
        writer = csv.writer(open("population_data.csv", 'a+'))
        writer.writerow([year_num, population])

        # Gender Data
        writer = csv.writer(open("gender_data.csv", 'a+'))
        writer.writerow([year_num, male, female])

        # Ethnicity Data
        writer = csv.writer(open("ethnicity_data.csv", 'a+'))
        writer.writerow([year_num, A, B_NL, HL, W_NL])
        year_num += 1

    # Caching the extracted data.
    f = open("extracted.pkl", "wb")
    pickle.dump(names_dict, f)
    f.close()


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
    generate_namsor_data()

# Web Crawler and Analysis for NLP Research Project

A web crawler built using a popular tool called `Scrapy`. 

This software is built as a part of __`independent study course` under the guidance of Professor Andrew Petersen at University of Toronto Mississauga.__

In this research, we will be analysing the __participation of people in the different conferences__. Specifically, we will be looking at the people in academic conferences and industry conferences.

There are __two components__ to this software. First component of the software is to `crawl` different conference pages, and extract the names of the people who participated in that conference. The data 
is then exported to a csv file named after the conference. The extracted data from the csv files is feeded to the second component of the software. 

Currently, the software uses only two spider and works perfectly in extracting the names of the people from the domain: __`bigdataieee.org` for the years 2015-2020 and `fitc.ca` for the years 2002-2019.__ The results of the crawler are present in `/data_mining/sample_output`. This component of software itself can be located in `/data_mining/scrapper_tool/spiders`

In the second component, the software calls an external API called `Namsor` to analyse the names of the people. The API returns information like gender, ethnicity, etc for the names. This component of software can be located in `/analysis/industry_conferences/industry_conf_analysed_data/analysis.py` and `/analysis/academic_conferences/academic_conf_analysed_data/namsor_analysis.py` for the respective conferences. 
The output is stored in `ethnicity_data.csv`, `gender_data.csv` and `population_data.csv`.

Additionally to limit the number of calls(duplicate calls) to external API, we store the existing information as a dictionary in `extracted.pkl`.

A __formal statistical analysis report__ for the respective conferences can also be found in the same respepctive folders.


The other files are irrelevant to this project and can be used to extend the code if required to integrate with a specific application.


# How to install

`Pre-requisites`: Python3.0 or higher must be installed in your computer and included in the $PATH.

`Step 1:` You can just clone the repository on your device. 

`Step 2:` You must have scrapy installed in your command line which can simply be done by calling `pip install Scrapy`
For more details on installing scrapy, you can visit the official documentation at: https://docs.scrapy.org/en/latest/intro/install.html

# How to use it
## Names Extraction and Data Mining
Simply navigate to ~/spiders folder in your command line and make a call to the desired spider.  Note that we only have two spiders implemented called `people` and `tech`.
`people` is used for extracting the information from the academic based conference `bigdataieee.org` and `tech` is used for extracting the information from industry based conference `fitc.ca`.

You can execute it by the command: `scrapy crawl people` and `scrapy crawl tech` in your command line.  

## NLP and Data Analysis
Navigate to `~/analysis.py` or `~/namsor_analysis.py` and  run it through the python shell. 

__Note:__ You need to purchase an API key to use the tool. However, there is some small qouta allocated on free accounts. For more details on the usage and installation of this tool, you can visit the official documentation at: https://github.com/namsor/namsor-python-sdk2




# Extend the code
The crawler can be used as a sample and can be tweaked easily to crawl different pages depending on the requirements. Specifically, for this project we can also extract the location and institution names for the people attending these conferences to analyse better.


# License Information
This repository has a general MIT License with some addtional conditons. Please review the license before using any segments of the repository. 

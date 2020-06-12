# Web Crawler for NLP Project

A web crawler built using a popular tool called `Scrapy`. 

This software is built as a part of `independent study course` under the guidance of Professor Andrew Petersen at University of Toronto Mississauga.

The main purpose of the software is to `crawl` different conference pages, and extract the names of the people who participated in that conference. The data 
is then exported to a csv file named after the conference. The extracted data from the csv files will later be used for NLP research purposes.

Currently, the software uses only one spider and works perfectly in extracting the names of the people from the domain: `bigdataieee.org` for the years 2015-2020

The results of the crawler are also present in the directory as csv files.

# How to install

`Pre-requisites`: Python3.0 or higher must be installed in your computer and included in the $PATH.

`Step 1:` You can just clone the repository on your device. 

`Step 2:` You must have scrapy installed in your command line which can simply be done by calling `pip install Scrapy`
For more details on installing scrapy, you can visit the official documentation at: https://docs.scrapy.org/en/latest/intro/install.html

# How to use it

Simply navigate to project folder in your command line and make a call to the spider.  Note that we only have one spyder implemented called `people`

You can execute it by the command: `scrapy crawl people`

# Extend the code
The crawler can be used as a sample and can be tweaked easily to crawl different pages depending on the requirements. Specifically, for this project we can include another spyder to crawl the confernce years of 2013 and 2014 for the current domain.
Another possible extension to this specific project could be extracting data in a different domain in big data conferences.




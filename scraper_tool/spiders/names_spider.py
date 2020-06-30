import scrapy
import csv


class namesSpider(scrapy.Spider):
    """
    Please visit the GitHub documentation for further details on usage and
    improvements that can be done in the next iteration.
    """

    name = "people"
    allowed_domains = ["bigdataieee.org"]

    start_urls = [
        "http://bigdataieee.org/"
    ]

    def parse(self, response):
        """
        This is the main parse method. It will automatically called when we
        make a call to this spyder from command line.
        This method extracts all the conferences from past year whose links are
        available on the conference home page.
        """
        conference_links = response.xpath("//nav/ul/li/a")
        for conference in conference_links:
            link = conference.xpath("@href").extract_first()
            if not(link == "index.html" or
                   any(year in link for year in ["2013", "2014", "2015"])):
                yield scrapy.Request(link, callback=self.parse_conference)

    def parse_conference(self, response):
        """
        This method is used to parse each conference. It makes calls to different
        parser methods depending on the type of information we want.
        """
        links = response.xpath("//a")
        for link in links:
            page_name = link.xpath("text()").extract_first()
            if "organization committee" in page_name.lower():
                url = response.urljoin(link.xpath("@href").extract_first())
                yield scrapy.Request(url, callback=self.parse_committee_members)
            if "program committee" in page_name.lower():
                url = response.urljoin(link.xpath("@href").extract_first())
                yield scrapy.Request(url,callback=self.parse_program_committee)
            if "speeches" in page_name.lower():
                url = response.urljoin(link.xpath("@href").extract_first())
                yield scrapy.Request(url, callback=self.parse_keynote_speakers)

    def parse_committee_members(self, response):
        """
        This method is used for parsing the names of the people from committee
        members page.
        """
        names = []
        # We need to determine the year of conf from title as 2016 has
        # different structure for this section.
        title = response.xpath("//title/text()").extract_first()
        if any(year in title for year in ["2016", "2017", "2018"]):
            html_tag = '//span/strong'
        else:
            html_tag = '//span'

        # Data Scraping
        for sel in response.xpath(html_tag):
            name = sel.xpath('text()').extract()
            for n1 in name:  # Format varies in different years by ":" or ","
                if ':' in n1:
                    names.append(n1.split(':')[0].strip())
                else:
                    names.append(n1.split(',')[0].strip())

        # File Writing
        file_name = response.xpath("//title/text()").extract_first() + ".csv"
        data_cat = "Organization Committee Members"
        write_data_to_file(file_name, names, data_cat)

    def parse_program_committee(self, response):
        """
        This method is used for parsing the names of the people from program
        committee page.
        """
        # Data Scraping
        details = response.xpath("//tr/th")
        file_name = response.xpath("//title/text()").extract_first() + ".csv"
        names = []
        for i in range(0,len(details),3):
            names.append(details[i].xpath('text()').extract_first())

        # File Writing
        data_cat = "Program Committee Members"
        write_data_to_file(file_name, names, data_cat)

    def parse_keynote_speakers(self, response):
        """
        This method is used for parsing the names of the people from keynote
        speakers page.
        """
        # Data Scraping
        speaker_info = response.xpath("//tr/td/div/p/strong")
        file_name = response.xpath("//title/text()").extract_first() + ".csv"
        names = []
        for i in range(len(speaker_info)):
            names.append(speaker_info[i].xpath('text()').extract_first())

        # File Writing
        data_cat = "Keynote Speakers"
        write_data_to_file(file_name,names, data_cat)


def write_data_to_file(file_name, names, data_cat):
    """
    This function writes the data to the file taking into the account of different
    years and also divides the csv file into sections.

    NOTE: The sections in csv file are separated by adding "" in the row after
    each section.
    """
    writer = csv.writer(open(file_name, "a+"))
    writer.writerow([data_cat])
    for n in names:
        if n.strip().lower() != "name":
            writer.writerow([n])
    writer.writerow([""])  # This signifies that the category ended.



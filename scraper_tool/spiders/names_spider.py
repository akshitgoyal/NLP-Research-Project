import scrapy
import csv
import os


class namesSpider(scrapy.Spider):
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
            if not(link == "index.html" or "2014" in link or "2013" in link):
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
        special = False
        for sel in response.xpath('//span'):
            name = sel.xpath('text()').extract()
            for n1 in name:
                if ':' in n1:
                    temp = n1.split(':')[0].strip()
                    if temp == '':
                        special = True
                        break
                    names.append(temp)
                else:
                    names.append(n1.split(',')[0].strip())
            if special:
                break
        # Due to different structure amongst different pages, I had to add a
        # special case to extract all the information.
        if special:
            for sel in response.xpath('//span/strong'):
                name = sel.xpath('text()').extract()
                for n1 in name:
                    if ':' in n1:
                        names.append(n1.split(':')[0].strip())
                    else:
                        names.append(n1.split(',')[0].strip())

        file_name = response.xpath("//title/text()").extract_first() + ".csv"
        if os.path.isfile(file_name):
            mode = 'a+'
        else:
            mode = 'w+'
        with open(file_name, mode) as file:
            writer = csv.writer(file)
            # writer.writerow(['Names', 'Organization', 'Location'])
            writer.writerow(['Names'])
            for n in names:
                writer.writerow([n])

    def parse_program_committee(self, response):
        """
        This method is used for parsing the names of the people from program
        committee page.
        """
        details = response.xpath("//tr/th")
        file_name = response.xpath("//title/text()").extract_first() + ".csv"
        if os.path.isfile(file_name):
            mode = 'a+'
        else:
            mode = 'w+'

        for i in range(0,len(details),3):
            name = details[i].xpath('text()').extract_first()
            with open(file_name, mode) as file:
                write = csv.writer(file)
                write.writerow([name])

    def parse_keynote_speakers(self, response):
        """
        This method is used for parsing the names of the people from keynote
         speakers page.
        """
        speaker_info = response.xpath("//tr/td/div/p/strong")
        file_name = response.xpath("//title/text()").extract_first() + ".csv"
        if os.path.isfile(file_name):
            mode = 'a+'
        else:
            mode = 'w+'
        for i in range(len(speaker_info)):
            name = speaker_info[i].xpath('text()').extract_first()
            with open(file_name, mode) as file:
                write = csv.writer(file)
                write.writerow([name])

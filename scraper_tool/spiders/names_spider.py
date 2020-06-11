import scrapy
import csv
import os


class namesSpider(scrapy.Spider):
    name = "people"
    allowed_domains = ["bigdataieee.org"]

    start_urls = [
        "http://bigdataieee.org/BigData2016/"
    ]

    def parse(self, response):
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
        names = []
        special = False
        for sel in response.xpath('//span'):
            name = sel.xpath('text()').extract()
            print(name)
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

        # Some tags have <strong> in it which will make it difficult so we will treat it as a special cas.
        if special:
            for sel in response.xpath('//span/strong'):
                name = sel.xpath('text()').extract()
                for n1 in name:
                    if ':' in n1:
                        names.append(n1.split(':')[0].strip())
                    else:
                        names.append(n1.split(',')[0].strip())
        if os.path.isfile('names.csv'):
            mode = 'a+'
        else:
            mode = 'w'
        with open('names.csv', mode) as file:
            writer = csv.writer(file)
            writer.writerow(['Names', 'Organization', 'Location'])
            for n in names:
                writer.writerow([n])

    def parse_program_committee(self, response):
        details = response.xpath("//tr/th")
        if os.path.isfile('names.csv'):
            mode = 'a+'
        else:
            mode = 'w'
        for i in range(0,len(details),3):
            name = details[i].xpath('text()').extract_first()
            with open('names.csv', mode) as file:
                write = csv.writer(file)
                write.writerow([name])
            # print(name)


    def parse_keynote_speakers(self, response):

        speaker_info = response.xpath("//tr/td/div/p/strong")
        if os.path.isfile('names.csv'):
            mode = 'a+'
        else:
            mode = 'w'
        for i in range(len(speaker_info)):
            name = speaker_info[i].xpath('text()').extract_first()
            with open('names.csv', mode) as file:
                write = csv.writer(file)
                write.writerow([name])



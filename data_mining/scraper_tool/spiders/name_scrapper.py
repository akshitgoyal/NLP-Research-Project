import scrapy
import csv


class namesSrcapper(scrapy.Spider):
    """
    Please visit the GitHub documentation for further details on usage and
    improvements that can be done in the next iteration.
    """

    name = "tech"
    allowed_domains = ["fitc.ca"]

    start_urls = [
        "https://fitc.ca/"
    ]

    def parse(self, response):
        """
        This is the main parse method. It will automatically called when we
        make a call to this spyder from command line.
        This method extracts all the conferences from past year whose links are
        available on the conference home page.
        """
        # Links for the year 2002-2009
        tech_conf_years = ["event/to0" + str(year) + "/speakers/" for year in range(2,10)]
        # Links for the year 2010-2019
        tech_conf_years.extend(["event/to" + str(year) + "/speakers/" for year in range(10,20)])
        # Crawling each conference 2002-2019
        for conference in tech_conf_years:
            url = response.urljoin(conference)
            yield scrapy.Request(url, callback=self.parse_conference)

    def parse_conference(self, response):
        names = response.xpath('/html//div[@class = "speaker-name"]/text()').extract()
        for name_tag in names:
            # File Writing
            file_name = response.xpath("//title/text()").extract_first() + ".csv"
            writer = csv.writer(open(file_name, "a+"))
            writer.writerow([name_tag.strip()])

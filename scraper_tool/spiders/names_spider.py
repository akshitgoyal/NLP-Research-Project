import scrapy


class namesSpider(scrapy.Spider):
    name = "people"
    allowed_domains = ["bigdataieee.org"]

    start_urls = [
        "http://bigdataieee.org/BigData2020/CommitteeMember.html"
    ]

    def parse(self, response):
        names = []
        for sel in response.xpath('//span'):
            name = sel.xpath('text()').extract()
            print(name)
            for n1 in name:
                if ':' in n1:
                    names.append(n1.split(':')[0])
                else:
                    names.append(n1.split(',')[0])
        output = open("output.txt", "w")
        for n in names:
            output.write(n + '\n')
        output.close()





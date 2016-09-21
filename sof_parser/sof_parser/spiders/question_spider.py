import scrapy
from sof_parser.items import AppItem


class QuestionSpider(scrapy.Spider):

    name = "question"

    def __init__(self, tag='python', sort='votes', size=10):
        super(QuestionSpider, self).__init__()
        self.limiter = size

        self.sort = 'sort={}'.format(sort)
        self.size = 'pagesize={}'.format(size)
        self.tag = tag
        self.start_urls = [
            "http://stackoverflow.com/questions/tagged/{}?{}&{}".format(self.tag, self.sort, self.size),
            # 'http://stackoverflow.com/questions/tagged/python',
        ]
        print self.start_urls

    # start_urls = [
    #     'http://stackoverflow.com/questions/tagged/python?sort=votes&pageSize=30',
    #     # 'http://stackoverflow.com/questions/tagged/python',
    # ]

    # def start_requests(self):
    #     yield scrapy.Request('http://stackoverflow.com/questions/tagged/python', self.parse, meta={"dont_redirect": True})

    def parse_answer(self, response):
        answer = response.xpath('//div[@class="answer accepted-answer"]')
        item = AppItem()
        item['a_author'] = answer.xpath('table/tr/td[2]/table/tr/td[3]/div/div[@class="user-details"]/a/text()').extract()[0]
        item['a_data'] = answer.xpath('table/tr/td[2]/table/tr/td[3]//div[@class="user-action-time"]/span/text()').extract()[0]
        item['a_votes'] = answer.xpath('table/tr/td[1]/div/span[1]/text()').extract()[0]
        yield item

    def parse(self, response):
        questions = response.xpath('//div[@class="question-summary"]')
        item = AppItem()
        for question in questions[:self.limiter]:
            # import pdb; pdb.set_trace()
            item['q_author'] = self.take_xpath(question.xpath('div[@class="summary"]//div[@class="user-details"]/a/text()').extract())
            item['q_text'] = self.take_xpath(question.xpath('div[@class="summary"]/h3/a/text()').extract())
            item['q_votes'] = self.take_xpath(question.xpath('div[@class="statscontainer"]//div[@class="votes"]/span/strong/text()').extract())
            item['a_link'] = 'https://stackoverflow.com/{}'.format(question.xpath('div[@class="summary"]/h3/a/@href').extract()[0])
            item['q_data'] = self.take_xpath(question.xpath('div[@class="summary"]//div[@class="user-action-time"]/span/text()').extract())
            yield item
            # yield scrapy.Request(item['a_link'], callback=self.parse_answer)

    @staticmethod
    def take_xpath(xpath):
        if type(xpath) == list and len(xpath) > 0:
            return xpath[0]
        else:
            return 'Empty value'


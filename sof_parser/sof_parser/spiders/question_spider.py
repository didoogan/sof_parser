import scrapy
from sof_parser.items import AppItem


class QuestionSpider(scrapy.Spider):

    name = "question"
    url = 'http://stackoverflow.com'

    def __init__(self, tag='python', sort='votes', size=250):
        super(QuestionSpider, self).__init__()
        remainder = size % 10
        if remainder == 0:
            pages = size / 10
        else:
            pages = size / 10 + 1

        sort = sort
        tag = tag
        # self.start_urls = [
        #     for i in range(pages):
        #
        #     "{}/tagged/{}?page={}&sort={}".format(self.url, tag, sort),
        # ]
        urls = ['{}/tagged/{}?page={}&sort={}'.format(self.url, tag, x+1, sort) for x in range(pages)]
        if remainder != 0:
            urls[len(urls)-1] = '{}/tagged/{}?page={}&sort={}&pagesize={}'.format(self.url, tag, pages, sort, remainder)
        self.start_urls = urls

    def parse_answer(self, response):
        answer = response.xpath('//div[@class="answer accepted-answer"]')
        item = response.meta['item']
        # item['a_author'] = answer.xpath('table/tr/td[2]/table/tr/td[3]/div/div[@class="user-details"]/a/text()').extract_first()
        # item['a_data'] = answer.xpath('table/tr/td[2]/table/tr/td[3]//div[@class="user-action-time"]/span/text()').extract_first()
        # item['a_votes'] = answer.xpath('table/tr/td[1]/div/span[1]/text()').extract_first()
        item['a_author'] = answer.xpath('//div[@class="user-details"]/a/text()').extract_first()
        item['a_data'] = answer.xpath('//div[@class="user-action-time"]/span/text()').extract_first()
        item['a_votes'] = answer.xpath('table/tr/td[1]/div/span[1]/text()').extract_first()
        yield item

    def parse(self, response):
        questions = response.xpath('//div[@class="question-summary"]')
        for question in questions[:self.limiter]:
            # import pdb; pdb.set_trace()
            item = AppItem()
            # item['q_author'] = question.xpath('div[@class="summary"]//div[@class="user-details"]/a/text()').extract_first()
            item['q_author'] = question.xpath('//div[@class="user-details"]/a/text()').extract_first()
            item['q_text'] = question.xpath('div[@class="summary"]/h3/a/text()').extract_first()
            # item['q_votes'] = question.xpath('div[@class="statscontainer"]//div[@class="votes"]/span/strong/text()').extract_first()
            item['q_votes'] = question.xpath('//div[@class="votes"]/span/strong/text()').extract_first()
            item['a_link'] = '{}/{}'.format(self.url, question.xpath('div[@class="summary"]/h3/a/@href').extract_first())
            # item['q_data'] = question.xpath('div[@class="summary"]//div[@class="user-action-time"]/span/text()').extract_first()
            item['q_data'] = question.xpath('//div[@class="user-action-time"]/span/text()').extract_first()
            # yield item
            yield scrapy.Request(item['a_link'], callback=self.parse_answer, meta={'item': item})

        # next_page = response.xpath('//a[@rel="next"]/@href').extract_first()
        # next_page = "{}{}".format(self.url, response.xpath('//a[@rel="next"]/@href').extract_first())
        # if next_page and len(questions) < self.limiter:
        #     self.limiter = self.limiter - 50
        #     yield scrapy.Request(next_page, callback=self.parse)




import scrapy
from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse(self, response):
        """Парсер ссылок на карточки PEP."""
        tbody = response.css('tbody')

        for tr in tbody.css('tr'):
            link_pep_page = tr.css('td').css('a::attr(href)').get()
            if link_pep_page is not None:
                yield response.follow(link_pep_page, callback=self.parse_pep)

    def parse_pep(self, response):
        """Парсер карточки PEP."""
        data = {
            'number': response.xpath('//h1').re_first(r'PEP \d{2,4}'),
            'name': response.css('h1.page-title::text').get(),
            'status': response.css('dt:contains("Status") + dd').xpath('//abbr/text()').get()
        }
        yield PepParseItem(data)

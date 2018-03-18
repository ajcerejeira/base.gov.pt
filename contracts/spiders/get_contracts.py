import json
import scrapy


class GetContractsSpider(scrapy.Spider):
    name = 'get_contracts'
    allowed_domains = ['base.gov.pt']
    base_url = 'http://www.base.gov.pt/base2/rest/contratos'
    ncontracts = 867164
    step = 100

    def start_requests(self):
        for i in range(1, self.ncontracts, self.step):
            headers = {'Range': '{}-{}'.format(i, i + self.step - 1)}
            yield scrapy.Request(url=self.base_url, headers=headers,
                                 dont_filter=True)

    def parse(self, response):
        contracts = json.loads(response.body_as_unicode())

        for contract in contracts:
            yield response.follow('{}/{}'.format(self.base_url, contract['id']),
                                  self.parse_contract)

    def parse_contract(self, response):
        contract = json.loads(response.body_as_unicode())
        yield contract

import json
import scrapy
import requests
from lxml import html


class GetContractsSpider(scrapy.Spider):
    name = 'get_contracts'
    allowed_domains = ['base.gov.pt']
    base_url = 'http://www.base.gov.pt/base2/rest/contratos'
    ncontracts = 0
    step = 100

    def get_total_number_of_contracts(self):

        URL = "http://www.base.gov.pt/Base/pt/ResultadosPesquisa"
        page = requests.get(URL, params={'type': 'contratos'})
        tree = html.fromstring(page.text)

        number_of_contracts = tree.xpath('//p[text()="Foram encontrados "]/span/text()')
        number_of_contracts = int(number_of_contracts[0])
        return number_of_contracts

    def start_requests(self):
        self.ncontracts = self.get_total_number_of_contracts()

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

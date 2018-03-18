# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import re
from scrapy.contrib.exporter import CsvItemExporter


class ContractsPipeline(object):
    def open_spider(self, spider):
        self.contracts_file = open('contracts.csv', 'w+b')
        self.contracts_csv = CsvItemExporter(self.contracts_file)

        self.contestants_file = open('contestants.csv', 'w+b')
        self.contestants_csv = CsvItemExporter(self.contestants_file)

        self.invitees_file = open('invitees.csv', 'w+b')
        self.invitees_csv = CsvItemExporter(self.invitees_file)

        self.documents_file = open('documents.csv', 'w+b')
        self.documents_csv = CsvItemExporter(self.documents_file)

        self.places_file = open('places.csv', 'w+b')
        self.places_csv = CsvItemExporter(self.places_file)

    def close_spider(self, spider):
        self.contracts_csv.finish_exporting()
        self.contracts_file.close()

        self.contestants_csv.finish_exporting()
        self.contestants_file.close()

        self.invitees_csv.finish_exporting()
        self.invitees_file.close()

        self.documents_csv.finish_exporting()
        self.documents_file.close()

        self.places_csv.finish_exporting()
        self.places_file.close()

    def process_item(self, item, spider):
        # Write the contestants to a separate table
        for contestant in item['contestants']:
            row = { 'contract': item['id'],
                    'contestant': contestant['id'],
                    'description': contestant['description'],
                    'nif': contestant['nif'] }
            self.contestants_csv.export_item(row)
        del item['contestants']

        # Write the invitees to a separate table
        for invitee in item['invitees']:
            row = { 'contract': item['id'],
                    'invitee': invitee['id'],
                    'description': invitee['description'],
                    'nif': invitee['nif'] }
            self.invitees_csv.export_item(row)
        del item['invitees']

        # Write the documents to a separate table
        for document in item['documents']:
            row = { 'contract': item['id'],
                    'document': document['id'],
                    'description': document['description'] }
            self.documents_csv.export_item(row)
        del item['documents']

        # Write places to a separate table
        if item['executionPlace']:
            for place in item['executionPlace'].split('<BR/>'):
                country, state, city = place.split(', ')
                row = { 'contract': item['id'],
                        'country': country,
                        'state': state,
                        'city': city }
            del item['executionPlace']

        # Normalize the contracted entity
        if item['contracted']:
            item['contracted_id'] = item['contracted'][0]['id']
            item['contracted_nif'] = item['contracted'][0]['nif']
            item['contracted'] = item['contracted'][0]['description']
        else:
            item['contracted_id'] = None
            item['contracted_nif'] = None
            item['contracted'] = None

        # Normalize the contracting entity
        if item['contracting']:
            item['contracting_id'] = item['contracting'][0]['id']
            item['contracting_nif'] = item['contracting'][0]['nif']
            item['contracting'] = item['contracting'][0]['description']
        else:
            item['contracting_id'] = None
            item['contracting_nif'] = None
            item['contracting'] = None

        def normalizeCurrency(money):
            """Converts a Portuguese local currency string in a float unit."""
            normalized = re.sub(r'^((\d+)\.)?(\d+),(\d+) €$', r'\2\3.\4', money)
            return float(normalized)

        # Normalize the total effective price
        if item['totalEffectivePrice']:
            money = item['totalEffectivePrice']
            item['totalEffectivePrice'] = normalizeCurrency(money)

        # Normalize the initial contractual price
        if item['initialContractualPrice']:
            money = item['initialContractualPrice']
            item['initialContractualPrice'] = normalizeCurrency(money)

        self.contracts_csv.export_item(item)

        return item

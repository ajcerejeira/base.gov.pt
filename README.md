# base.gov.pt

A crawler that fetches data from <http://www.base.gov.pt/>.

## Spiders

 - `get_contracts`: a spider that fetches the data regarding the public
   contracts from the website REST API
   (<http://www.base.gov.pt/base2/rest/contratos/>), and 

## Usage

Download the spider and its dependencies:

    git clone 'https://github.com/ajcerejeira/base.gov.pt.git'
    cd base.gov.pt/
    pip install -r requirements.txt

And then run the desired spider:

    scrapy crawl get_contracts

This will generate the following files:

 - `contracts.csv` - main table, containing the most important info regarding
   the contracts
 - `contestants.csv`
 - `invitees.csv`
 - `documents.csv`
 - `places.csv` 

Please be patient, since it takes some hours before it completes (on my machine
it took about 26 hours to finish gathering all data).

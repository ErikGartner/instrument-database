import requests
import grequests
import json
import codecs
from bs4 import BeautifulSoup

class GoogleFinance:
    """
    Fetches:
    - Symbol
    - Name
    - Exchange
    - Website
    - Summary
    - Sector
    """

    URL='https://www.google.com/finance?start=0&num=50000&q=[exchange == "%s"]&restype=company&output=json'
    QUERY_URL='https://www.google.com/finance?q=%s:%s'
    SUPPORTED_EXCHANGES = ['NYSE', 'STO']
    PARALLEL_REQUESTS = 25

    def __init__(self):
        pass

    def fetch(self):
        print('Fetching master list')
        stocks = []
        for exchange in GoogleFinance.SUPPORTED_EXCHANGES:
            url = GoogleFinance.URL % exchange
            data = requests.get(url).text
            data = data.replace('\\x22', "'")
            data = codecs.decode(data, 'unicode_escape')
            master_list = json.loads(data)
            for s in master_list['searchresults']:
                stock = {
                    'name': s['title'],
                    'exchange': s['exchange'],
                    'ticker': s['ticker'],
                    'extra': {
                            'google-finance-id': s['id'],
                            'google-finance-url': GoogleFinance.QUERY_URL % (s['exchange'], s['ticker']),
                            'currency': s['local_currency_symbol']
                        },
                    'logo': '',
                    'website': ''
                }
                stocks.append(stock)

        for i in range(0, len(stocks), GoogleFinance.PARALLEL_REQUESTS):
            pass
            #self.fetch_page(stocks[i:i + GoogleFinance.PARALLEL_REQUESTS])
        return stocks

    def fetch_page(self, stocks):
        """
        Use gevents to perform multiple async http reqeusts to fetch data from stock page.
        """
        urls = [stock['extra']['google-finance-url'] for stock in stocks]
        rs = [grequests.get(u) for u in urls]
        resps = grequests.map(rs, size=GoogleFinance.PARALLEL_REQUESTS)

        for i in range(len(stocks)):
            response = resps[i]
            stock = stocks[i]

            if response.status_code != 200:
                print('Failed to fetch page for: %s' % stock)
                continue

            soup = BeautifulSoup(response.text, 'html.parser')

            # Find website
            link = soup.find(id='fs-chome')
            if link != None:
                stock['extra']['website'] = link.get_text().strip()

            summary = soup.find('div', class_='companySummary')
            if summary != None:
                stock['extra']['summary'] = summary.get_text().replace('More from Reuters »', '').strip()

            sector = soup.find(id='sector')
            if sector != None:
                stock['extra']['sector'] = sector.get_text().strip()


    def website_to_logo(self, website):
        return 'https://logo.clearbit.com/%s?format=png&size=302' % website


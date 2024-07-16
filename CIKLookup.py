import requests 

class EdgarCIKLookup:
    def __init__(self): 
        self.company_name_dict = {}
        self.ticker_dict = {}
        self.fetch_data = {}

    def fetch_data(self):
        urls = {
            'company_tickers': 'https://www.sec.gov/files/company_tickers.json',
            'company_tickers_exchange': 'https://www.sec.gov/files/company_tickers_exchange.json',
            'company_tickers_mf': 'https://www.sec.gov/files/company_tickers_mf.json'
        }

        headers = {
            'User-Agent': 'YourCompanyName AdminContact@yourcompanydomain.com',
            'Accept-Encoding': 'gzip, deflate',
            'Host': 'www.sec.gov'
        }

        for url_key, url in urls.items():
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                self.parse_data(data) #parse and store the retrieved data
    
    def parse_data(self,data):
        for entry in data:
            if 'ticker' in entry:
                # add entry to ticker dict w ticker as the key
                self.ticker_dict[entry['ticker']] = entry 
            if 'title' in entry:
                self.company_name_dict[entry['title']] = entry
    
    def name_to_cik(self, company_name):
        # look up cik for a given company name
        if company_name in self.company_name_dict:
            entry = self.company_name_dict[company_name]
            return (entry['cik'], entry.get('title', ''), entry.get('ticker', ''))
        else: 
            return None


    def ticker_to_cik(self, ticker):
        if ticker in self.ticker_dict:
            entry = self.ticker_dict[ticker]
            return (entry['cik'], entry.get('title', ''), ticker)
        else:
            return None
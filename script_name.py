import requests

# interact with the SEC EDGAR API
class SECFilingsClient: 
    BASE_URL = "https://data.sec.gov/submissions/"
    HEADERS = {"User-Agent": "MLT GS gspivey@mlt.org"}

    def __init__(self):
        pass

    def __get_company_filings(self, cik):
        # format cik to 10 digits to construct the url and retrieve json data
        url = f"{self.BASE_URL}CIK{cik:0>10}.json"
        # send request to the api
        response = requests.get(url, headers=self.HEADERS)
        # check if request was successful and return the json response
        response.raise_for_status()
        return response.json()
    
    # filings is the filing data found by the json response, quarter is just for 10-q filings
    def __find_filings(self, filings, form_type, year, quarter=None):
        accession_numbers = filings['filings']['recent']['accessionNumber']
        primary_documents = filings['filings']['recent']['primaryDocument']
        document_descriptions = filings['filings']['recent']['primaryDocumentDescription']
        filing_dates = filings['filings']['recent']['filingDate']
        forms = filings['filings']['recent']['form']

        for i, form in enumerate(forms):
            if form == form_type: 
                filing_year = int(filing_dates[i][:4])
                if filing_year == year:
                    if form_type == '10-Q' and quarter is not None:
                        filing_quarter = (int(filing_dates[i][5:7])-1) // 3 + 1
                        if filing_quarter != quarter:
                            continue
                    return {
                        'form' : form,
                        'description': document_descriptions[i], 
                        'url': f"https://www.sec.gov/Archives/edgar/data/{cik}/{accession_numbers[i].replace('-', '')}/{primary_documents[i]}"
                    }
        return None
        
    def annual_filing(self, cik, year):
        filings = self.__get_company_filings(cik)
        return self.__find_filings(filings, '10-K', year)
        
    def quarterly_filing(self, cik, year, quarter):
        filings = self.__get_company_filings(cik)
        return self.__find_filings(filings, '10-Q', year, quarter)
    
if __name__ == "__main__":
    client = SECFilingsClient()
    cik = "0000320193"
    year = 2023
    quarter = 2

    annual_filing = client.annual_filing(cik, year)
    if annual_filing:
        print(f"Annual Filing: {annual_filing}")
    else:
        print("No annual filing found")

    quarterly_filing = client.quarterly_filing(cik, year, quarter)
    if quarterly_filing:
        print(f"Quarterly Filing: {quarterly_filing}")
    else:
        print("No quarterly filing found")
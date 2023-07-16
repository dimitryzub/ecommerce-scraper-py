from google_shopping import GoogleShoppingSearch

scraper = GoogleShoppingSearch(
    api_key='<your_serpapi_api_key>',
    query='coffee starbucks',
    domain='google.de',
    country='de',
    language='de'
)

filters = scraper.get_filters()
scraper.print(filters)

scraper.save_to_json(filters)
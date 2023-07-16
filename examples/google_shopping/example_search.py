from google_shopping import GoogleShoppingSearch

scraper = GoogleShoppingSearch(
    api_key='<your_serpapi_api_key>',
    query='coffee',
    domain='google.de',
    country='de',
    language='de',
    price_from=20,
    price_to=200,
    results_limit=150
)

products = scraper.get_products()
scraper.print(products)

scraper.save_to_json(products)
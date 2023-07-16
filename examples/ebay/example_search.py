from ebay import EbaySearch

scraper = EbaySearch(
    api_key='<your_serpapi_api_key>',
    query='coffee starbucks',
    price_from=20,
    price_to=200,
    results_limit=250,
    domain='ebay.com'
)

products = scraper.get_products()
scraper.print(products)

scraper.save_to_json(products)
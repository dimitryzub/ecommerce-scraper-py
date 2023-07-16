from walmart import WalmartSearch

scraper = WalmartSearch(
    api_key='<your_serpapi_api_key>',
    query='coffee starbucks',
    price_from=20,
    price_to=200,
    results_limit=150,
    # store="356"
)

products = scraper.get_products()
scraper.print(products)

scraper.save_to_json(products)
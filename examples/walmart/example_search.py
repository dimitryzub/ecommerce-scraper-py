from walmart import WalmartSearch

scraper = WalmartSearch(
    api_key='5868ece26d41221f5e19ae8b3e355d22db23df1712da675d144760fc30d57988',
    query='coffee starbucks',
    price_from=20,
    price_to=200,
    results_limit=150,
    # store="356"
)

products = scraper.get_products()
scraper.print(products)

scraper.save_to_json(products)
from walmart import WalmartSearch, WalmartProduct

search_scraper = WalmartSearch(
    api_key='<your_serpapi_api_key>',
    query='coffee starbucks',
    price_from=20,
    price_to=200,
    results_limit=10
)

data = []

products = search_scraper.get_products()

for product in products:
    product_scraper = WalmartProduct(
        api_key='<your_serpapi_api_key>',
        product_id=product['product_id'],
        reviews_limit=15
    )

    product_data = product_scraper.get_product()
    data.append(product_data)

search_scraper.print(data)
search_scraper.save_to_json(data)
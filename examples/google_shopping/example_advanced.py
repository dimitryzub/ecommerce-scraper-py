from google_shopping import GoogleShoppingSearch, GoogleShoppingProduct

search_scraper = GoogleShoppingSearch(
    api_key='<your_serpapi_api_key>',
    query='Sony PlayStation 5',
    price_from=400,
    price_to=1000,
    results_limit=10,
    domain='google.de',
    country='de',
    language='de'
)

data = []

products = search_scraper.get_products()

for product in products:
    product_scraper = GoogleShoppingProduct(
        api_key='<your_serpapi_api_key>',
        product_id=product['product_id'],
        reviews_limit=15,
        domain='google.de',
        country='de',
        language='de'
    )

    product_data = product_scraper.get_product()
    data.append(product_data)

search_scraper.print(data)
search_scraper.save_to_json(data)
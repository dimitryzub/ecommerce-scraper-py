from home_depot import HomeDepotSearch, HomeDepotProduct

search_scraper = HomeDepotSearch(
    api_key='<your_serpapi_api_key>',
    query='chair',
    price_from=20,
    price_to=200,
    results_limit=10,
    zip_code='04401'    # zip code must be in the format '12345' or '12345-6789'
)

data = []

products = search_scraper.get_products()

for product in products:
    product_scraper = HomeDepotProduct(
        api_key='<your_serpapi_api_key>',
        product_id=product['product_id']
    )

    product_data = product_scraper.get_product()
    data.append(product_data)

search_scraper.print(data)
search_scraper.save_to_json(data)
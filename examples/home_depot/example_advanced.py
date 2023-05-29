from home_depot import HomeDepotSearch, HomeDepotProduct

API_KEY = '5868ece26d41221f5e19ae8b3e355d22db23df1712da675d144760fc30d57988'

search_scraper = HomeDepotSearch(
    api_key=API_KEY,
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
        api_key=API_KEY,
        product_id=product['product_id']
    )

    product_data = product_scraper.get_product()
    data.append(product_data)

search_scraper.print(data)
search_scraper.save_to_json(data)
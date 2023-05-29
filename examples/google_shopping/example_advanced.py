from google_shopping import GoogleShoppingSearch, GoogleShoppingProduct

API_KEY = '5868ece26d41221f5e19ae8b3e355d22db23df1712da675d144760fc30d57988'

search_scraper = GoogleShoppingSearch(
    api_key=API_KEY,
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
        api_key=API_KEY,
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
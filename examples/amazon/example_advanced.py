from amazon import AmazonSearch, AmazonProduct

search_scraper = AmazonSearch(
    query='coffee',
    results_limit=5,
    price_from=20,
    price_to=50,
    currency='USD',
    language='en_US',
    customer_reviews_rating=4,
    multiplier=1
)

data = []

products = search_scraper.get_products()

for product in products:
    product_scraper = AmazonProduct(
        link=product['link'],
        reviews_limit=15,
        multiplier=1,
        currency='USD',
        language='en_US'
    )

    product_data = product_scraper.get_product()
    data.append(product_data)

search_scraper.print(data)
search_scraper.save_to_json(data)
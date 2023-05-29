from amazon import AmazonSearch

scraper = AmazonSearch(
    query='coffee',
    results_limit=125,
    price_from=20,
    price_to=50,
    currency='USD',
    language='en_US',
    customer_reviews_rating=4,
    multiplier=1
)

products = scraper.get_products()
scraper.print(products)

scraper.save_to_json(products)

from amazon import AmazonProduct

scraper = AmazonProduct(
    link='https://www.amazon.com/McCafe-Premium-Roast-Decaf-Coffee/dp/B07GCNDL91/ref=sr_1_1?currency=USD&keywords=coffee&qid=1684849762&refinements=p_36%3A2000-5000%2Cp_72%3A1248897011&rnid=1248895011&s=grocery&sr=1-1&th=1',
    reviews_limit=35,
    multiplier=1,
    currency='USD',
    language='en_US'
)

# product_info = scraper.get_product_info()
# scraper.print(product_info)

# product_reviews = scraper.get_product_reviews()
# scraper.print(product_reviews)

product = scraper.get_product()
scraper.print(product)

scraper.save_to_json(product)
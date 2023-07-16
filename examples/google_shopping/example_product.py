from google_shopping import GoogleShoppingProduct

scraper = GoogleShoppingProduct(
    api_key='<your_serpapi_api_key>',
    product_id=14019378181107046593,
    reviews_limit=125
)

# product_info = scraper.get_product_info()
# scraper.print(product_info)

# product_reviews = scraper.get_product_reviews()
# scraper.print(product_reviews)

product = scraper.get_product()
scraper.print(product)

scraper.save_to_json(product)
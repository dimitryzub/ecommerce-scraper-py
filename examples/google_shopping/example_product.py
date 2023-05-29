from google_shopping import GoogleShoppingProduct

scraper = GoogleShoppingProduct(
    api_key='5868ece26d41221f5e19ae8b3e355d22db23df1712da675d144760fc30d57988',
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
from walmart import WalmartProduct

scraper = WalmartProduct(
    api_key='<your_serpapi_api_key>',
    product_id=520468661,
    reviews_limit=125
)

# product_info = scraper.get_product_info()
# scraper.print(product_info)

# product_reviews = scraper.get_product_reviews()
# scraper.print(product_reviews)

product = scraper.get_product()
scraper.print(product)

scraper.save_to_json(product)
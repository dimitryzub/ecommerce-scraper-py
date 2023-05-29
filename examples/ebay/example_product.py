from ebay import EbayProduct

scraper = EbayProduct(
    link='https://www.ebay.com/itm/2-Bags-STARBUCKS-French-Roast-DARK-Whole-Bean-100-Arabica-Coffee-40oz-ea-09-23/144356021636',
    reviews_limit=125,
    multiplier=1
)

# product_info = scraper.get_product_info()
# scraper.print(product_info)

# product_reviews = scraper.get_product_reviews()
# scraper.print(product_reviews)

product = scraper.get_product()
scraper.print(product)

scraper.save_to_json(product)
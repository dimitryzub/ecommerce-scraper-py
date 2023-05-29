from ebay import EbaySearch, EbayProduct

search_scraper = EbaySearch(
    api_key='5868ece26d41221f5e19ae8b3e355d22db23df1712da675d144760fc30d57988',
    query='coffee',
    results_limit=5,
    domain='ebay.com'
)

data = []

products = search_scraper.get_products()

for product in products:
    product_scraper = EbayProduct(
        link=product['link'],
        reviews_limit=15,
        multiplier=1
    )

    product_data = product_scraper.get_product()
    data.append(product_data)

search_scraper.print(data)
search_scraper.save_to_json(data)
from home_depot import HomeDepotProduct

scraper = HomeDepotProduct(
    api_key='5868ece26d41221f5e19ae8b3e355d22db23df1712da675d144760fc30d57988',
    product_id=202054749
)

product = scraper.get_product()
scraper.print(product)

scraper.save_to_json(product)
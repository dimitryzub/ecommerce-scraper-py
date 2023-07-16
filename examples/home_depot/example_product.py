from home_depot import HomeDepotProduct

scraper = HomeDepotProduct(
    api_key='<your_serpapi_api_key>',
    product_id=202054749
)

product = scraper.get_product()
scraper.print(product)

scraper.save_to_json(product)
from home_depot import HomeDepotSearch

scraper = HomeDepotSearch(
    api_key='5868ece26d41221f5e19ae8b3e355d22db23df1712da675d144760fc30d57988',
    query='chair',
    price_from=20,
    price_to=200,
    results_limit=150,
    # zip_code='04401'    # zip code must be in the format '12345' or '12345-6789'
)

products = scraper.get_products()
scraper.print(products)

scraper.save_to_json(products)
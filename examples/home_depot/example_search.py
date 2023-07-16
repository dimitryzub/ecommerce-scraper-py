from home_depot import HomeDepotSearch

scraper = HomeDepotSearch(
    api_key='<your_serpapi_api_key>',
    query='chair',
    price_from=20,
    price_to=200,
    results_limit=150,
    # zip_code='04401'    # zip code must be in the format '12345' or '12345-6789'
)

products = scraper.get_products()
scraper.print(products)

scraper.save_to_json(products)
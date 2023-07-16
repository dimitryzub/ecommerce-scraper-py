from home_depot import HomeDepotSearch

scraper = HomeDepotSearch(
    api_key='<your_serpapi_api_key>',
    query='chair'
)

filters = scraper.get_filters()
scraper.print(filters)

scraper.save_to_json(filters)
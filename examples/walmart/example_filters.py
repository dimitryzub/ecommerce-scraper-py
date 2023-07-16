from walmart import WalmartSearch

scraper = WalmartSearch(
    api_key='<your_serpapi_api_key>',
    query='coffee starbucks'
)

filters = scraper.get_filters()
scraper.print(filters)

scraper.save_to_json(filters)
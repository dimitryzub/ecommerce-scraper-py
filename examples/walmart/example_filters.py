from walmart import WalmartSearch

scraper = WalmartSearch(
    api_key='5868ece26d41221f5e19ae8b3e355d22db23df1712da675d144760fc30d57988',
    query='coffee starbucks'
)

filters = scraper.get_filters()
scraper.print(filters)

scraper.save_to_json(filters)
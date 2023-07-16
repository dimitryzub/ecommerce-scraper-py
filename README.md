<div align="center">
<p>Sponsor of the project:</p>
<div>
   <img src="https://user-images.githubusercontent.com/78694043/231375638-5bbf2989-fc7b-482a-b6fe-603d1d6d613f.svg" width="60" alt="SerpApi">
</div>
<a href="https://serpapi.com">
	<b>API to get search engine results with ease.</b>
</a>
</div>

<h1 align="center">Python E-Commerce Scraper 🛒</h1>

<h4 align="center">
  Scrape Amazon, eBay, Walmart, Home Depot and Google Shopping from a single Python module.
</h4>

<div align="center">
   <img src="https://user-images.githubusercontent.com/78694043/231951681-c56b79ce-1643-406c-90c7-39692c6eeaee.svg" width="500" alt="SerpApi">
</div>


This tool uses [SerpApi](https://serpapi.com/) as a tool to parse data. 

You can use provided API key that will be available after installation, however, it's purely for testing purposes to see if the tool fits your needs. If you'll be using it for your own purpose (personal or commercial), you have to use [your own SerpApi key](https://serpapi.com/manage-api-key).


## ⚙️Installation

```bash
$ pip install ecommerce-scraper-py
```

## Scrape Google Shopping

#### Example to scrape search page

```python
from google_shopping import GoogleShoppingSearch

scraper = GoogleShoppingSearch(
    api_key='<your_serpapi_api_key>',
    query='coffee',
    domain='google.de',
    country='de',
    language='de',
    price_from=20,
    price_to=200,
    results_limit=150
)

products = scraper.get_products()
scraper.print(products)

scraper.save_to_json(products)
```

___

#### Example to scrape product page

```python
from google_shopping import GoogleShoppingProduct

scraper = GoogleShoppingProduct(
    api_key='<your_serpapi_api_key>',
    product_id=14019378181107046593,
    reviews_limit=125
)

product = scraper.get_product()
scraper.print(product)

scraper.save_to_json(product)
```

___

#### Advanced example

```python
from google_shopping import GoogleShoppingSearch, GoogleShoppingProduct

search_scraper = GoogleShoppingSearch(
    api_key='<your_serpapi_api_key>',
    query='Sony PlayStation 5',
    price_from=400,
    price_to=1000,
    results_limit=10,
    domain='google.de',
    country='de',
    language='de'
)

data = []

products = search_scraper.get_products()

for product in products:
    product_scraper = GoogleShoppingProduct(
        api_key='<your_serpapi_api_key>',
        product_id=product['product_id'],
        reviews_limit=15,
        domain='google.de',
        country='de',
        language='de'
    )

    product_data = product_scraper.get_product()
    data.append(product_data)

search_scraper.print(data)
search_scraper.save_to_json(data)
```

## Scrape Walmart

#### Example to scrape search page

```python
from walmart import WalmartSearch

scraper = WalmartSearch(
    api_key='<your_serpapi_api_key>',
    query='coffee starbucks',
    price_from=20,
    price_to=200,
    results_limit=150,
    # store="356"
)

products = scraper.get_products()
scraper.print(products)

scraper.save_to_json(products)
```

___

#### Example to scrape product page

```python
from walmart import WalmartProduct

scraper = WalmartProduct(
    api_key='<your_serpapi_api_key>',
    product_id=520468661,
    reviews_limit=125
)

product = scraper.get_product()
scraper.print(product)

scraper.save_to_json(product)
```

___

#### Advanced example

```python
from walmart import WalmartSearch, WalmartProduct

search_scraper = WalmartSearch(
    api_key='<your_serpapi_api_key>',
    query='coffee starbucks',
    price_from=20,
    price_to=200,
    results_limit=10
)

data = []

products = search_scraper.get_products()

for product in products:
    product_scraper = WalmartProduct(
        api_key='<your_serpapi_api_key>',
        product_id=product['product_id'],
        reviews_limit=15
    )

    product_data = product_scraper.get_product()
    data.append(product_data)

search_scraper.print(data)
search_scraper.save_to_json(data)
```

## Scrape Home Depot

#### Example to scrape search page

```python
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
```

___

#### Example to scrape product page

```python
from home_depot import HomeDepotProduct

scraper = HomeDepotProduct(
    api_key='<your_serpapi_api_key>',
    product_id=202054749
)

product = scraper.get_product()
scraper.print(product)

scraper.save_to_json(product)
```

___

#### Advanced example

```python
from home_depot import HomeDepotSearch, HomeDepotProduct

search_scraper = HomeDepotSearch(
    api_key='<your_serpapi_api_key>',
    query='chair',
    price_from=20,
    price_to=200,
    results_limit=10,
    zip_code='04401'    # zip code must be in the format '12345' or '12345-6789'
)

data = []

products = search_scraper.get_products()

for product in products:
    product_scraper = HomeDepotProduct(
        api_key='<your_serpapi_api_key>',
        product_id=product['product_id']
    )

    product_data = product_scraper.get_product()
    data.append(product_data)

search_scraper.print(data)
search_scraper.save_to_json(data)
```

## Scrape Amazon

#### Example to scrape search page

```python
from amazon import AmazonSearch

scraper = AmazonSearch(
    query='coffee',
    results_limit=125,
    price_from=20,
    price_to=50,
    currency='USD',
    language='en_US',
    customer_reviews_rating=4,
    multiplier=1
)

products = scraper.get_products()
scraper.print(products)

scraper.save_to_json(products)
```

___

#### Example to scrape product page

```python
from amazon import AmazonProduct

scraper = AmazonProduct(
    link='https://www.amazon.com/McCafe-Premium-Roast-Decaf-Coffee/dp/B07GCNDL91/ref=sr_1_1?currency=USD&keywords=coffee&qid=1684849762&refinements=p_36%3A2000-5000%2Cp_72%3A1248897011&rnid=1248895011&s=grocery&sr=1-1&th=1',
    reviews_limit=35,
    multiplier=1,
    currency='USD',
    language='en_US'
)

product = scraper.get_product()
scraper.print(product)

scraper.save_to_json(product)
```

___

#### Advanced example

```python
from amazon import AmazonSearch, AmazonProduct

search_scraper = AmazonSearch(
    query='coffee',
    results_limit=5,
    price_from=20,
    price_to=50,
    currency='USD',
    language='en_US',
    customer_reviews_rating=4,
    multiplier=1
)

data = []

products = search_scraper.get_products()

for product in products:
    product_scraper = AmazonProduct(
        link=product['link'],
        reviews_limit=15,
        multiplier=1,
        currency='USD',
        language='en_US'
    )

    product_data = product_scraper.get_product()
    data.append(product_data)

search_scraper.print(data)
search_scraper.save_to_json(data)
```

## Scrape eBay

#### Example to scrape search page

```python
from ebay import EbaySearch

scraper = EbaySearch(
    api_key='<your_serpapi_api_key>',
    query='coffee starbucks',
    price_from=20,
    price_to=200,
    results_limit=250,
    domain='ebay.com'
)

products = scraper.get_products()
scraper.print(products)

scraper.save_to_json(products)
```

___

#### Example to scrape product page

```python
from ebay import EbayProduct

scraper = EbayProduct(
    link='https://www.ebay.com/itm/2-Bags-STARBUCKS-French-Roast-DARK-Whole-Bean-100-Arabica-Coffee-40oz-ea-09-23/144356021636',
    reviews_limit=125,
    multiplier=1
)

product = scraper.get_product()
scraper.print(product)

scraper.save_to_json(product)
```

___

#### Advanced example

```python
from ebay import EbaySearch, EbayProduct

search_scraper = EbaySearch(
    api_key='<your_serpapi_api_key>',
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
```

### ✍Contributing

Feel free to open bug issue, something isn't working, what feature to add, or anything else.

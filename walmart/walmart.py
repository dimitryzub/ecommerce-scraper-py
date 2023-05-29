from .stores import stores
from serpapi import WalmartSearch as SerpApiSearch
from copy import deepcopy
from urllib.parse import urlsplit, parse_qsl
import json


class WalmartParams(object):
    def __init__(self, store) -> None:
        self.store = store


    @staticmethod
    def get_stores() -> list:
        return stores


    def _validate_params(self):
        store_id = next(
            (el['store_id'] for el in stores if el['store_id'] == self.store or el['address'] == self.store),
            None
        )

        if self.store and not store_id:
            raise ValueError('Please select available store (use "WalmartParams.get_stores()" to get all stores list).')

        return store_id


class WalmartSearch(WalmartParams):
    def __init__(self,
                 api_key: str,
                 query: str,
                 price_from: float = 0,
                 price_to: float = 0,
                 results_limit: int = 10,
                 sort: int = 1,
                 store = None) -> None:
        self.api_key = api_key
        self.query = query
        self.price_from = price_from
        self.price_to = price_to
        self.results_limit = results_limit
        self.sort = sort
        super().__init__(store)


    def __get_params(self) -> dict:
        params = {
            'api_key': self.api_key,        # https://serpapi.com/manage-api-key
            'engine': 'walmart',            # search engine
            'device': 'desktop',            # device to use to get the results
            'query': self.query,            # search query
            'spelling': True,               # activate spelling fix
        }

        if self.price_from != 0 or self.price_to != 0:
            if self.price_from > self.price_to or self.price_from < 0 or self.price_to < 0:
                raise ValueError('Please set correct price arguments.')
            params['min_price'] = self.price_from
            params['max_price'] = self.price_to

        if self.store:
            store_id = self._validate_params()
            params['store_id'] = store_id

        if self.sort == 1:
            params['sort'] = 'best_match'
        elif self.sort == 2:
            params['sort'] = 'best_seller'
        elif self.sort == 3:
            params['sort'] = 'price_low'
        elif self.sort == 4:
            params['sort'] = 'price_high'
        elif self.sort == 5:
            params['sort'] = 'rating_high'
        elif self.sort == 6:
            params['sort'] = 'new'
        else:
            raise ValueError('Please set correct sort argument (from 1 to 6).')

        return params


    def get_products(self) -> list:
        params = self.__get_params()        # parameters for search
        search = SerpApiSearch(params)      # data extraction on the SerpApi backend
        results = search.get_dict()         # JSON -> Python dict

        products = []
        limit = deepcopy(self.results_limit)

        # pagination if needed
        while True:
            walmart_results = results.get('organic_results', [])

            if limit < len(walmart_results):
                products.extend(walmart_results[:limit])
                break

            limit -= len(walmart_results)
            products.extend(walmart_results)

            if 'next' in results.get('serpapi_pagination', {}):
                search.params_dict.update(
                    dict(parse_qsl(urlsplit(results.get('serpapi_pagination', {}).get('next')).query)))
            else:
                break

            results = search.get_dict()     # new page results

        for index, product in enumerate(products, start=0):
            products[index]['product_id'] = deepcopy(products[index]['us_item_id'])
            products[index]['position'] = index + 1

            if products[index].get('primary_offer', {}).get('offer_id', None):
                del products[index]['primary_offer']['offer_id']
            del products[index]['us_item_id']
            del products[index]['seller_id']
            del products[index]['serpapi_product_page_url']

        return products


    def get_filters(self) -> list:
        params = self.__get_params()        # parameters for search
        search = SerpApiSearch(params)      # data extraction on the SerpApi backend
        results = search.get_dict()         # JSON -> Python dict

        return results.get('filters', 'Filters will be in the future.')


    def save_to_json(self, data) -> None:
        with open(f'walmart_search_{self.query.lower().replace(" ", "_")}.json', 'w',
                  encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=2, ensure_ascii=False)


    @staticmethod
    def print(data) -> None:
        """Prints pretty JSON instead of regular print()"""
        print(json.dumps(data, indent=2, ensure_ascii=False))


class WalmartProduct(WalmartParams):
    def __init__(self,
                 api_key: str,
                 product_id,
                 reviews_limit: int = 10,
                 store = None) -> None:
        self.api_key = api_key
        self.product_id = product_id
        self.reviews_limit = reviews_limit
        super().__init__(store)


    def __get_params(self, engine) -> dict:
        # parameters for search
        params = {
            'api_key': self.api_key,        # https://serpapi.com/manage-api-key
            'engine': engine,               # search engine
            'device': 'desktop',            # device to use to get the results
            'product_id': self.product_id,  # Walmart ID of a product
        }

        if self.store and engine == 'walmart_product':
            store_id = self._validate_params()
            params['store_id'] = store_id

        return params


    def get_product_info(self) -> dict:
        params = self.__get_params(engine='walmart_product')
        search = SerpApiSearch(params)      # data extraction on the SerpApi backend
        results = search.get_dict()         # JSON -> Python dict

        product_info = results['product_result']

        product_info['product_id'] = self.product_id

        if product_info.get('arrival_date', None):
            del product_info['arrival_date']
        if product_info.get('delivery_option', {}).get('arrival_date', None):
            del product_info['delivery_option']['arrival_date']
        del product_info['us_item_id']
        del product_info['upc']
        del product_info['seller_id']
        del product_info['product_type_id']
        del product_info['offer_id']

        for index, offer in enumerate(product_info.get('offers', []), start=0):
            del product_info['offers'][index]['seller_id']
            del product_info['offers'][index]['catalog_seller_id']

        return product_info


    def get_product_reviews(self) -> list:
        params = self.__get_params(engine='walmart_product_reviews')
        params['page'] = 1                  # pagination for reviews
        search = SerpApiSearch(params)      # data extraction on the SerpApi backend
        results = search.get_dict()         # JSON -> Python dict

        reviews = []

        product_reviews = results.get('total_count', 0)

        if product_reviews:
            limit = self.reviews_limit if self.reviews_limit < product_reviews else product_reviews

            while True:
                reviews_results = results.get('reviews', [])

                if limit < len(reviews_results):
                    reviews.extend(reviews_results[:limit])
                    break

                limit -= len(reviews_results)
                reviews.extend(reviews_results)

                params['page'] += 1
                results = search.get_dict() # new page results

        # index recalculation because on each page the review position starts from 1
        for index, review in enumerate(reviews, start=0):
            review['position'] = index + 1

        return reviews


    def get_product(self) -> dict:
        product_data = {
            'product': self.get_product_info(),
            'reviews': self.get_product_reviews()
        }

        return product_data


    def save_to_json(self, data) -> None:
        with open(f'walmart_product_{self.product_id}.json', 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=2, ensure_ascii=False)


    @staticmethod
    def print(data) -> None:
        """Prints pretty JSON instead of regular print()"""
        print(json.dumps(data, indent=2, ensure_ascii=False))

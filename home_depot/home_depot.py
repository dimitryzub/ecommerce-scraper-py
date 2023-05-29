from serpapi import HomeDepotSearch as SerpApiSearch
from copy import deepcopy
from urllib.parse import urlsplit, parse_qsl
import json, re


class HomeDepotSearch(object):
    def __init__(self,
                 api_key: str,
                 query: str,
                 price_from: float = 0,
                 price_to: float = 0,
                 results_limit: int = 10,
                 sort: int = 1,
                 zip_code = None) -> None:
        self.api_key = api_key
        self.query = query
        self.price_from = price_from
        self.price_to = price_to
        self.results_limit = results_limit
        self.sort = sort
        self.zip_code = zip_code


    def __get_params(self) -> dict:
        params = {
            'api_key': self.api_key,        # https://serpapi.com/manage-api-key
            'engine': 'home_depot',         # search engine
            'device': 'desktop',            # device to use to get the results
            'q': self.query,                # search query
            'ps': 48,                       # number of items per page
            'page': 1,                      # pagination
        }

        # https://regex101.com/r/UnEKoe/1
        zip_pattern = re.compile(r'^\d{5}(-\d{4})?$')

        if self.zip_code:
            if not zip_pattern.match(self.zip_code):
                raise ValueError('Please set a correct ZIP code.')
            params['delivery_zip'] = self.zip_code

        if self.price_from != 0 or self.price_to != 0:
            if self.price_from > self.price_to or self.price_from < 0 or self.price_to < 0:
                raise ValueError('Please set correct price arguments.')
            params['lowerbound'] = self.price_from
            params['upperbound'] = self.price_to

        if self.sort == 1:
            params['hd_sort'] = 'best_match'
        elif self.sort == 2:
            params['hd_sort'] = 'top_sellers'
        elif self.sort == 3:
            params['hd_sort'] = 'price_low_to_high'
        elif self.sort == 4:
            params['hd_sort'] = 'price_high_to_low'
        elif self.sort == 5:
            params['hd_sort'] = 'top_rated'
        else:
            raise ValueError('Please set correct sort argument (from 1 to 5).')

        return params


    def get_products(self) -> list:
        params = self.__get_params()        # parameters for search
        search = SerpApiSearch(params)      # data extraction on the SerpApi backend
        results = search.get_dict()         # JSON -> Python dict

        products = []
        limit = deepcopy(self.results_limit)

        # pagination if needed
        while 'error' not in results:
            home_depot_results = results.get('products', [])

            if limit < len(home_depot_results):
                products.extend(home_depot_results[:limit])
                break

            limit -= len(home_depot_results)
            products.extend(home_depot_results)

            params['page'] += 1
            results = search.get_dict()     # new page results

        for index, product in enumerate(products, start=0):
            products[index]['position'] = index + 1

            del products[index]['serpapi_link']

        return products


    def get_filters(self) -> list:
        params = self.__get_params()        # parameters for search
        search = SerpApiSearch(params)      # data extraction on the SerpApi backend
        results = search.get_dict()         # JSON -> Python dict

        return results.get('filters', [])


    def save_to_json(self, data) -> None:
        with open(f'home_depot_search_{self.query.lower().replace(" ", "_")}.json', 'w',
                  encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=2, ensure_ascii=False)


    @staticmethod
    def print(data) -> None:
        """Prints pretty JSON instead of regular print()"""
        print(json.dumps(data, indent=2, ensure_ascii=False))


class HomeDepotProduct(object):
    def __init__(self,
                 api_key: str,
                 product_id,
                 zip_code = None) -> None:
        self.api_key = api_key
        self.product_id = product_id
        self.zip_code = zip_code


    def __get_params(self) -> dict:
        params = {
            'api_key': self.api_key,        # https://serpapi.com/manage-api-key
            'engine': 'home_depot_product', # search engine
            'device': 'desktop',            # device to use to get the results
            'product_id': self.product_id,  # Home Depot ID of a product
        }

        # https://regex101.com/r/UnEKoe/1
        zip_pattern = re.compile(r'^\d{5}(-\d{4})?$')

        if self.zip_code:
            if not zip_pattern.match(self.zip_code):
                raise ValueError('Please set a correct ZIP code.')
            params['delivery_zip'] = self.zip_code

        return params


    def get_product(self) -> dict:
        """Returns:
            Dictionary with product data without reviews
        """
        params = self.__get_params()
        search = SerpApiSearch(params)      # data extraction on the SerpApi backend
        results = search.get_dict()         # JSON -> Python dict

        product_info = results['product_results']
        del product_info['upc']

        return product_info


    def save_to_json(self, data) -> None:
        with open(f'home_depot_product_{self.product_id}.json', 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=2, ensure_ascii=False)


    @staticmethod
    def print(data) -> None:
        """Prints pretty JSON instead of regular print()"""
        print(json.dumps(data, indent=2, ensure_ascii=False))

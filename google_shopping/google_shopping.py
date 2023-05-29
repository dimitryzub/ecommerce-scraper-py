from .domains import domains
from .countries import countries
from .languages import languages
from serpapi import GoogleSearch
from copy import deepcopy
from urllib.parse import urlsplit, parse_qsl
import json


class GoogleShoppingParams(object):
    def __init__(self, domain: str, country: str, language: str) -> None:
        self.domain = domain
        self.country = country
        self.language = language


    @staticmethod
    def get_domains() -> list:
        return domains


    @staticmethod
    def get_countries() -> list:
        return countries


    @staticmethod
    def get_languages() -> list:
        return languages


    def _validate_params(self):
        selected_domain = next(
            (el for el in domains if
             el['domain'].lower() == self.domain.lower() or el['country_name'].lower() == self.domain.lower()),
            None
        )
        if self.domain and not selected_domain:
            raise ValueError(
                'Please select available domain (use "GoogleShoppingParams.get_domains()" to get all domains list).')

        selected_country = next(
            (el['code'] for el in countries if
             el['code'].lower() == self.country.lower() or el['name'].lower() == self.country.lower()),
            None
        )
        if self.country and not selected_country:
            raise ValueError(
                'Please select available country (use "GoogleShoppingParams.get_countries()" to get all countries list).')

        selected_language = next(
            (el['code'] for el in languages if
             el['code'].lower() == self.language.lower() or el['name'].lower() == self.language.lower()),
            None
        )
        if self.language and not selected_language:
            raise ValueError(
                'Please select available language (use "GoogleShoppingParams.get_languages()" to get all languages list).')

        domain = selected_domain['domain'] if selected_domain else 'google.com'
        country = selected_country or selected_domain['default_country_code'] if selected_domain else 'us'
        language = selected_language or selected_domain['default_language_code'] if selected_domain else 'en'

        return domain, country, language


class GoogleShoppingSearch(GoogleShoppingParams):
    def __init__(self,
                 api_key: str,
                 query: str,
                 price_from: float = 0,
                 price_to: float = 0,
                 results_limit: int = 10,
                 sort: int = 1,
                 domain: str = 'google.com',
                 country: str = 'us',
                 language: str = 'en') -> None:
        self.api_key = api_key
        self.query = query
        self.price_from = price_from
        self.price_to = price_to
        self.results_limit = results_limit
        self.sort = sort
        super().__init__(domain, country, language)


    def __get_tbs(self) -> str:
        tbs = ''

        if self.sort == 1:
            tbs = 'p_ord:r'
        elif self.sort == 2:
            tbs = 'p_ord:rv'
        elif self.sort == 3:
            tbs = 'p_ord:p'
        elif self.sort == 4:
            tbs = 'p_ord:pd'
        else:
            raise ValueError('Please set correct sort argument (from 1 to 4).')

        if self.price_from != 0 or self.price_to != 0:
            if self.price_from > self.price_to or self.price_from < 0 or self.price_to < 0:
                raise ValueError('Please set correct price arguments.')
            tbs += f",mr:1,price:1,ppr_min:{self.price_from},ppr_max:{self.price_to}"

        return tbs


    def __get_params(self) -> dict:
        domain, country, language = self._validate_params()

        params = {
            'api_key': self.api_key,        # https://serpapi.com/manage-api-key
            'engine': 'google_shopping',    # search engine
            'device': 'desktop',            # device to use to get the results
            'q': self.query,                # search query
            'google_domain': domain,        # Google domain to use
            'gl': country,                  # country of the search
            'hl': language,                 # language of the search
            'start': 0,                     # result offset
            'num': 100,                     # maximum number of results
            'tbs': self.__get_tbs()         # advanced search parameters
        }

        return params


    def get_products(self) -> list:
        params = self.__get_params()        # parameters for search
        search = GoogleSearch(params)       # data extraction on the SerpApi backend
        results = search.get_dict()         # JSON -> Python dict

        products = []
        limit = deepcopy(self.results_limit)

        # pagination if needed
        while True:
            shopping_results = results.get('shopping_results', [])

            if limit < 100:
                products.extend(shopping_results[:limit])
                break

            limit -= 100
            products.extend(shopping_results)

            params['start'] += params['num']
            results = search.get_dict()

        # index recalculation because on each page the position starts from 1
        for index, product in enumerate(products, start=0):
            products[index]['position'] = index + 1

            del products[index]['serpapi_product_api']
            del products[index]['number_of_comparisons']
            del products[index]['comparison_link']
            del products[index]['serpapi_product_api_comparisons']

        return products


    def get_filters(self) -> list:
        params = self.__get_params()        # parameters for search
        search = GoogleSearch(params)       # data extraction on the SerpApi backend
        results = search.get_dict()         # JSON -> Python dict

        return results.get('filters', [])


    def save_to_json(self, data) -> None:
        with open(f'google_shopping_search_{self.query.lower().replace(" ", "_")}.json', 'w',
                  encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=2, ensure_ascii=False)


    @staticmethod
    def print(data) -> None:
        """Prints pretty JSON instead of regular print()"""
        print(json.dumps(data, indent=2, ensure_ascii=False))


class GoogleShoppingProduct(GoogleShoppingParams):
    def __init__(self,
                 api_key: str,
                 product_id,
                 reviews_limit: int = 10,
                 domain: str = 'google.com',
                 country: str = 'us',
                 language: str = 'en') -> None:
        self.api_key = api_key
        self.product_id = product_id
        self.reviews_limit = reviews_limit
        super().__init__(domain, country, language)


    def __get_params(self) -> dict:
        domain, country, language = self._validate_params()

        params = {
            'api_key': self.api_key,        # https://serpapi.com/manage-api-key
            'engine': 'google_product',     # search engine
            'device': 'desktop',            # device to use to get the results
            'product_id': self.product_id,  # Google Shopping ID of a product
            'google_domain': domain,        # Google domain to use
            'gl': country,                  # country of the search
            'hl': language,                 # language of the search
        }

        return params


    def get_product_info(self) -> dict:
        params = self.__get_params()        # parameters for search
        search = GoogleSearch(params)       # data extraction on the SerpApi backend
        results = search.get_dict()         # JSON -> Python dict

        return results['product_results']


    def get_product_reviews(self) -> list:
        params = self.__get_params()        # parameters for search
        params['reviews'] = True            # more reviews, could be also set as '1` which is the same as True
        search = GoogleSearch(params)       # data extraction on the SerpApi backend
        results = search.get_dict()         # JSON -> Python dict

        reviews = []

        product_reviews = results.get('product_results', {}).get('reviews', 0)

        if product_reviews:
            limit = self.reviews_limit if self.reviews_limit < product_reviews else product_reviews

            while True:
                reviews_results = results.get('reviews_results', {}).get('reviews', [])

                if limit < 10:
                    reviews.extend(reviews_results[:limit])
                    break

                limit -= 10
                reviews.extend(reviews_results)

                if 'next' in results.get('serpapi_pagination', {}):
                    search.params_dict.update(dict(parse_qsl(urlsplit(results.get('serpapi_pagination', {}).get('next')).query)))
                else:
                    break

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
        with open(f'google_shopping_product_{self.product_id}.json', 'w',
                  encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=2, ensure_ascii=False)


    @staticmethod
    def print(data) -> None:
        """Prints pretty JSON instead of regular print()"""
        print(json.dumps(data, indent=2, ensure_ascii=False))

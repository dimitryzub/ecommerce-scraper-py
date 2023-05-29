from .domains import domains
from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selectolax.lexbor import LexborHTMLParser
from serpapi import EbaySearch as SerpApiSearch
from copy import deepcopy
from urllib.parse import urlsplit, parse_qsl
import json, re, time


class EbayParams(object):
    def __init__(self, domain) -> None:
        self.domain = domain


    @staticmethod
    def get_domains() -> list:
        return domains


    def _validate_params(self):
        selected_domain = next(
            ((el['domain'] for el in domains if el['domain'] == self.domain or el['country'] == self.domain)),
            None
        )

        if self.domain and not selected_domain:
            raise ValueError('Please select available domain (use "EbayParams.get_domains()" to get all domains list).')

        return selected_domain


class EbaySearch(EbayParams):
    def __init__(self,
                 api_key: str,
                 query: str,
                 price_from: float = 0,
                 price_to: float = 0,
                 results_limit: int = 10,
                 domain = 'ebay.com') -> None:
        self.api_key = api_key
        self.query = query
        self.price_from = price_from
        self.price_to = price_to
        self.results_limit = results_limit
        super().__init__(domain)


    def __get_params(self) -> dict:
        domain = self._validate_params()

        params = {
            'api_key': self.api_key,        # https://serpapi.com/manage-api-key
            'engine': 'ebay',            # search engine
            'device': 'desktop',            # device to use to get the results
            'ebay_domain': domain,          # eBay domain to use
            '_nkw': self.query,             # search query
            '_ipg': 200,                    # number of items per page
            '_pgn': 1,                      # pagination
        }

        if self.price_from != 0 or self.price_to != 0:
            if self.price_from > self.price_to or self.price_from < 0 or self.price_to < 0:
                raise ValueError('Please set correct price arguments.')
            params['_udlo'] = self.price_from
            params['_udhi'] = self.price_to

        return params


    def get_products(self) -> list:
        params = self.__get_params()        # parameters for search
        search = SerpApiSearch(params)      # data extraction on the SerpApi backend
        results = search.get_dict()         # JSON -> Python dict

        products = []
        limit = deepcopy(self.results_limit)

        # pagination if needed
        while 'error' not in results:
            ebay_results = results.get('organic_results', [])

            if limit < len(ebay_results):
                products.extend(ebay_results[:limit])
                break

            limit -= len(ebay_results)
            products.extend(ebay_results)

            params['_pgn'] += 1
            results = search.get_dict()     # new page results

        for index, product in enumerate(products, start=0):
            products[index]['position'] = index + 1

        return products


    def save_to_json(self, data) -> None:
        with open(f'ebay_search_{self.query.lower().replace(" ", "_")}.json', 'w',
                  encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=2, ensure_ascii=False)


    @staticmethod
    def print(data) -> None:
        """Prints pretty JSON instead of regular print()"""
        print(json.dumps(data, indent=2, ensure_ascii=False))


class EbayProduct(object):
    def __init__(self, link: str, reviews_limit: int = 10, multiplier: float = 1.0) -> None:
        self.link = link
        self.reviews_limit = reviews_limit
        self.multiplier = multiplier
        self.driver = self.__get_browser_instance()
        self.product_id = self.__get_product_id()


    def __del__(self):
        self.driver.quit()


    def __get_product_id(self):
        # https://regex101.com/r/82v2sq/1
        product_id = re.search(r'/(\d{7,})\??', self.link).group(1)

        return product_id


    def __get_browser_instance(self):
        service = Service(ChromeDriverManager().install())

        options = webdriver.ChromeOptions()
        options.add_argument('start-maximized')
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_experimental_option('excludeSwitches', ['enable-automation', 'enable-logging'])
        options.add_experimental_option('useAutomationExtension', False)

        driver = webdriver.Chrome(service=service, options=options)

        stealth(
            driver,
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
            languages=['en-US', 'en'],
            vendor='Google Inc.',
            platform='Win32',
            webgl_vendor='Intel Inc.',
            renderer='Intel Iris OpenGL Engine',
            fix_hairline=True,
        )

        driver.get(self.link)

        return driver


    def get_product_info(self) -> dict:
        parser = LexborHTMLParser(self.driver.page_source)

        title = parser.root.css_first('[data-testid="x-item-title"]').text(strip=True)

        raw_condition = parser.root.css_first('[data-testid="x-item-condition"] [data-testid="ux-textual-display"]')
        condition = raw_condition.text(strip=True) if raw_condition else None

        raw_price = parser.root.css_first('[data-testid="x-price-primary"] > span > span')
        price = raw_price.text(strip=True) if raw_price else None

        item_specifics = {}
        item_specifics_elements = parser.root.css('[data-testid="x-about-this-item"] [data-testid="ux-layout-section__item"], [data-testid="x-about-this-item"] [data-testid="ux-layout-section-evo__item"]')

        for element in item_specifics_elements:
            label = element.css_first('.ux-labels-values__labels:nth-child(1) span').text(strip=True)
            value = element.css_first('.ux-labels-values__values:nth-child(2) span').text(strip=True)
            item_specifics[label] = value

            if element.css_first('.ux-labels-values__labels:nth-child(3)'):
                sub_label = element.css_first('.ux-labels-values__labels:nth-child(3) span').text(strip=True)
                sub_value = element.css_first('.ux-labels-values__values:nth-child(4) span').text(strip=True)
                item_specifics[sub_label] = sub_value

        about_product = {}
        about_product_elements = parser.root.css('[data-testid="x-product-details"] [data-testid="ux-layout-section"], [data-testid="x-product-details"] [data-testid="ux-layout-section-module-evo"]')

        for element in about_product_elements:
            section_title = element.css_first('.section-title').text(strip=True)
            labels_values = {}
            labels_values_elements = element.css('[data-testid="ux-labels-values"]')

            for lv_element in labels_values_elements:
                lv_label = lv_element.css_first('.ux-labels-values__labels-content').text(strip=True)
                lv_value = lv_element.css_first('.ux-labels-values__values-content').text(strip=True)
                labels_values[lv_label] = lv_value

            about_product[section_title] = labels_values

        raw_rating = parser.root.css_first('#review-ratings-cntr > span:first-child')
        rating = float(raw_rating.attributes.get('title').split(' ')[0]) if raw_rating else None

        raw_reviews = parser.root.css_first('#review-ratings-cntr > span:last-child')
        reviews = int(raw_reviews.text(strip=True).split(' ')[0].replace(',', '').replace('.', '')) if raw_reviews else None

        description = ''
        frames = self.driver.find_elements(By.TAG_NAME, "iframe")

        for frame in frames:
            self.driver.switch_to.frame(frame)

            try:
                text = self.driver.find_element(By.CSS_SELECTOR, "#ds_div").text.strip()
                if text:
                    description = text
                    self.driver.switch_to.default_content()
                    break
            except:
                pass

            self.driver.switch_to.default_content()

        data = {
            'title': title,
            'link': self.link,
            'product_id': self.product_id,
            'condition': condition,
            'price': price,
            'item_specifics': item_specifics,
            'about_product': about_product,
            'description': description,
            'rating': rating,
            'reviews': reviews
        }

        return data


    def get_product_reviews(self) -> list:
        reviews = []

        try:
            self.driver.execute_script('document.querySelector(".reviews-right .reviews-header a").click()')
            time.sleep(self.multiplier * 1)

            while True:
                self.driver.find_element(By.CSS_SELECTOR, 'body').send_keys(Keys.END)
                time.sleep(self.multiplier * 1)

                parser = LexborHTMLParser(self.driver.page_source)

                for el in parser.css('.ebay-review-section'):
                    name = el.css_first('[itemprop="author"]').text(strip=True)
                    raw_rating = el.css_first('[itemprop="reviewRating"]')
                    rating = float(raw_rating.attributes.get('title', '0 ').split(' ')[0]) if raw_rating else None
                    raw_heading = el.css_first('[itemprop="name"]')
                    heading = raw_heading.text(strip=True) if raw_heading else None
                    date = el.css_first('[itemprop="datePublished"]').text(strip=True)
                    raw_badge = el.css_first('.ebay-review-section-l > span:nth-child(5)')
                    badge = raw_badge.text(strip=True) if raw_badge else None
                    raw_review = el.css_first('[itemprop="reviewBody"]')
                    review = raw_review.text(strip=True) if raw_review else None

                    reviews.append({
                        'name': name,
                        'rating': rating,
                        'heading': heading,
                        'date': date,
                        'badge': badge,
                        'review': review
                    })

                if len(reviews) >= self.reviews_limit:
                    reviews = reviews[:self.reviews_limit]
                    break

                try:
                    self.driver.find_element(By.CSS_SELECTOR, 'nav li:last-child > a:not(.disabled)').click()
                    time.sleep(self.multiplier * 1)
                    self.driver.find_element(By.CSS_SELECTOR, '.ebay-review-section')
                except:
                    break

            self.driver.find_element(By.CSS_SELECTOR, '.vertical-align a').click()
            time.sleep(self.multiplier * 1)

            for index, review in enumerate(reviews, start=0):
                reviews[index]['position'] = index + 1
        except:
            pass
        finally:
            return reviews


    def get_product(self) -> dict:
        product_data = {
            'product': self.get_product_info(),
            'reviews': self.get_product_reviews()
        }

        return product_data


    def save_to_json(self, data) -> None:
        with open(f'ebay_product_{self.product_id}.json', 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=2, ensure_ascii=False)


    @staticmethod
    def print(data) -> None:
        """Prints pretty JSON instead of regular print()"""
        print(json.dumps(data, indent=2, ensure_ascii=False))

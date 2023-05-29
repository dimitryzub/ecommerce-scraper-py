from .currencies import currencies
from .languages import languages
from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selectolax.lexbor import LexborHTMLParser
import json, re, time


class AmazonParams(object):
    def __init__(self, currency: str, language: str) -> None:
        self.currency = currency
        self.language = language


    @staticmethod
    def get_currencies() -> list:
        return currencies


    @staticmethod
    def get_languages() -> list:
        return languages


    def _validate_params(self):
        selected_currency = next(
            (el['code'] for el in currencies if
             el['code'].lower() == self.currency.lower() or el['text'].lower() == self.currency.lower()),
            None
        )
        if self.currency and not selected_currency:
            raise ValueError(
                'Please select available currency (use "AmazonParams.get_currencies()" to get all currencies list).')

        selected_language = next(
            (el['code'] for el in languages if
             el['code'].lower() == self.language.lower() or el['text'].lower() == self.language.lower()),
            None
        )
        if self.language and not selected_language:
            raise ValueError(
                'Please select available language (use "AmazonParams.get_languages()" to get all languages list).')

        return selected_currency, selected_language


class AmazonSearch(AmazonParams):
    def __init__(self,
                 query: str,
                 results_limit: int = 10,
                 multiplier: float = 1.0,
                 currency: str = '',
                 language: str = '',
                 price_from: float = 0,
                 price_to: float = 0,
                 customer_reviews_rating: int = 0) -> None:
        super().__init__(currency, language)
        self.query = query
        self.results_limit = results_limit
        self.multiplier = multiplier
        self.price_from = price_from
        self.price_to = price_to
        self.customer_reviews_rating = customer_reviews_rating
        self.currency, self.language = self._validate_params()
        self.driver = self.__get_browser_instance()


    def __del__(self):
        self.driver.quit()


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

        url = f'https://www.amazon.com/s?k={self.query}'

        if self.language:
            url += f'&language={self.language}'

        if self.price_from != 0 or self.price_to != 0:
            if self.price_from > self.price_to or self.price_from < 0 or self.price_to < 0:
                raise ValueError('Please set correct price arguments.')
            url += f'&rh=p_36:{self.price_from}00-{self.price_to or 0}00'

        rating_number = int(self.customer_reviews_rating)

        if rating_number:
            if not rating_number or rating_number < 1 or rating_number > 4:
                raise Exception('Please set "customer_reviews_rating" argument from 1 to 4.')

        driver.get(url)
        WebDriverWait(driver, 10000).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '.s-result-item:not(.a-section, .s-widget)'))
        )

        if self.currency:
            try:
                driver.find_element(By.CSS_SELECTOR, '#icp-touch-link-cop').click()
                time.sleep(self.multiplier * 2)
                driver.find_element(By.CSS_SELECTOR, '#icp-currency-dropdown-selected-item-prompt').click()
                time.sleep(self.multiplier * 2)
                driver.find_element(By.CSS_SELECTOR, f'#{self.currency} a').click()
                time.sleep(self.multiplier * 2)
                driver.find_element(By.CSS_SELECTOR, '#icp-save-button').click()
                time.sleep(self.multiplier * 2)
                WebDriverWait(driver, 10000).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, '#reviewsRefinements'))
                )
            except:
                print('Error in currency')

        if self.customer_reviews_rating:
            selector_number = None

            if rating_number == 1:
                selector_number = 4
            elif rating_number == 2:
                selector_number = 3
            elif rating_number == 3:
                selector_number = 2
            elif rating_number == 4:
                selector_number = 1

            try:
                driver.find_element(By.CSS_SELECTOR, f'#reviewsRefinements ul > span:nth-child({selector_number})').click()
                time.sleep(self.multiplier * 1)
                WebDriverWait(driver, 10000).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, '.s-result-item:not(.a-section, .s-widget)'))
                )
            except:
                print('Error in customer reviews rating')

        return driver

    def get_products(self) -> list:
        products = []

        try:
            while True:
                time.sleep(self.multiplier * 1)

                parser = LexborHTMLParser(self.driver.page_source)

                for product in parser.root.css('.s-result-item:not(.a-section, .s-widget)'):
                    title = product.css_first('h2').text(strip=True)
                    raw_subtitle = product.css_first('h2 + div')
                    subtitle = raw_subtitle.text(strip=True).replace('·', ' ') if raw_subtitle else None
                    raw_link = product.css_first('h2 a').attributes.get('href')
                    link = f'https://www.amazon.com{raw_link}'
                    raw_thumbnail = product.css_first('[data-component-type="s-product-image"] img')
                    thumbnail_srcset = raw_thumbnail.attributes.get('srcset') if raw_thumbnail else None
                    thumbnail = thumbnail_srcset.split(' ')[-2] if thumbnail_srcset else raw_thumbnail.attributes.get('src')
                    raw_badge = product.css_first('[data-component-type="s-status-badge-component"] .a-badge-text')
                    badge = raw_badge.text(strip=True) if raw_badge else None
                    raw_rating = product.css_first('.s-product-image-container + div > div:nth-child(2) span:first-child, .s-list-col-right > div > div > div:nth-child(2) > div > span:first-child')
                    raw_rating_attribute = raw_rating.attributes.get('aria-label') if raw_rating else None
                    rating = float(raw_rating_attribute.split(" ")[0]) if raw_rating_attribute else None
                    raw_reviews = product.css_first('.s-product-image-container + div > div:nth-child(2) > div > span:last-child, .s-list-col-right > div > div > div:nth-child(2) > div > span:last-child')
                    reviews = int(raw_reviews.text(strip=True).replace(',', '').replace('.', '')) if raw_reviews else None
                    raw_listing_history = product.css_first('.s-product-image-container + div > div:nth-child(2) > div:nth-child(2), .s-list-col-right > div > div > div:nth-child(2) > div:nth-child(2) > span')
                    listing_history = raw_listing_history.text(strip=True) if raw_listing_history else None
                    raw_options = product.css_first('.a-truncate-cut')
                    options = raw_options.text(strip=True) if raw_options else None
                    raw_additional_info = product.css_first('.s-product-image-container + div > div:nth-child(4) span.a-size-base, .s-list-col-right > div > div > div:nth-child(3) .a-section:nth-child(2)')
                    additional_info = raw_additional_info.text(strip=True) if raw_additional_info else None
                    raw_price = product.css_first('.s-product-image-container + div > div:nth-child(3) .a-price .a-offscreen, .s-list-col-right > div > div > div:nth-child(3) a .a-price .a-offscreen')
                    price = raw_price.text(strip=True) if raw_price else None

                    products.append({
                        'title': title,
                        'subtitle': subtitle,
                        'link': link,
                        'thumbnail': thumbnail,
                        'badge': badge,
                        'rating': rating,
                        'reviews': reviews,
                        'listing_history': listing_history,
                        'options': options,
                        'additional_info': additional_info,
                        'price': price,
                    })

                if len(products) >= self.results_limit:
                    products = products[:self.results_limit]
                    break

                try:
                    self.driver.find_element(By.CSS_SELECTOR, '.s-pagination-next:not(.s-pagination-disabled)').click()
                    time.sleep(self.multiplier * 1)
                    WebDriverWait(self.driver, 10000).until(
                        EC.visibility_of_element_located((By.CSS_SELECTOR, '.s-result-item:not(.a-section, .s-widget)'))
                    )
                    time.sleep(self.multiplier * 3)
                except:
                    print('Error in pagination')

            for index, product in enumerate(products, start=0):
                products[index]['position'] = index + 1
        except:
            print('Error in getting the product')
        finally:
            return products


    def save_to_json(self, data) -> None:
        with open(f'amazon_search_{self.query.lower().replace(" ", "_")}.json', 'w',
                  encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=2, ensure_ascii=False)


    @staticmethod
    def print(data) -> None:
        """Prints pretty JSON instead of regular print()"""
        print(json.dumps(data, indent=2, ensure_ascii=False))


class AmazonProduct(AmazonParams):
    def __init__(self,
                 link: str,
                 reviews_limit: int = 10,
                 multiplier: float = 1.0,
                 currency: str = '',
                 language: str = '',) -> None:
        super().__init__(currency, language)
        self.link = link
        self.reviews_limit = reviews_limit
        self.multiplier = multiplier
        self.currency, self.language = self._validate_params()
        self.driver = self.__get_browser_instance()
        self.product_name = self.__get_product_name()


    def __del__(self):
        self.driver.quit()


    def __get_product_name(self):
        # https://regex101.com/r/27NCcr/1
        product_name = re.search(r'amazon\.com/(.+)/dp', self.link).group(1)

        return product_name


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

        if self.language:
            driver.get(self.link + f'&language={self.language}')
        else:
            driver.get(self.link)

        WebDriverWait(driver, 10000).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'span#productTitle'))
        )

        if self.currency:
            try:
                driver.find_element(By.CSS_SELECTOR, '#icp-touch-link-cop').click()
                time.sleep(self.multiplier * 2)
                driver.find_element(By.CSS_SELECTOR, '#icp-currency-dropdown-selected-item-prompt').click()
                time.sleep(self.multiplier * 2)
                driver.find_element(By.CSS_SELECTOR, f'#{self.currency} a').click()
                time.sleep(self.multiplier * 2)
                driver.find_element(By.CSS_SELECTOR, '#icp-save-button').click()
                time.sleep(self.multiplier * 2)
                WebDriverWait(driver, 10000).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, 'span#productTitle'))
                )
            except:
                print('Error in currency')

        return driver


    def get_product_info(self) -> dict:
        parser = LexborHTMLParser(self.driver.page_source)

        raw_title = parser.root.css_first('span#productTitle')
        title = raw_title.text(strip=True) if raw_title else None

        raw_badge = parser.root.css_first('#acBadge_feature_div span > span')
        badge = raw_badge.text(strip=True) if raw_badge else None

        overview = {}
        for element in parser.root.css('#productOverview_feature_div tr'):
            key = element.css_first('td:first-child').text(strip=True).lower().replace(' ', '_')
            value = element.css_first('td:last-child').text(strip=True)
            overview[key] = value

        features = [
            element.text(strip=True)
            for element in parser.css('#featurebullets_feature_div li')
        ] if parser.css_first('#featurebullets_feature_div li') else None

        information = {}
        for element in parser.root.css('#productDetails_feature_div tr, #detailBulletsWrapper_feature_div li'):
            raw_key = element.css_first('th') if element.css_first('th') else element.css_first('.a-text-bold')
            key = raw_key.text().split('\n')[0].strip().lower().replace(' ', '_') if raw_key else None
            raw_value = element.css_first('td') if element.css_first('td') else element.css_first('.a-list-item span:last-child')
            value = raw_value.text(strip=True) if raw_value else None

            if str(key) in 'best_sellers_rank':
                if element.css_first('td'):
                    value = [el.text(strip=True) for el in element.css('td span span')]
                else:
                    raw_value = element.css_first('span.a-list-item').text(strip=True).split('#')
                    value = ['#' + el for el in raw_value[1:len(raw_value)]]
            elif str(key) in 'customer_reviews':
                continue

            if key is not None:
                information[key] = value

        raw_description = parser.root.css_first("#productDescription span")
        description = raw_description.text(strip=True) if raw_description else None

        raw_rating = parser.root.css_first('span#acrPopover')
        rating = float(
            raw_rating.attributes.get('aria-label').split()[0]
            if raw_rating.attributes.get('aria-label') else
            raw_rating.attributes.get('title').split()[0]
        ) if raw_rating else None

        raw_reviews = parser.root.css_first('#acrCustomerReviewLink')
        reviews = int(raw_reviews.text(strip=True).split(' ')[0].replace(',', '').replace('.', '')) if raw_reviews else None

        data = {
            'title': title,
            'link': self.link,
            'badge': badge,
            'overview': overview,
            'features': features,
            'information': information,
            'description': description,
            'buying_options': [],
            'by_feature': {},
            'rating': rating,
            'reviews': reviews,
        }

        return data


    def get_by_feature(self) -> dict:
        by_feature = {}

        try:
            self.driver.find_element(By.CSS_SELECTOR, 'body').send_keys(Keys.END)
            time.sleep(self.multiplier * 1)

            for i in range(10):
                self.driver.find_element(By.CSS_SELECTOR, 'body').send_keys(Keys.PAGE_UP)
                time.sleep(self.multiplier * 0.5)

            parser = LexborHTMLParser(self.driver.page_source)

            for element in parser.root.css('#cr-summarization-attributes-list > div'):
                key = element.css_first('.a-col-left').text(strip=True).lower().replace(' ', '_')
                value = float(element.css_first('i > span').text(strip=True))
                by_feature[key] = value
        except:
            print('Error in by feature')
        finally:
            return by_feature


    def get_buying_options(self) -> list:
        buying_options = []

        try:
            self.driver.find_element(By.CSS_SELECTOR, '#buybox-see-all-buying-choices').click()
            time.sleep(self.multiplier * 2)

            parser = LexborHTMLParser(self.driver.page_source)

            for element in parser.root.css('#aod-offer-list > div'):
                raw_condition = element.css_first('#aod-offer-heading h5')
                condition = raw_condition.text(strip=True).replace('\n', '') if raw_condition else None
                raw_price = element.css_first('.a-price .a-offscreen')
                price = raw_price.text(strip=True) if raw_price else None
                delivery_block = element.css_first('#mir-layout-DELIVERY_BLOCK')
                delivery = {
                    'date': delivery_block.css_first('span > span').text(strip=True),
                    'price': delivery_block.css_first('span').text(strip=True).split()[0]
                } if delivery_block else None
                raw_ships_from = element.css_first('#aod-offer-shipsFrom .aod-ships-from-country')
                ships_from = raw_ships_from.text(strip=True) if raw_ships_from else None
                raw_seller = element.css_first('#aod-offer-soldBy a')
                seller = raw_seller.text(strip=True) if raw_seller else None
                seller_link = 'https://www.amazon.com' + raw_seller.attributes.get('href') if raw_seller else None
                raw_seller_rating = element.css_first('#aod-offer-seller-rating')
                seller_rating = raw_seller_rating.text(strip=True) if raw_seller_rating else None
                sold_by = {
                    'seller': seller,
                    'seller_link': seller_link,
                    'seller_rating': seller_rating
                } if raw_seller else None

                buying_options.append({
                    'condition': condition,
                    'price': price,
                    'delivery': delivery,
                    'shipsFrom': ships_from,
                    'soldBy': sold_by
                })

            self.driver.find_element(By.CSS_SELECTOR, '#aod-close').click()
            time.sleep(self.multiplier * 1)
        except:
            print('Error in buying options')
        finally:
            return buying_options


    def get_product_reviews(self) -> list:
        reviews = []

        try:
            self.driver.execute_script('document.querySelector(\'[data-hook="see-all-reviews-link-foot"]\').click()')
            time.sleep(self.multiplier * 1)

            while True:
                self.driver.find_element(By.CSS_SELECTOR, 'body').send_keys(Keys.END)
                time.sleep(self.multiplier * 1)

                parser = LexborHTMLParser(self.driver.page_source)

                for element in parser.css('[data-hook="review"]'):
                    raw_name = element.css_first('.a-profile-name')
                    name = raw_name.text(strip=True) if raw_name else None
                    raw_avatar = element.css_first('.a-profile-avatar > img')
                    avatar = raw_avatar.attributes.get('src') if raw_avatar else None
                    raw_rating = element.css_first('i > span')
                    rating = float(raw_rating.text(strip=True).split(' ')[0]) if raw_rating else None
                    raw_heading = element.css_first('[data-hook="review-title"]')
                    heading = raw_heading.text(strip=True) if raw_heading else None
                    raw_date = element.css_first('[data-hook="review-date"]')
                    date = raw_date.text(strip=True).split(' on ')[-1] if raw_date else None
                    raw_badge = element.css_first('[data-hook="avp-badge"]')
                    badge = raw_badge.text(strip=True) if raw_badge else None
                    raw_review = element.css_first('[data-hook="review-body"]')
                    review = raw_review.text(strip=True) if raw_review else None

                    reviews.append({
                        'name': name,
                        'avatar': avatar,
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
                    self.driver.find_element(By.CSS_SELECTOR, '.a-pagination > li:last-child:not(.a-disabled)').click()
                    time.sleep(self.multiplier * 1)
                    self.driver.find_element(By.CSS_SELECTOR, '[data-hook="review"]')
                except:
                    break

            self.driver.find_element(By.CSS_SELECTOR, '#cm_cr-footer_dp_link .a-link-normal').click()
            time.sleep(self.multiplier * 1)

            for index, review in enumerate(reviews, start=0):
                review['position'] = index + 1
        except:
            print('Error in product reviews')
        finally:
            return reviews


    def get_product(self) -> dict:
        product = self.get_product_info()
        product['by_feature'] = self.get_by_feature()
        product['buying_options'] = self.get_buying_options()

        reviews = self.get_product_reviews()

        product_data = {
            'product': product,
            'reviews': reviews
        }

        return product_data


    def save_to_json(self, data) -> None:
        with open(f'amazon_product_{self.product_name.lower().replace("-", "_")}.json', 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=2, ensure_ascii=False)


    @staticmethod
    def print(data) -> None:
        """Prints pretty JSON instead of regular print()"""
        print(json.dumps(data, indent=2, ensure_ascii=False))

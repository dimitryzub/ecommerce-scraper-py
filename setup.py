from setuptools import setup, find_packages

README = ''
with open('README.md', 'r', encoding='utf-8') as readme_file:
    README = readme_file.read()

setup(
    name='ecommerce-scraper-py',
    description = 'Scrape ecommerce websites such as Amazon, eBay, Walmart, Home Depot, Google Shopping from a single module in Python🐍',
    url='https://github.com/dimitryzub/ecommerce-scraper-py',
    version='0.1.1',
    license='MIT',
    author='Artur Chukhrai',
    author_email='chukhraiartur@gmail.com',
    maintainer='Artur Chukhrai, Dmitiry Zub',
    maintainer_email='chukhraiartur@gmail.com, dimitryzub@gmail.com',
    long_description_content_type='text/markdown',
    long_description=README,
    include_package_data=True,
    python_requires='>=3.8',
    packages=find_packages(),
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS',
        'Operating System :: POSIX :: Linux',
        'Topic :: Internet',
        'Natural Language :: English',
        'Topic :: Utilities',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        "License :: OSI Approved :: MIT License"
    ],
    keywords=[
        'amazon',
        'ebay',
        'home depot',
        'walmart',
        'google shopping',
        'serpapi',
        'scraper',
        'python',
        'ecommerce',
        'e-commerce',
        'web scraping',
        'python web scraping',
        'google-search-results'
    ],
    install_requires=[
        'google-search-results>=2.4',
        'selenium>=4.3',
        'selectolax>=0.3',
        'webdriver-manager>=3.8',
        'selenium-stealth>=1.0'
    ],
    project_urls={
        'Documentation': 'https://github.com/dimitryzub/ecommerce-scraper-py',
        'Source': 'https://github.com/dimitryzub/ecommerce-scraper-py',
        'Tracker': 'https://github.com/dimitryzub/ecommerce-scraper-py/issues',
    }
)
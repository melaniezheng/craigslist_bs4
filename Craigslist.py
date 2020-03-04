from listings import Listing
from Scraper import CraiglistScraper
import re


def feature_urls(boro, url):
    result=[]
    dog_allowed_url = url + "&pets_dog=1"
    cat_allowed_url = url + "&pets_cat=1"
    no_fee_url = url + "&broker_fee=1"
    scraper = CraiglistScraper(boro, url)

    dog_allowed_url_lst = scraper.generate_url_lst(dog_allowed_url)
    dogs_ok_listings = set()
    for dogs_allowed_url in dog_allowed_url_lst:
        dogs_ok_listings.update(scraper.filter_ok_listings(dogs_allowed_url))

    cat_allowed_url_lst = scraper.generate_url_lst(cat_allowed_url)
    cats_ok_listings = set()
    for cat_allowed_url in cat_allowed_url_lst:
        cats_ok_listings.update(scraper.filter_ok_listings(cat_allowed_url))

    no_fee_url_lst = scraper.generate_url_lst(no_fee_url)
    no_fee_listings = set()
    for no_fee_url in no_fee_url_lst:
        no_fee_listings.update(scraper.filter_ok_listings(no_fee_url))

    result.append(scraper)
    result.append(dogs_ok_listings)
    result.append(cats_ok_listings)
    result.append(no_fee_listings)
    return result

min_price = "500"
max_price = "7000"
min_bedrooms = "0"
max_bedrooms = "5"
location = "newyork"
boro = "mnh"

url0 = f"https://{location}.craigslist.org/search/{boro}/apa?&min_price={min_price}&max_price={max_price}&min_bedrooms={min_bedrooms}&max_bedrooms={max_bedrooms}"
scraper = CraiglistScraper(boro, url0)
mnh_hood = scraper.get_nyc_neighborhoods(url0)

all_posts=[]
for neighborhood in mnh_hood: 
    url = url0 + "&" + mnh_hood[neighborhood]
    scraper, dogs_ok_listings, cats_ok_listings, no_fee_listings = feature_urls(boro, url)
    url_lst = scraper.generate_url_lst(url)
    for url in url_lst:
        all_posts.extend(scraper.extract_nyc_posts(url, neighborhood, dogs_ok_listings, cats_ok_listings, no_fee_listings))
scraper.write_to_tsv(all_posts,location,IsNYC=True)


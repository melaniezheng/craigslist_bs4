from listings import Listing
from Scraper import CraiglistScraper
import re


# add phoenix - cph evl nph wvl, sandiego - csd nsd esd ssd

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
# scraper = CraiglistScraper(boro, url0)
# mnh_hood = scraper.get_nyc_neighborhoods(url0)
# to save time
mnh_hood = {'Battery Park': 'nh_120', 'Chelsea': 'nh_134', 'Chinatown / Lit Italy': 'nh_160', 'Downtown': 'nh_121', 'East Harlem': 'nh_159', 'East Village': 'nh_129', 'Financial District': 'nh_122', 'Flatiron': 'nh_133', 'Gramercy': 'nh_132', 'Greenwich Village': 'nh_127', 'Harlem / Morningside': 'nh_141', 'Inwood / Wash Hts': 'nh_140', 'Lower East Side': 'nh_126', 'Midtown': 'nh_135', 'Midtown East': 'nh_136', 'Midtown West': 'nh_137', 'Murray Hill': 'nh_131', 'Nolita / Bowery': 'nh_125', 'SoHo': 'nh_124', 'TriBeCa': 'nh_123', 'Union Square': 'nh_130', 'Upper East Side': 'nh_139', 'Upper West Side': 'nh_138', 'West Village': 'nh_128'}

all_posts=[]
for neighborhood in mnh_hood: #neighborhood, id
    url = url0 + "&" + mnh_hood[neighborhood]
    scraper, dogs_ok_listings, cats_ok_listings, no_fee_listings = feature_urls(boro, url)
    url_lst = scraper.generate_url_lst(url)
    for url in url_lst:
        all_posts.extend(scraper.extract_nyc_posts(url, neighborhood, dogs_ok_listings, cats_ok_listings, no_fee_listings))
scraper.write_to_tsv(all_posts,location,IsNYC=True)


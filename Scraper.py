from datetime import datetime
from bs4 import BeautifulSoup
import urllib.request
import csv
import re

from listings import Listing

class CraiglistScraper(object):
    def __init__(self, boro, url, dogs_ok = 0, cats_ok = 1, no_broker_fee = 0):
        self.boro = boro
        self.url = url
        self.dogs_ok = dogs_ok
        self.cats_ok = cats_ok
        self.no_broker_fee = no_broker_fee
  

    def generate_url_lst(self, url):
        html_page = urllib.request.urlopen(url)
        soup = BeautifulSoup(html_page, "lxml")
        pages = soup.find("span", {"class": "totalcount"}).text
        url_lst = []
        pages = int(pages)
        for page in range(0, pages, 120):
            page = str(page)
            url_pp = url + "&s=" + page
            url_lst.append(url_pp)  # generate url list
        return url_lst

    
    def filter_ok_listings(self, url):
        html_page = urllib.request.urlopen(url)
        soup = BeautifulSoup(html_page, "lxml")
        filter_ok_listings=set()
        for result in soup.findAll("p", {"class": "result-info"}):
            try:
                url = result.find("a", {"class": "result-title hdrlnk"})
                url = url["href"]
            except:
                continue
            filter_ok_listings.add(url)
        return filter_ok_listings
    
    
    def get_nyc_neighborhoods(self, url):
        html_page = urllib.request.urlopen(url)
        soup = BeautifulSoup(html_page, "lxml")
        mnh_hood={}
        result=soup.find("div", {"class": "search-attribute"})
        for li in result.findAll("li"):
            try:
                hood = li.find('label').text
                hood = hood.strip()
            except Exception as e:
                print(f"Error occured: {e}")
            try:
                v = li.find("input")
                v = v["id"]
            except:
                print(f"Error occured: Can't find NYC neighborhood ID {hood}")
            mnh_hood[hood] = v
        return mnh_hood

    
    def extract_posts(self, url, dogs_ok_listings, cats_ok_listings, no_fee_listings):
        html_page = urllib.request.urlopen(url)
        soup = BeautifulSoup(html_page, "lxml")
        count = 0
        single_page_result=[]
        for result in soup.findAll("li", {"class": "result-row"}):
            count = count + 1
            try:
                url = result.find("a", {"class": "result-title hdrlnk"})
                url = url["href"]
            except:
                continue
            try:
                listing_id = result["data-pid"]
            except:
                listing_id = ""
            try:
                repost_of = result["data-repost-of"]
            except:
                repost_of = ""
            try:
                post_date = result.find("time", {"class": "result-date"})
                post_date = post_date["datetime"]
            except:
                post_date = ""
            try: 
                title = result.find('a').string
            except:
                title = ""
            try:
                price = result.find('span', {'class':'result-price'}).string
            except:
                price = ""
            try:
                neighborhood = result.find('span', {'class':'result-hood'}).string.strip()
            except:
                neighborhood = ""
            try:
                bedrooms = result.find('span', {'class':'housing'}).text
            except:
                bedrooms = ""
            if url in cats_ok_listings:
                cats_ok = "1"
            else:
                cats_ok = "0"
            if url in dogs_ok_listings:
                dogs_ok = "1"
            else:
                dogs_ok = "0"
            if url in no_fee_listings:
                no_fee = "1"
            else:
                no_fee = "0"
            listing = Listing(url, listing_id, repost_of, title, post_date, self.boro, neighborhood, price, bedrooms, cats_ok, dogs_ok, no_fee)
            single_page_result.append(listing.__repr__())    
        return single_page_result

    
    def extract_nyc_posts(self, url, neighborhood, dogs_ok_listings, cats_ok_listings, no_fee_listings):
        html_page = urllib.request.urlopen(url)
        soup = BeautifulSoup(html_page, "lxml")
        count = 0
        single_page_result=[]
        for result in soup.findAll("li", {"class": "result-row"}):
            count = count + 1
            try:
                url = result.find("a", {"class": "result-title hdrlnk"})
                url = url["href"]
            except:
                continue
            try:
                listing_id = result["data-pid"]
            except:
                listing_id = ""
            try:
                repost_of = result["data-repost-of"]
            except:
                repost_of = ""
            try:
                post_date = result.find("time", {"class": "result-date"})
                post_date = post_date["datetime"]
            except:
                post_date = ""
            try: 
                title = result.find('a').string
            except:
                title = ""
            try:
                price = result.find('span', {'class':'result-price'}).string
            except:
                price = ""
            try:
                bedrooms = result.find('span', {'class':'housing'}).string
            except:
                bedrooms = ""
            try:
                housing = result.find('span', {'class':'housing'}).string.split("-")
                if len(housing)>1:
                    bedrooms = housing[0]
                    size = housing[1]
            except:
                size = ""
            if url in cats_ok_listings:
                cats_ok = "1"
            else:
                cats_ok = "0"
            if url in dogs_ok_listings:
                dogs_ok = "1"
            else:
                dogs_ok = "0"
            if url in no_fee_listings:
                no_fee = "1"
            else:
                no_fee = "0"
            listing = Listing(url, listing_id, repost_of, title, post_date, self.boro, neighborhood, price, size, bedrooms, cats_ok, dogs_ok, no_fee)
            single_page_result.append(listing.__repr__())
        return single_page_result

    def write_to_tsv(self, all_posts, location, IsNYC = False):
        now = datetime.now()
        file_date = now.strftime("%Y-%m-%d")
        if IsNYC == False:
            filepath = "./data/" + location + "_"+ file_date + "_" + self.boro + ".tsv"
        else:
            filepath = "./data/" + "NYC"+ file_date + "_Manhattan" + ".tsv"
        fieldnames = ['url','listing_id','repost_of','title','date','boro','neighborhood','price','size','bedrooms','cats_allowed','dogs_allowed', 'no_fee']
        try:
            with open(filepath, "w") as output_file:
                dict_writer = csv.DictWriter(output_file, fieldnames=fieldnames, delimiter='\t')
                dict_writer.writeheader()
                dict_writer.writerows(all_posts)  
        except ValueError:
            print("Problem writing to tsv file")

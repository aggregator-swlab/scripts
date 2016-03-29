#! /usr/bin/env python
import sys
import subprocess
import json
from pprint import pprint

from bs4 import BeautifulSoup
import requests
import sys
import re
import urllib2

flip_id = sys.argv[1]

print type(flip_id)

all_sites_final = list()

# link_url = "https://affiliate-api.flipkart.net/affiliate/product/json?id=" + flip_id;
f = open("flipkart_id_result", "w")
process = subprocess.call(['curl',  '-H', 'Fk-Affiliate-Id:shariffaz', '-H', 'Fk-Affiliate-Token:c569d5da22704c278e90af8226c42174', "https://affiliate-api.flipkart.net/affiliate/product/json?id=" + flip_id], stdout=f)

with open('flipkart_id_result') as data_file:
	data = json.load(data_file)

fliptitle = data['productBaseInfo']['productAttributes']['title'];
flipdesc = data['productBaseInfo']['productAttributes']['productDescription'];
flipimgurl = data['productBaseInfo']['productAttributes']['imageUrls']['200x200'];
flipmrp = data['productBaseInfo']['productAttributes']['maximumRetailPrice']['amount'];
flipsp = data['productBaseInfo']['productAttributes']['sellingPrice']['amount'];
flipurl = data['productBaseInfo']['productAttributes']['productUrl'];

#flipkart array
flipkart_prod = dict()

flipkart_prod['server'] = "FLIPKART"
flipkart_prod['title'] = fliptitle
flipkart_prod['price'] = flipsp
flipkart_prod['imgurl'] = flipimgurl
flipkart_prod['url'] = flipurl
flipkart_prod['rating'] = "NA"

all_sites_final.append(flipkart_prod)

temptitle = flipkart_prod['title']
title = temptitle.replace(" ","+")
price = flipkart_prod['price']
flipkart_price = int(price)


#amazon array
amazon_minimum = 100000000
url = "http://www.amazon.in/s/ref=nb_sb_noss_2/278-5943722-6241930?url=search-alias%3Daps&field-keywords=" + title
page = urllib2.urlopen(url)
soupe = BeautifulSoup(page, "html.parser")
amazon_all_links = soupe.find_all("li", class_="s-result-item celwidget")

final_amazon_prod = dict()

for i in amazon_all_links:
	amazon_prod = dict()
	try:
		title = i.select('h2.a-text-normal')[0].string
	except:
		title = "NA"
	try:
		price = i.select('div.a-row div.a-span7 div.a-spacing-none a.a-text-normal span')[0].text.encode("utf-8")
	except:
		price = "NA"
	try:
		link = i.select('div.a-col-right div.a-spacing-small a.a-text-normal')[0].get("href")
	except:
		link = "NA"
	try:
		imgurl = i.select('div.a-row div.a-text-center a.a-text-normal img')[0].get("src")
	except:
		imgurl = "NA"
	try:
		rating = i.select('a.a-popover-trigger span.a-icon-alt')[0].text
		if rating.endswith(" out of 5 stars"):
			rating = rating[:-15]
	except:
		rating = "NA"

	amazon_prod['server'] = "AMAZON"
	amazon_prod['title'] = title
	amazon_prod['imgurl'] = imgurl
	amazon_prod['price'] = price
	amazon_prod['url'] = link
	amazon_prod['rating'] = rating

	try:
		amazon_price = price.decode('utf8')
		amazon_price = amazon_price.replace(",","")
		amazon_price = amazon_price.strip()
		amazon_price = int(float(amazon_price))
		if(abs(amazon_price - flipkart_price) < amazon_minimum):
			final_amazon_prod['server'] = "AMAZON"
			final_amazon_prod['title'] = title
			final_amazon_prod['imgurl'] = imgurl
			final_amazon_prod['price'] = price
			final_amazon_prod['url'] = link
			final_amazon_prod['rating'] = rating + " / 5"
			amazon_minimum = abs(amazon_price - flipkart_price)
	except:
		qqq = 1

all_sites_final.append(final_amazon_prod)

#snapdeal array
snapdeal_minimum = 100000000
title = temptitle.replace(" ","%20")
url = "http://www.snapdeal.com/search?keyword=" + title + "&noOfResults=48&sort=rlvncy"
page = urllib2.urlopen(url)
soupe = BeautifulSoup(page, "html.parser")
all_links = soupe.find_all("div", class_="col-xs-6 product-tuple-listing js-tuple ")

final_snapdeal_prod = dict()

for i in all_links:
	snapdeal_prod = dict()
	try:
		title = i.select('p.product-title')[0].string
	except:
		title = "NA"
	try:
		mrp = i.select('span.product-desc-price.strike')[0].string
	except:
		mrp = "NA"
	try:
		sp = i.select('span.product-price')[0].string
	except:
		sp = "NA"
	try:
		link = i.select('div.product-tuple-image a')[0].get("href")
	except:
		link = "NA"
	try:
		imgurl = i.select('div.product-tuple-image img')[0].get("src")
		if imgurl == None:
			imgurl = i.select('div.product-tuple-image img')[0].get("lazysrc")
	except:
		imgurl = "NA"
	try:
		rating = i.select('div.filled-stars')[0].get("style")[6:8]
	except:
		rating = "NA"

	snapdeal_prod['server'] = "SNAPDEAL"
	snapdeal_prod['title'] = title
	snapdeal_prod['imgurl'] = imgurl
	snapdeal_prod['price'] = sp
	snapdeal_prod['url'] = link
	snapdeal_prod['rating'] = rating

	try:
		snapdeal_price = sp[4:]
		snapdeal_price = snapdeal_price.replace(",","")
		snapdeal_price = snapdeal_price.strip()
		snapdeal_price = int(float(snapdeal_price))
		if(abs(snapdeal_price - flipkart_price) < snapdeal_minimum):
			final_snapdeal_prod['server'] = "SNAPDEAL"
			final_snapdeal_prod['title'] = title
			final_snapdeal_prod['imgurl'] = imgurl
			final_snapdeal_prod['price'] = sp
			final_snapdeal_prod['url'] = link
			final_snapdeal_prod['rating'] = rating + " / 100"
			snapdeal_minimum = abs(snapdeal_price - flipkart_price)
		# all_sites_final.append(snapdeal_prod)
	except:
		qqq = 1

all_sites_final.append(final_snapdeal_prod)

#ebay array

ebay_minimum = 100000000
title = temptitle.replace(" ","+")
url = "http://www.ebay.in/sch/i.html?_nkw=" + title
page = urllib2.urlopen(url)
soupe = BeautifulSoup(page, "html.parser")
all_links = soupe.find_all("li", class_="sresult lvresult clearfix li")

final_ebay_prod = dict()

for i in all_links:
	ebay_prod = dict()
    	try:
        		title = i.select('h3.lvtitle a.vip')[0].text.encode("utf-8").strip()
    	except:
        		title = "NA"
    	try:
        		mrp = i.select('li.lvprice span.bold')[0].text.encode("utf-8").strip()
    	except:
        		mrp = "NA"
    	try:
        		link = i.select('h3.lvtitle a.vip')[0].get("href")
    	except:
        		link = "NA"
    	try:
        		imgurl = i.select('img.img')[0].get("src")
    	except:
        		imgurl = "NA"

	ebay_prod['title'] = title
	ebay_prod['imgurl'] = imgurl
	ebay_prod['price'] = mrp
	ebay_prod['url'] = link
	ebay_prod['rating'] = "NA"

	try:
		ebay_price = mrp[4:]
		ebay_price = ebay_price.replace(",","")
		ebay_price = ebay_price.strip()
		ebay_price = int(float(ebay_price))
		if(abs(ebay_price - flipkart_price) < ebay_minimum):
			final_ebay_prod['server'] = "EBAY"
			final_ebay_prod['title'] = title
			final_ebay_prod['imgurl'] = imgurl
			final_ebay_prod['price'] = mrp
			final_ebay_prod['url'] = link
			final_ebay_prod['rating'] = "NA"
			ebay_minimum = abs(ebay_price - flipkart_price)
	except:
		qqq = 1

all_sites_final.append(final_ebay_prod)

print all_sites_final
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import re
import json
import math
import pandas as pd
import datetime
import requests
import urllib.request
import urllib.error
import urllib.parse
import requests
from bs4 import BeautifulSoup

import requests


headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
}

# create lists for wanted data
keys = ['title', 'longitude', 'latitude']
postdate = []
title = []
longitude = []
latitude = []

# create list for search start numbers
search_start_count = list(range(1, 140, 10))

def get_search_url(start_date, end_date, page_num):
    search_url = "https://search.naver.com/search.naver?where=review&query=%ED%99%8D%EB%8C%80%20%EC%B9%B4%ED%8E%98&sm=tab_opt&nso=so%3Ar%2Cp%3Afrom" + str(start_date) + "to" + str(end_date) + "%2Ca%3Aall&start=" + str(page_num)
    return search_url


def get_blog_post_url(search_url):
    get_blog_post_content_code = requests.get(search_url, headers=headers)
    get_blog_post_content_text = get_blog_post_content_code.text
    get_blog_post_content_soup = BeautifulSoup(get_blog_post_content_text, 'lxml')

    blog_url_list = []

    for li in get_blog_post_content_soup.find_all(class_="review_thumb"):
        blog_url_list.append(li.a.get('href'))

    return blog_url_list

def get_map_data(blog_url_list):
    for blog_url in blog_url_list:
        get_blog_post_content_code = requests.get(blog_url)
        get_blog_post_content_text = get_blog_post_content_code.text
        get_blog_post_content_soup = BeautifulSoup(get_blog_post_content_text, 'lxml')

        for link in get_blog_post_content_soup.select('frame#mainFrame'):
            real_blog_post_url = "http://blog.naver.com" + link.get('src')

            get_real_blog_post_content_code = requests.get(real_blog_post_url)
            get_real_blog_post_content_text = get_real_blog_post_content_code.text

            get_real_blog_post_content_soup = BeautifulSoup(get_real_blog_post_content_text, 'lxml')

            # Get map data
            blog_post_content = get_real_blog_post_content_soup.select('.se_caption_group.is-contact > a')

            # exception handling
            if not blog_post_content:
                mappoition = {"title":"None", "longitude":"0", "latitude":"0"}
                mappoition = json.dumps(mappoition)
            else:
                for contents in blog_post_content:
                    mappoition = contents.get('data-linkdata', None)

            # map data to json
            mapposition = json.loads(mappoition)

            # Add to lists by key
            key_num = 1
            for key in keys:
                if key_num == 1:
                    title.append(mapposition[key])
                elif key_num == 2:
                    longitude.append(mapposition[key])
                else:
                    latitude.append(mapposition[key])

                key_num = key_num+1


if __name__ == '__main__':
    for post_num in search_start_count:
        search_url = get_search_url(20180630, 20180101,post_num)
        blog_url_list = get_blog_post_url(search_url)
        get_map_data(blog_url_list)

    # create dataframe for final data storage
    data = {'title':title, 'longitude':longitude, 'latitude':latitude}
    post_geo_data = pd.DataFrame(data)

    # Drop empty columns
    post_geo_data = post_geo_data[post_geo_data.title != 'None']
    # print(post_geo_data.head(5))

    # Export csv file
    post_geo_data.to_csv("mapdata_web.csv", mode='w')

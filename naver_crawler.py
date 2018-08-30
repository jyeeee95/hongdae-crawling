import requests
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
import itertools
from bs4 import BeautifulSoup
from geo import *
# from get_mapdata import *


headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
}

# create lists for wanted data
keys = ['title', 'longitude', 'latitude']

blog_url_list = []
title = []
longitude = []
latitude = []

# create list for search start numbers
search_start_count = list(range(1, 1000, 10))

def get_search_url(start_date, end_date, page_num):
    search_url = "https://search.naver.com/search.naver?date_from=" + str(start_date) + "&date_option=8&date_to=" + str(end_date) + "&dup_remove=1&nso=p%3Afrom" + str(start_date) + "to" + str(end_date) + "&post_blogurl=&post_blogurl_without=&query=%ED%99%8D%EB%8C%80%20%EC%B9%B4%ED%8E%98&sm=tab_pge&srchby=all&st=sim&where=post&start=" + str(page_num)
    return search_url


def get_blog_post_url(search_url):
    get_blog_post_content_code = requests.get(search_url, headers=headers)
    get_blog_post_content_text = get_blog_post_content_code.text
    get_blog_post_content_soup = BeautifulSoup(get_blog_post_content_text, 'lxml')

    blog_url_list_draft = []
    blog_url_list = []

    for li in get_blog_post_content_soup.find_all(class_="thumb thumb-rollover"):
        blog_url_list_draft.append(li.a.get('href'))

    for url_ad_temp in blog_url_list_draft:
        url_ad = url_ad_temp.replace("?Redirect=Log&logNo=", "/")
        blog_url_list.append(url_ad)

    return blog_url_list


def get_map_data_up_ver(blog_url):
    get_blog_post_content_code = requests.get(blog_url)
    get_blog_post_content_text = get_blog_post_content_code.text
    get_blog_post_content_soup = BeautifulSoup(get_blog_post_content_text, 'lxml')

    for link in get_blog_post_content_soup.select('frame#mainFrame'):
        real_blog_post_url = "http://blog.naver.com" + link.get('src')

        # # Invalid link filtering
        # response_code = urllib.request.urlopen(real_blog_post_url).getcode()
        #
        # if response_code is 200:
        get_real_blog_post_content_code = requests.get(real_blog_post_url)
        get_real_blog_post_content_text = get_real_blog_post_content_code.text

        get_real_blog_post_content_soup = BeautifulSoup(get_real_blog_post_content_text, 'lxml')

        # Get map data
        blog_post_content = get_real_blog_post_content_soup.select('.se_caption_group.is-contact > a')

        # exception handling
        if not blog_post_content:
            pass
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


def get_map_data_down_ver(blog_url):
    get_blog_post_content_code = requests.get(blog_url)
    get_blog_post_content_text = get_blog_post_content_code.text
    get_blog_post_content_soup = BeautifulSoup(get_blog_post_content_text, 'lxml')

    for link in get_blog_post_content_soup.select('frame#mainFrame'):
        step2_blog_post_url = "http://blog.naver.com" + link.get('src')
        # print("step2_blog_post_url : " + step2_blog_post_url)

        get_step2_blog_post_content_code = requests.get(step2_blog_post_url)
        get_step2_blog_post_content_text = get_step2_blog_post_content_code.text

        get_step2_blog_post_content_soup = BeautifulSoup(get_step2_blog_post_content_text, 'lxml')

        for link in get_step2_blog_post_content_soup.select('#postViewArea iframe'):
            real_blog_post_url = link.get('src')

            # # Invalid link filtering
            # response_code = urllib.request.urlopen(real_blog_post_url).getcode()
            #
            # if response_code is 200:
            get_real_blog_post_content_code = requests.get(real_blog_post_url)
            get_real_blog_post_content_text = get_real_blog_post_content_code.text

            get_real_blog_post_content_soup = BeautifulSoup(get_real_blog_post_content_text, 'lxml')

            # Get map data
            blog_script_list = get_real_blog_post_content_soup.select('script')
            blog_script = str(blog_script_list[-2])
            blog_script = blog_script.replace("\\", "")
            pattern = re.compile("\\\"(\w+)\\\":\"(.*?)\"")
            map_dict = dict(re.findall(pattern, blog_script))
            # print(type(map_dict))
            # print(map_dict['centerX'])

            if not map_dict:
                pass
            else:
                longitude_data = map_dict['centerX']
                latitude_data = map_dict['centerY']

                title.append(map_dict['title'])
                longitude.append(longitude_data)
                latitude.append(latitude_data)


if __name__ == '__main__':
    for post_num in search_start_count:
        search_url = get_search_url(20121001, 20121231, post_num)
        blog_url_list.append(get_blog_post_url(search_url))

    blog_url_list = list(itertools.chain.from_iterable(blog_url_list))

    for blog_url in blog_url_list:
        try:
            get_map_data_down_ver(blog_url)
            get_map_data_up_ver(blog_url)
        except:
            pass


    # create dataframe for final data storage
    data = {'title':title, 'longitude':longitude, 'latitude':latitude}
    post_geo_data = pd.DataFrame(data)

    # Check data frames
    print(post_geo_data.head(20))

    # Export csv file
    post_geo_data.to_csv("all_mapdata_2012_4.csv", mode='w')

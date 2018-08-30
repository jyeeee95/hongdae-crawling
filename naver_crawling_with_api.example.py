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
from auth import *

# import api client info
naver_client_id = "QrFzh~~~"
naver_client_secret = "A9~~~"

# create lists for wanted data
keys = ['title', 'longitude', 'latitude']
postdate = []
title = []
longitude = []
latitude = []

# create list for search start numbers
search_start_count = list(range(1, 1000, 100))

# Get response dict
def get_response_dict(keyword, display_count, search_result_blog_page_count, sort_type):
    encText = urllib.parse.quote(keyword)

    url = "https://openapi.naver.com/v1/search/blog?query=" + encText + "&display=" + str(
        display_count) + "&start=" + str(search_result_blog_page_count) + "&sort=" + sort_type

    request = urllib.request.Request(url)

    request.add_header("X-Naver-Client-Id", naver_client_id)
    request.add_header("X-Naver-Client-Secret", naver_client_secret)

    response = urllib.request.urlopen(request)
    response_code = response.getcode()

    if response_code is 200:
        response_body = response.read()
        response_body_dict = json.loads(response_body.decode('utf-8'))

    return response_body_dict, display_count, search_result_blog_page_count, sort_type


# Get total posts
def get_blog_search_result_pagination_count(response_body_dict):
    blog_pagination_total_count = response_body_dict['total']

    # print total posts
    print('total posts : ' + str(blog_pagination_total_count))

    return blog_pagination_total_count



# Get blog posts
def get_blog_post(response_body_dict):
    for i in range(0, len(response_body_dict['items'])):
        try:
            blog_post_url = response_body_dict['items'][i]['link'].replace("amp;", "")

            get_blog_post_content_code = requests.get(blog_post_url)
            get_blog_post_content_text = get_blog_post_content_code.text
            get_blog_post_content_soup = BeautifulSoup(get_blog_post_content_text, 'lxml')

            for link in get_blog_post_content_soup.select('frame#mainFrame'):
                real_blog_post_url = "http://blog.naver.com" + link.get('src')

                get_real_blog_post_content_code = requests.get(real_blog_post_url)
                get_real_blog_post_content_text = get_real_blog_post_content_code.text

                get_real_blog_post_content_soup = BeautifulSoup(get_real_blog_post_content_text, 'lxml')


                # Get post creation date
                date = get_real_blog_post_content_soup.select('div.blog2_container > span.se_publishDate.pcol2')[0].text
                postdate.append(date)


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

        except:
            i += 1



if __name__ == '__main__':
    # import keyword: 홍대 카페
    for k in search_start_count:
        response_body_dict, display_count, search_result_blog_page_count, sort_type = get_response_dict("홍대 카페", 100, k, 'date')
        print(search_result_blog_page_count)

        get_blog_search_result_pagination_count(response_body_dict)
        get_blog_post(response_body_dict)

    # create dataframe for final data storage
    data = {'postdate': postdate, 'title':title, 'longitude':longitude, 'latitude':latitude}
    post_geo_data = pd.DataFrame(data)

    # Drop empty columns
    post_geo_data = post_geo_data[post_geo_data.title != 'None']
    print(post_geo_data.head(5))

    # Export csv file
    post_geo_data.to_csv("mapdata_sample.csv", mode='w')

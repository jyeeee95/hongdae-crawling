# hongdae-crawling

데잇걸즈 E조의 중간프로젝트를 위해 진행된 네이버 블로그 포스트의 지도 데이터 크롤링을 위한 코드입니다.
네이버 블로그 포스트 내에 있는 지도 데이터(신, 구 버전)를 모두 크롤링할 수 있습니다.

<br>

## 파일 설명

1. naver_crawler.py
   - 본 프로젝트에 사용된 최종 코드입니다. 네이버 블로그의 구, 신버전의 에디터 내 지도 데이터를 모두 크롤링할 수 있습니다.
2. naver_blog_crawler.py
   - 네이버의 최근 버전의 블로그 데이터만을 크롤링할 수 있습니다
3. naver_review_crawler.py
   - 네이버의 리뷰 포스트(네이버 지도와 연관되어 각 업체의 리뷰로 분류됨) 데이터만을 크롤링할 수 있습니다
4. naver_crawling_wiht_api.py
   - api를 활용한 블로그 포스트 크롤러입니다. 본 코드는 지도 데이터를 크롤링하지는 않습니다.
   - naver_client_id 와 naver_client_secret 에 본인이 받은 애플리케이션 정보를 입력해주세요. 애플리케이션 등록은 [Naver Developers](https://developers.naver.com/main/)에서 할 수 있습니다.
5. geo.py
   - 네이버가 가지고 있는 좌표계를 위경도로 바꾸는 함수입니다.
6. every_mapdata_to_wsg.py
   - geo 함수(자체)를 사용해 데이터의 좌표를 모두 위경도로 반환합니다.(현재 사용에 약간 어려움이 있습니다. 차후 수정이 진행될 예정입니다.)
7.  Mapping_data.ipynb
   - 프로젝트를 위해 만든 그래프 코드입니다.

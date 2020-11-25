import json
import re
import requests


class NewsApi:
    NEWS_API = 'https://focustaiwan.tw/cna2019api/cna/FTNewsList/'
    CATEGORY = ['politics', 'cross-strait', 'business', 'society', 'sports', 'sci-tech', 'culture', 'ad']
    CATEGORY_TAG = {
        'Politics': 'politics',
        'Cross-Strait': 'cross-strait',
        'Business': 'business',
        'Society': 'society',
        'Sports': 'sports',
        'Science & Tech': 'sci-tech',
        'Culture': 'culture',
        'Sponsored Content': 'ad'
    }

    @classmethod
    def get_all_news(cls, category):
        payload = {
            'action': 4,
            'category': category,
            'pagesize': 100
        }
        response = requests.post(url=cls.NEWS_API, data=payload).text
        data = json.loads(response)
        if data['Result'] == 'Y':
            news = data['ResultData']['Items']
            return news


REMOVE_AUTHOR = re.compile(r'<div class="author">.+<\\div>')
REMOVE_P_TAG = re.compile(r'(<p>)|(<\/p>)')


if __name__ == '__main__':
    NewsApi.get_all_news(category='politics')

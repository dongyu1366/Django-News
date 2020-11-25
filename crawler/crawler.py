from bs4 import BeautifulSoup
from queue import Queue
from tool import NewsApi, REMOVE_P_TAG
import json
import MySQLdb
import os
import sys
import threading
import re
import requests


class News:
    FOCUS_TAIWAN_DOMAIN = 'https://focustaiwan.tw'
    CATEGORY_LIST = ['politics', 'cross-strait', 'business', 'society', 'sports', 'sci-tech', 'culture', 'ad']

    @staticmethod
    def _fetch_news_list(category):
        payload = {
            'action': 4,
            'category': category,
            'pagesize': 100
        }
        response = requests.post(url=NewsApi.NEWS_API, data=payload).text
        data = json.loads(response)
        if data['Result'] == 'Y':
            news = data['ResultData']['Items']
            return news

    @classmethod
    def get_news_list(cls):
        for category in NewsApi.CATEGORY:
            news_list = cls._fetch_news_list(category=category)
            for news in news_list:
                token = news['Id']
                if not cur.execute(f'SELECT title FROM news_list WHERE token={token}'):
                    DbHandler.insert_list_to_db(news=news)
            print(f'News List: Completed get all news from {category}')

    @staticmethod
    def _fetch_news_content(q, url, sema):
        try:
            sema.acquire()
            response = requests.get(url=url)
            soup = BeautifulSoup(response.text, 'html.parser')
            div_area = soup.find('div', class_='PrimarySide')
            information = div_area.find('div', class_='Information')
            paragraph = div_area.find_all('div', class_='paragraph')

            token = (re.compile(r'(\/)(\d+)').search(url).group(2))
            category = information.find('a', class_='cate-col').text
            title = information.find('span', class_='h1t').text
            date = information.find('div', class_='updatetime').text
            if soup.find('div', class_='FullPic'):
                image = soup.find('div', class_='FullPic').find('img').get('src')
            else:
                image = None
            if paragraph[0].find('div', class_='author'):
                author = paragraph[0].find('div', class_='author').text
            else:
                author = None
            content = ''
            for para in paragraph:
                p_tags = para.find_all('p', recursive=False)
                for p in p_tags:
                    p = str(p)
                    p = re.sub(REMOVE_P_TAG, '\n', p)
                    content += p

            news_content = {
                'token': token,
                'category': category,
                'title': title,
                'author': author,
                'date': date,
                'image': image,
                'content': content
            }
            q.put(news_content)
            sema.release()
        except AttributeError as er:
            print(er, 'URL:', url)
            sema.release()

    @classmethod
    def _fetch_all_news_content(cls, category):
        cur.execute(f'SELECT url FROM news_list WHERE category=%s', (category,))
        url_list = cur.fetchall()
        url_list = [''.join(url) for url in url_list]
        news_contents = list()
        threads = list()
        max_threads = 30
        sema = threading.Semaphore(value=max_threads)
        q = Queue()
        for url in url_list:
            thread = threading.Thread(target=cls._fetch_news_content, args=(q, url, sema,))
            threads.append(thread)
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        count = 0
        while not q.empty():
            count += 1
            news_contents.append(q.get())
        print(f'Get {count} News from category {category}!')
        return news_contents

    @classmethod
    def get_news(cls):
        category_list = ['Politics', 'Cross-Strait', 'Business', 'Society', 'Sports', 'Science & Tech', 'Culture',
                         'Sponsored Content']
        for category in category_list:
            news_contents = cls._fetch_all_news_content(category=category)
            for news in news_contents:
                token = news['token']
                if not cur.execute(f'SELECT title FROM news WHERE token={token}'):
                    DbHandler.insert_news_to_db(news=news)

    @classmethod
    def run(cls):
        cls.get_news_list()
        cls.get_news()


class DbHandler:
    @classmethod
    def insert_list_to_db(cls, news):
        token = news['Id']
        category = news['ClassName']
        title = news['HeadLine']
        abstract = news['Abstract']
        date = news['CreateTime']
        image = news['Image']
        url = news['PageUrl']
        sql_i = "INSERT INTO news_list(token, category, title, abstract, date, image, url) \
                 VALUES(%s, %s, %s, %s, %s, %s, %s)"
        try:
            cur.execute(sql_i, (token, category, title, abstract, date, image, url))
            conn.commit()
        except MySQLdb.IntegrityError:
            pass

    @classmethod
    def insert_news_to_db(cls, news):
        token = news['token']
        category = news['category']
        title = news['title']
        author = news['author']
        date = news['date']
        image = news['image']
        content = news['content']
        sql_i = "INSERT INTO news(token, category, title, author, date, image, content) \
                 VALUES(%s, %s, %s, %s, %s, %s, %s)"
        try:
            cur.execute(sql_i, (token, category, title, author, date, image, content))
            conn.commit()
        except MySQLdb.IntegrityError:
            pass


if __name__ == '__main__':
    # Check for environment variable
    if not os.getenv("PASSWORD"):
        raise RuntimeError("PASSWORD is not set: export PASSWORD='your password'")

    # Connect to database
    try:
        conn = MySQLdb.connect(
            host='localhost',
            port=3306,
            user='root',
            passwd=os.getenv("PASSWORD"),
            db='news',
        )
    except MySQLdb.Error as e:
        print(e)
        sys.exit()

    cur = conn.cursor()

    News.run()

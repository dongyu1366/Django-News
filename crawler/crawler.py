from bs4 import BeautifulSoup
from datetime import datetime
from queue import Queue
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import ElementNotInteractableException
from .tool import CATEGORY_TAG, REMOVE_P_TAG
from time import sleep
import MySQLdb
import os
import sys
import threading
import re
import requests


class News:
    FOCUS_TAIWAN_DOMAIN = 'https://focustaiwan.tw'
    CATEGORY_LIST = ['politics', 'cross-strait', 'business', 'society', 'sports', 'sci-tech', 'culture', 'ad']

    def __init__(self):
        self.options = Options()
        self.options.add_argument("--disable-notifications")
        self.driver = webdriver.Chrome(chrome_options=self.options)

    def _initialize(self, url):
        self.driver.get(url=url)

        # Click privacy button
        try:
            privacy_button = self.driver.find_element_by_id('jsCloseGDPR')
            privacy_button.click()
        except ElementNotInteractableException:
            pass
        sleep(1)

    def _show_more_stories(self):
        """
        Get more stories button to load more news
        """
        more_stories = self.driver.find_element_by_id('jsListLoadMore')
        more_stories.click()
        sleep(1)

        try:
            self.driver.find_element_by_id('jsListLoadMore')
            self._show_more_stories()
        except ElementNotInteractableException:
            pass

    def _fetch_news_list(self, news_list):
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        div_area = soup.find('div', class_='PrimarySide')
        category = div_area.find('div', class_='Category').text
        ul_list = div_area.find('ul', id='jsList').find_all('li')
        for li in ul_list:
            try:
                url = li.a.get('href')
                url = f'{self.FOCUS_TAIWAN_DOMAIN}{url}'
                source_token = re.compile(r'(\/)(\d+)').search(url).group(2)
                title = li.find('div', class_='listInfo').h2.text
                abstract = li.find('div', class_='desc').text
                date_str = li.find('div', class_='date').text
                date = datetime.strptime(date_str, '%m/%d/%Y %I:%M %p')
                image = li.img.get('src')
                category_tag = CATEGORY_TAG[category]
                news_dict = {
                    'source_token': source_token,
                    'category': category,
                    'category_tag': category_tag,
                    'title': title,
                    'abstract': abstract,
                    'date_str': date_str,
                    'date': date,
                    'image': image,
                    'url': url
                }
                news_list.append(news_dict)
            except AttributeError:
                pass
        return news_list

    @staticmethod
    def _fetch_news_content(q, url, sema):
        try:
            sema.acquire()
            response = requests.get(url=url)
            soup = BeautifulSoup(response.text, 'html.parser')
            div_area = soup.find('div', class_='PrimarySide')
            information = div_area.find('div', class_='Information')
            paragraph = div_area.find_all('div', class_='paragraph')

            source_token = (re.compile(r'(\/)(\d+)').search(url).group(2))
            category = information.find('a', class_='cate-col').text
            title = information.find('span', class_='h1t').text
            date_str = information.find('div', class_='updatetime').text
            date = datetime.strptime(date_str, '%m/%d/%Y %I:%M %p')
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
                'source_token': source_token,
                'category': category,
                'title': title,
                'author': author,
                'date_str': date_str,
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

    def get_news_list(self):
        for category in self.CATEGORY_LIST:
            url = f'{self.FOCUS_TAIWAN_DOMAIN}/{category}'
            news_list = list()
            self._initialize(url=url)
            self._show_more_stories()
            news_list = self._fetch_news_list(news_list=news_list)
            for news in news_list:
                source_token = news['source_token']
                if not cur.execute(f'SELECT title FROM news_list WHERE source_token={source_token}'):
                    DbHandler.insert_list_to_db(news=news)
            print(f'Completed News list --- {len(news_list)} in  {category}!')
        self.driver.quit()

    @classmethod
    def get_news(cls):
        category_list = ['Politics', 'Cross-Strait', 'Business', 'Society', 'Sports', 'Science & Tech', 'Culture', 'AD']
        for category in category_list:
            news_contents = cls._fetch_all_news_content(category=category)
            for news in news_contents:
                source_token = news['source_token']
                if not cur.execute(f'SELECT title FROM news WHERE source_token={source_token}'):
                    DbHandler.insert_news_to_db(news=news)


class DbHandler:
    @classmethod
    def insert_list_to_db(cls, news):
        source_token = news['source_token']
        category = news['category']
        category_tag = news['category_tag']
        title = news['title']
        abstract = news['abstract']
        date_str = news['date_str']
        date = news['date']
        image = news['image']
        url = news['url']
        sql_i = "INSERT INTO news_list(source_token, category, category_tag, title, abstract, date_str, date, image, url) \
                 VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        try:
            cur.execute(sql_i, (source_token, category, category_tag, title, abstract, date_str, date, image, url))
            conn.commit()
        except MySQLdb.IntegrityError:
            pass

    @classmethod
    def insert_news_to_db(cls, news):
        source_token = news['source_token']
        category = news['category']
        title = news['title']
        author = news['author']
        date_str = news['date_str']
        date = news['date']
        image = news['image']
        content = news['content']
        sql_i = "INSERT INTO news(source_token, category, title, author, date_str, date, image, content) \
                 VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"
        try:
            cur.execute(sql_i, (source_token, category, title, author, date_str, date, image, content))
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
    a = News()
    a.get_news_list()
    sleep(5)
    News.get_news()

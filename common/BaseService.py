#-*-coding=utf-8-*-
import datetime
import os
import re
import requests
import parsel
from loguru import logger


class BaseService(object):

    def __init__(self, logfile='default.log'):
        self.logger = logger
        self.logger.add(logfile)
        self.init_const_data()

    def init_const_data(self):
        '''
        常见的数据初始化
        '''
        self.today = datetime.datetime.now().strftime('%Y-%m-%d')


    def check_path(self, path):
        if not os.path.exists(path):
            try:
                os.makedirs(path)
            except Exception as e:
                self.logger.error(e)

    def get_url_filename(self, url):
        return url.split('/')[-1]


    def save_iamge(self, content, path):
        with open(path, 'wb') as fp:
            fp.write(content)

    def get(self, _josn=False, binary=False, retry=5):

        start = 0
        while start < retry:

            try:
                r = requests.get(
                    url=self.url,
                    params=self.params,
                    headers=self.headers,
                    cookies=self.cookie)

            except Exception as e:
                start += 1
                continue

            else:
                if _josn:
                    result = r.json()
                elif binary:
                    result = r.content
                else:
                    result = r.text
                return result

        return None

    def post(self, post_data, _json=False, binary=False, retry=5):

        start = 0
        while start < retry:

            try:
                r = requests.post(
                    url=self.url,
                    headers=self.headers,
                    data=post_data
                )

            except Exception as e:
                start += 1
                continue

            else:
                if _json:
                    result = r.json()
                elif binary:
                    result = r.content
                else:
                    result = r.text
                return result

        return None

    def parse(self, content):
        '''
        页面解析
        '''
        response = parsel.Selector(text=content)

        return None

    def process(self, data, history=False):
        '''
        数据存储
        '''
        pass







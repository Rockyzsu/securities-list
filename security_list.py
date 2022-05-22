# -*- coding: utf-8 -*-
# @Time : 2022/4/24 22:24
# @File : security_list.py
# @Author : Rocky C@www.30daydo.com
import datetime

from common.BaseService import BaseService
from configure.settings import DBSelector

SECURITY_LIST_URL = 'https://jg.sac.net.cn/pages/publicity/resource!search.action'


class SecurityList(BaseService):
    def __init__(self):
        self.url = SECURITY_LIST_URL
        self.headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'jg.sac.net.cn',
            'Origin': 'https://jg.sac.net.cn',
            'Referer': 'https://jg.sac.net.cn/pages/publicity/securities-list.html',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
        }

        self.db = DBSelector().mongo('qq')

    def crawl(self):
        data = {
            'filter_EQS_O#otc_id': '01',
            'filter_EQS_O#sac_id': '',
            'filter_LIKES_aoi_name': '',
            'sqlkey': 'publicity',
            'sqlval': 'ORG_BY_TYPE_INFO',
        }
        ret_data = self.post(post_data=data, _json=True)

        return ret_data


    def parse(self, content):
        return content

    def dump_mongo(self,data_list):

        for item in data_list:
            item['crawltime'] = datetime.datetime.now()
            self.db['db_parker']['security_list'].insert_one(item)

    def run(self):
        content = self.crawl()
        content=self.parse(content)
        self.dump_mongo(content)


def main():
    app = SecurityList()
    app.run()


if __name__ == '__main__':
    main()

# -*- coding: utf-8 -*-
# @Time : 2022/4/24 22:48
# @File : branch_office.py
# @Author : Rocky C@www.30daydo.com
import datetime

from common.BaseService import BaseService
from configure.settings import DBSelector

BRANCH_URL = 'https://jg.sac.net.cn/pages/publicity/resource!list.action'


class BranchOffice(BaseService):

    def __init__(self):
        self.url = BRANCH_URL
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

    def crawl(self, _id,page):
        # page=1
        data = {
            "filter_LIKES_msdi_name": "",
            "filter_LIKES_msdi_reg_address": "",
            "filter_EQS_aoi_id": _id,
            "page.searchFileName": 'publicity',
            "page.sqlKey": 'PAG_SALES_DEPT',
            "page.sqlCKey": 'SIZE_SALES_DEPT',
            "_search": 'false',
            # "nd": 1650811369297,
            "page.pageSize": 100,
            "page.pageNo": page,
            "page.orderBy": 'MATO_UPDATE_DATE',
            "page.order": 'desc',
        }
        ret_data = self.post(post_data=data,_json=True)
        return ret_data

    def get_security_id(self):
        return self.db['db_parker']['security_list'].find({},{'AOI_ID':1})


    def run(self):
        for _id in self.get_security_id():
            _id = _id.get('AOI_ID')
            page = 1
            has_next = True
            while has_next:
                content = self.crawl(_id,page)
                self.dump_mongo(content,_id)
                totalPage = self.next_page(content)
                page+=1
                if page>totalPage:
                    has_next = False



    def dump_mongo(self,data,sec_id):
        for item in data['result']:
            item['crawltime']=datetime.datetime.now()
            item['AOI_ID'] = sec_id
            self.db['db_parker']['security_branch_office'].insert_one(item)


    def next_page(self,content):
        return content.get('totalPages')


def main():
    app = BranchOffice()
    app.run()

if __name__ == '__main__':
    main()

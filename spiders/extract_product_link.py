import json
from operator import index
from typing import Iterable, Any

from scrapy.cmdline import execute
import scrapy
from header_cookies import cookies,headers

class ExtractProductLinkSpider(scrapy.Spider):
    name = "extract_product_link"
    allowed_domains = ["boodmo.com"]
    start_urls = ["https://boodmo.com/"]

    def __init__(self):
        # Initialize initial value
        try:
            with open(rf"All_Category_Data.json",'r',encoding='Utf-8')as fp:
                self.all_pending_category=json.load(fp)
        except:
            self.logger.info(rf"Failed to read pending category...")

        self.headers=headers
        self.cookies=cookies
        try:
            with open(rf"All product Link.json","r",encoding='utf-8')as fp:
                self.aproduct_link=json.load(fp)
        except:
            self.product_link=[]



    def start_requests(self):
        #send request of each extracted category for fetch product link of each category
        for no,pending_category in enumerate(self.all_pending_category):
            if pending_category['Status']=='Pending':
                url='https://boodmo.com/api/v1/customer/api/catalog/part/list'
                params = {
                    'sort': 'new',
                    'page[offset]': '1',
                    'page[limit]': '48',
                    'filter[category]': rf'{pending_category['Category-III Id']}',
                    'filter[carMaker]': rf'{pending_category['Car Id']}',
                }

                query_string = "&".join([f"{k}={v}" for k, v in params.items()])
                full_url = f"{url}?{query_string}"

                yield scrapy.Request(
                    url=full_url,
                    headers=self.headers,
                    cookies=self.cookies,
                    meta={'Unique Id':pending_category['Unique Id'],'Index Id':no,'product_count':0,'page_no':1,'pending_category':pending_category},
                    callback=self.parse,
                )

                # break



    def parse(self, response,**kwargs):
        #Extract product link of each category
        if response.status==200:
            page_no=response.meta['page_no']
            product_count=response.meta['product_count']
            pending_category=response.meta['pending_category']
            json_dic=response.json()


            all_product=json_dic['items']

            for product in all_product:

                self.product_link.append({'Product Id':product['id'],'Status':'pending'})
                product_count+=1

            total_product=json_dic['list']['size']

            #Use pagination logic when product link can be available on more than 1 pages
            if total_product>product_count:
                page_no+=1

                url = 'https://boodmo.com/api/v1/customer/api/catalog/part/list'
                params = {
                    'sort': 'new',
                    'page[offset]': rf'{page_no}',
                    'page[limit]': '48',
                    'filter[category]': rf'{pending_category['Category-III Id']}',
                    'filter[carMaker]': rf'{pending_category['Car Id']}',
                }

                query_string = "&".join([f"{k}={v}" for k, v in params.items()])
                full_url = f"{url}?{query_string}"

                yield scrapy.Request(
                    url=full_url,
                    headers=self.headers,
                    cookies=self.cookies,
                    meta={'Unique Id': pending_category['Unique Id'], 'product_count': product_count, 'page_no': page_no,
                          'pending_category': pending_category,'Index Id':response.meta['Index Id']},
                    callback=self.parse,
                )
            else:
                with open(rf"All product Link.json",'w',encoding='utf-8')as fp:
                    json.dump(self.product_link,fp,indent=4,ensure_ascii=False)
                self.logger.info(rf"All data can be scraped....")

                index_no=response.meta['Index Id']

                if self.all_pending_category[index_no]['Unique Id']==response.meta['Unique Id']:
                    self.all_pending_category[index_no]['status']='Done'
                    with open(rf"All_Category_Data.json", "w", encoding='utf-8') as fp:
                        json.dump(self.all_pending_category, fp, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    execute(rf"scrapy crawl extract_product_link".split())

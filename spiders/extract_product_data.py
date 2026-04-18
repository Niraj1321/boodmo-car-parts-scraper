import json
import scrapy,requests
from scrapy.cmdline import execute
from header_cookies import headers,cookies
from scrapy.crawler import signals
import pandas as pd



class ExtractProductDataSpider(scrapy.Spider):
    name = "extract_product_data"
    allowed_domains = ["boodmo.com"]
    start_urls = ["https://boodmo.com/"]

    def __init__(self):
        self.headers=headers
        self.cookies=cookies

        try:
            with open(rf"All product Link.json","r",encoding='utf-8')as fp:
                self.all_pending_links=json.load(fp)
        except:
            self.logger.info(rf"Failed to load pending links...")

        try:
            with open(rf"Product Details.json","r",encoding='utf-8')as fp:
                self.all_product_details=json.load(fp)
        except Exception as e:
            self.all_product_details=[]

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super().from_crawler(crawler, *args, **kwargs)

        # Connect signals
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)

        return spider


    def start_requests(self):

        for no,pending_link in enumerate(self.all_pending_links):

            if pending_link['Status']=='pending':

                yield scrapy.Request(rf'https://boodmo.com/api/v1/customer/api/catalog/part/{pending_link['Product Id']}',
                                     cookies=self.cookies, headers=self.headers,
                                     meta={'Product Id':pending_link['Product Id'],"index_":no},
                                     callback=self.parse,
                                     dont_filter=True)
                # break



    def parse(self, response,**kwargs):
        if response.status==200:
            product_id=response.meta['Product Id']
            index_=response.meta['index_']
            json_dic=response.json()

            product_dic={}

            product_link=rf"https://boodmo.com/catalog/part-{json_dic['slug']}/"

            product_dic['Url']=product_link

            product_name=json_dic['name']

            product_dic['Product Name']=product_name

            part_number=json_dic['number']

            product_dic['Part Number'] = part_number

            image=rf"https://boodmo.com/media/cache/catalog_part/{json_dic['image']}"

            product_dic['Image']=image

            product_brand=json_dic['brand']['name']

            product_dic['Brand']=product_brand

            product_class=json_dic['family']['name']

            product_dic['Class']=product_class


            product_attributes=json_dic['attributes']

            for attribute in product_attributes:
                product_dic[attribute['name']]=attribute['value']

            description=json_dic['custom_attributes']['gmc_title']

            product_dic['Description']=description

            product_category=json_dic['categories']

            category_list=[]

            category_list.append({
                "Name":"Catalogues",
                "Url":"https://boodmo.com/catalog/"
            })

            for category in product_category:
                category_list.append({
                    "Name":category['name'],
                    "Url":rf"https://boodmo.com/catalog/{category['id']}-{category['slug']}/"
                })
            product_dic['Product category']=category_list

            product_dic=self.extrcat_product_offer(product_id,product_dic)

            self.all_product_details.append(product_dic)

            if self.all_pending_links[index_]['Product Id']==product_id:
                self.all_pending_links[index_]['Status']="Done"

            # self.save_data()

    def save_data(self):
        with open(rf"All product Link.json","w",encoding='utf-8')as fp:
            json.dump(self.all_pending_links,fp,ensure_ascii=False,indent=4)

        with open(rf"Product Details.json","w",encoding='utf-8')as fp:
            json.dump(self.all_product_details,fp,indent=4,ensure_ascii=False)

        df=pd.DataFrame(self.all_product_details)

        df.to_excel(rf"Product_details.xlsx",index=False,engine='openpyxl')

        self.logger.info(rf"File Generated Successfully...")

    def spider_closed(self, reason):
        self.save_data()



    def extrcat_product_offer(self,product_id,product_dic):
        params = {
            'filter[pin]': '380026',
        }

        response = requests.get(
            rf'https://boodmo.com/api/v1/customer/api/checkout/part-offers/{product_id}',
            params=params,
            cookies=self.cookies,
            headers=self.headers,
        )

        if response.status_code==200:
            json_dic=response.json()

            price=None

            offer_list=[]

            for offer in json_dic['items']:
                if not price:
                    price=offer['price']/100

                offer_list.append({
                    "Seller":offer['seller']['name'],
                    "Stock Quantity":offer['stockQuantity'],
                    "Price":offer['price']/100,
                    "Mrp":offer['mrpPrice']/100,
                    "Discount":rf"{offer['safePercent']}%",
                    "Delivery within":rf"{offer['deliveryLogisticDays']+offer['deliveryDispatchDays']}"
                })

            product_dic['Price']=price
            product_dic['Offer']=offer_list

            return product_dic






if __name__ == '__main__':
    execute(rf"scrapy crawl extract_product_data".split())

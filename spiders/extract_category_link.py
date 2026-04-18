import json
import hashlib
from header_cookies import cookies,headers
from scrapy.cmdline import execute
import scrapy,requests
from scrapy.crawler import signals


class ExtractCategoryLinkSpider(scrapy.Spider):
    name = "extract_category_link"
    allowed_domains = ["boodmo.com"]
    start_urls = ["https://boodmo.com/"]

    def __init__(self):
        # Initialize initial value

        self.cookies = cookies

        self.headers = headers

        self.all_category_list=[]

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        # Handle dynamically to manage breakdowns and ensure data is saved safely
        spider = super().from_crawler(crawler, *args, **kwargs)

        # Connect signals
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)

        return spider




    def start_requests(self):
        #send initial request to extract category of car parts
        yield  scrapy.Request('https://boodmo.com/api/v1/customer/api/catalog/category/list',
                              cookies=self.cookies,
                              headers=self.headers,
                              dont_filter=True,
                              callback=self.extract_category_level_1
                              )

    def extract_car_maker_list(self):
        # Extract list of car manufacturers to filter car parts based on brand (e.g., Audi)
        response = requests.get(
            'https://boodmo.com/api/v1/customer/api/catalog/vehicle/car-maker-list',
            cookies=self.cookies,
            headers=self.headers,
        )

        if response.status_code == 200:
            car_maker = []
            json_dic = response.json()
            car_maker_list = json_dic['items']

            for car_dic in car_maker_list:
                car_maker.append({'id': car_dic['id'], 'slug': car_dic['slug']})

            return  car_maker


    def extract_category_level_1(self, response,**kwargs):
        # Extract First category of car parts
        if response.status==200:
            car_maker_list = self.extract_car_maker_list()
            json_dic=response.json()

            category_list=json_dic['items']

            if category_list:


                for car_brand in car_maker_list:


                    # Send requests to fetch second-level categories for each extracted first-level category
                    for category in category_list:

                        url = "https://boodmo.com/api/v1/customer/api/catalog/aggregation/list"

                        params = {
                            'type': 'fulfilledByBoodmo,freeDelivery,carMaker,category,brand,family,origin,price,modelLine',
                            'pageType': 'category',
                            'filter[category]': rf'{category['id']}',
                            'filter[carMaker]': rf'{car_brand['id']}',
                        }

                        # Convert params to query string
                        query_string = "&".join([f"{k}={v}" for k, v in params.items()])
                        full_url = f"{url}?{query_string}"

                        yield scrapy.Request(
                            url=full_url,
                            headers=self.headers,
                            cookies=self.cookies,
                            meta={'category_id':category['id'],'category_name':category['name'],'car_id':car_brand['id'],'car_name':car_brand['slug']},
                            callback=self.extract_category_level_2,
                        )







    def extract_category_level_2(self,response,**kwargs):
        #Extract second level of category of each part
        if response.status==200:
            category_id=response.meta['category_id']
            car_id=response.meta['car_id']
            category_name=response.meta['category_name']
            car_name=response.meta['car_name']
            json_dic = response.json()

            sub_category_list = json_dic['category']

            if sub_category_list:

                for sub_category in sub_category_list:
                    if sub_category['parent_id']==category_id:
                        url = "https://boodmo.com/api/v1/customer/api/catalog/aggregation/list"

                        params = {
                            'type': 'fulfilledByBoodmo,freeDelivery,carMaker,category,brand,family,origin,price,modelLine',
                            'pageType': 'category',
                            'filter[category]': rf'{sub_category['id']}',
                            'filter[carMaker]': rf'{car_id}',
                        }

                        # Convert params to query string
                        query_string = "&".join([f"{k}={v}" for k, v in params.items()])
                        full_url = f"{url}?{query_string}"

                        yield scrapy.Request(
                            url=full_url,
                            headers=self.headers,
                            cookies=self.cookies,
                            meta={'category_id': category_id, 'category_name':category_name,
                                  'car_id': car_id, 'car_name': car_name,'subcategory_id':sub_category['id'],
                                  'subcategory_name':sub_category['name']},
                            callback=self.extract_category_level_3,
                        )
                        # break

    def generate_hash(self,url, key):
        # Generate a unique hash key to identify each category,
        # enabling tracking of extracted product links and ensuring successful scraping
        raw = f"{url}_{key}"
        return hashlib.sha256(raw.encode()).hexdigest()

    def extract_category_level_3(self,response,**kwargs):
        #Extract third level of category of each parts
        if response.status==200:
            subcategory_id=response.meta['subcategory_id']
            json_dic = response.json()

            final_category_list = json_dic['category']

            for final_category in final_category_list:
                if final_category['parent_id'] == subcategory_id:
                    hash_key=self.generate_hash(response.url,final_category['id'])
                    self.all_category_list.append({
                        "Unique Id":hash_key,
                        'Category-I Id':response.meta['category_id'],
                        'Category-I Name': response.meta['category_name'],
                        'Category-II Id':response.meta['subcategory_id'],
                        'Category-II Name': response.meta['subcategory_name'],
                        'Category-III Id':final_category['id'],
                        'Category-III Name': final_category['name'],
                        'Car Name':response.meta['car_name'],
                        'Car Id':response.meta['car_id'],
                        'Status':'Pending'
                    })

    def save_data(self):
        #Saved all extracted category Data
        with open(rf"All_Category_Data.json","w",encoding='utf-8')as fp:
            json.dump(self.all_category_list,fp,indent=4,ensure_ascii=False)

        self.logger.info(rf"All data can be saved successfully...")


    def spider_closed(self, reason):
        self.save_data()




if __name__ == '__main__':
    execute(rf"scrapy crawl extract_category_link".split())



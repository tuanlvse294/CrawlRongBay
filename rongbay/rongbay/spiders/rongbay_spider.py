import json
import os

import requests
import scrapy

BASE_URL = 'https://rongbay.com/Ha-Noi/Nha-rieng-Mua-Ban-nha-dat-c15-t4-trang{}.html'

BASE_CRAWL_DATA = '~/Projects/Timnha/crawl_data/'


class RongbaySpider(scrapy.Spider):
    name = 'rongbay'

    def start_requests(self):
        for i in range(1, 2):
            yield scrapy.Request(url=BASE_URL.format(i), callback=self.parse)

    def parse(self, response):
        for i in response.css('a[id^=ad_id]::attr(href)').getall():
            yield scrapy.Request(url=i, callback=self.parse_bds)

    def parse_bds(self, response):
        try:
            uid = response.css('.note_gera span::text')[2].get().strip()
            title = response.css('div .sub_detail_popup p.title::text').get().strip()
            price = response.css('.box_infor_ct li.icon_bds span::text')[0].get().strip()
            area = response.css('.box_infor_ct li.icon_bds span::text')[1].get().strip()
            content = ''.join(response.css('.info_text  *::text').extract())
            imgs = response.css('.info_box img::attr(src)').getall()
            imgs = [img.replace('/zoom,70/180_150', 'original') for img in imgs]
            address = response.css('.box_infor_ct .cl_666::text')[2].get().strip()
            print()
            print('----------------')
            print(uid)
            print(title)
            print(price)
            print(area)
            print(content)
            print(address)
            print(imgs)
            print('----------------')
            print()

            bds_dir = BASE_CRAWL_DATA + uid
            if not os.path.isdir(bds_dir):
                os.mkdir(bds_dir)
                os.mkdir(bds_dir + '/images')
                for img in imgs:
                    print('download ', img)
                    open(bds_dir + '/images/' + os.path.basename(img), 'wb').write(
                        requests.get(img).content)
                meta_data = {'uid': uid, 'title': title, 'price': price, 'area': area, 'content': content,
                             'address': address}
                open(bds_dir + '/metadata.json', 'w').write(json.dumps(meta_data))
        except:
            print('ERROR', response.url)

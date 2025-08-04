import pandas as pd
import scrapy
from bs4 import BeautifulSoup

class ProductImagSpider(scrapy.Spider):
    name = "product_imgs"
    all_data = []

    def start_requests(self):
        headers = {
            'authority': 'www.example.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'accept-language': 'en-US,en;q=0.9',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
            'upgrade-insecure-requests': '1',
        }
        
        cookies = {
            'session-id': '132-7281856-2392936',
            'session-id-time': '2082787201l',
            'ubid-main': '134-5337216-0122550',
            'i18n-prefs': 'USD',
            'lc-main': 'en_US',
            'sp-cdn': '"L5Z9:IN"',
        }

        urls = [
            "https://www.example.com/gp/product/078696555X",
            "https://www.example.com/gp/product/614847932X",
            "https://www.example.com/gp/product/B00000DMCE",
            "https://www.example.com/gp/product/B00000DMD2",
            "https://www.example.com/gp/product/B00000ISC5",
            "https://www.example.com/gp/product/B00000J50W",
            "https://www.example.com/gp/product/B0000224C9",
            "https://www.example.com/gp/product/B0000224SD",
            "https://www.example.com/gp/product/B00002N5N7",
            "https://www.example.com/gp/product/B00002N5V6",
            "https://www.example.com/gp/product/B00002N64X",
            "https://www.example.com/gp/product/B00002N7FP",
            "https://www.example.com/gp/product/B00002N8SO",
            "https://www.example.com/gp/product/B00002N8UC",
            "https://www.example.com/gp/product/B00002N9DQ",
            "https://www.example.com/gp/product/B00002NB84",
            "https://www.example.com/gp/product/B00002ND64",
            "https://www.example.com/gp/product/B00004C8S8",
            "https://www.example.com/gp/product/B00004R9TU",
            "https://www.example.com/gp/product/B00004R9TX",
            "https://www.example.com/gp/product/B00004R9W4",
            "https://www.example.com/gp/product/B00004RA2V",
            "https://www.example.com/gp/product/B00004RANZ",
            "https://www.example.com/gp/product/B00004RDF3",
            "https://www.example.com/gp/product/B00004RKCU",
            "https://www.example.com/gp/product/B00004RKD0",
            "https://www.example.com/gp/product/B00004S9D3",
            "https://www.example.com/gp/product/B00004T154",
            "https://www.example.com/gp/product/B00004T7P1",

        ]

        for url in urls:
            yield scrapy.Request(url=url, headers=headers, cookies=cookies, callback=self.parse,meta={'original_url': url})

    def parse(self, response):
        
        soup = BeautifulSoup(response.text, 'html.parser')
        thumbnail_ul = soup.find('ul', {
          'aria-label':'Image thumbnails'  
        })

        img_tags = thumbnail_ul.find_all('img') if thumbnail_ul else []
        img_urls = [img['src'] for img in img_tags if 'src' in img.attrs]

        product_img_urls = [
            url for url in img_urls
            if "transparent-pixel" not in url and url.endswith(('.jpg', '.jpeg', '.png'))
        ]

        item = {'Page URL': response.meta['original_url']}
        for i, img_url in enumerate(product_img_urls):
            item[f'image{i+1}'] = img_url

        self.all_data.append(item)

    def closed(self, reason):
        if self.all_data:
            df = pd.DataFrame(self.all_data)
            df.to_excel("output_images.xlsx", index=False)
            self.logger.info("Saved output_images.xlsx successfully.")     
       



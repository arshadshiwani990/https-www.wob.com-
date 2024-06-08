import scrapy
import re
import json
class WobSitemapSpider(scrapy.Spider):
    name = 'wob_sitemap_spider'
    start_urls = ['https://www.wob.com/sitemap/en-au/seo_friendly_sitemap.xml']

    custom_settings = {
        'FEEDS': {
            'wob_sitemap.csv': {
                'format': 'csv',
                'encoding': 'utf8',
                'overwrite': True,
             
            },
        },
    }

    def parse(self, response):
       
        links=re.findall('loc>(.+?products.+)<',response.text)
        for link in links:
            print(link)
            yield scrapy.Request(url=link, callback=self.scrape_product_links)
            

    def scrape_product_links(self,response):
        
        
        products_links=re.findall('loc>(.+\/\d+)',response.text)
        for product_link in products_links:
            yield scrapy.Request(url=product_link, callback=self.scrape_page)
     
        
    def scrape_page(self,response):
        
        
        data=response.xpath('//script[@type="application/ld+json"][contains(text(),"Product")]/text()').get()
        data=json.loads(data)
        
        isbn=data.get('sku')
        

        items=data.get('offers')
        for item in items:
            availability=item.get('availability')
            itemCondition=item.get('itemCondition')
            priceCurrency=item.get('priceCurrency')
            sku=item.get('sku')
            price=item.get('price')

            if 'InStock' in availability:
            
                availability=True
      
                result={}
                result['isbn']=isbn
                result['sku']=sku
                result['price']=price
                result['availability']=availability
                result['itemCondition']=itemCondition
                result['priceCurrency']=priceCurrency
                
                
                yield result
        
        
            
            
        
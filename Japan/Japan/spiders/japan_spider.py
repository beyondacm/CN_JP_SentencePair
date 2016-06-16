import scrapy
import re 

from scrapy.selector import Selector
# from posts.items import AnswerItem
# from posts.items import QuestionItem
from Japan.items import JapanItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.exceptions import CloseSpider


class JanpanSpider(scrapy.Spider):

    name = "japan"

    allowed_domains = ['http://cjjc.weblio.jp']
    
    ##############  This needs to change #####################
    urls = open('./urls/urls_20_34.txt')
    start_urls = [ url.strip() for url in urls.readlines() ] 
    urls.close() 

    # rules = (
    #     Rule(LinkExtractor(allow=r"/sentence/content/*"),
    #     callback = "parse_answer", follow = False),
    # )

    def parse(self, response):
           
        item =  JapanItem()
        self.get_cn(response, item)
        
        yield item 

    def get_cn(self, response, item):
        
        cns = response.xpath("//p[@class='qotCC']").extract()
        jps = response.xpath("//p[@class='qotCJ']").extract()
        
        ############   This needs to change ##################
        fout_cn = open("./cn_source/cn_20_34.txt", 'a')
        fout_jp = open("./jp_source/jp_20_34.txt", 'a')

        print len(cns), len(jps)
        
        for cn in cns :
            
            str_extract = str(cn.encode('utf-8'))
            str_extract = re.sub(r'\s+', ' ', str_extract) 
            print str_extract

            fout_cn.write( str_extract + '\n')


        for jp in jps :

            str_extract = str(jp.encode('utf-8'))
            str_extract = re.sub(r's\+', ' ', str_extract)
            print str_extract

            fout_jp.write( str_extract + '\n')

        fout_cn.close()
        fout_jp.close()

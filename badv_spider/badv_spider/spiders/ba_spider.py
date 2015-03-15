import re
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from badv_spider.items import BadvSpiderItem
from bs4 import BeautifulSoup


class BaSpider(CrawlSpider):
    name = "baspider"
    start_urls = [
        'http://www.google.com/search?q=cache:http://www.beeradvocate.com/beer/style/'
    ]
    rules = [
        Rule(LinkExtractor(allow=(r'beer/profile/\d+/\d+/', )), callback='parse_item'),
        Rule(LinkExtractor(allow=(r'beer/style/\d+/\?start=\d+')))
    ]

    def parse_item(self, response):
        self.log('item page: %s' % response.url)
        item = BadvSpiderItem()
        soup = BeautifulSoup(response.body)

        item['name'] = soup.find_all(
            "div",
            class_="titleBar"
        )[0].find_all("h1")[0].contents[0].string.strip()

        item['company'] = soup.find_all(
            "div",
            class_="titleBar"
        )[0].find_all(
            "h1"
        )[0].find_all("span")[0].contents[0].string.replace(" - ", "")

        item['score'] = soup.find_all(
            "span", class_="BAscore_big ba-score"
        )[0].string.strip()
        if item['score'] == "-":
            item['score'] = "0"

        # TODO: this is VERY bad, needs looking to be redone
        # done quick for the first iteration
        style_pattern = re.compile(r"/beer/style/\d+")
        location_pattern = re.compile(r"/place/directory/\d+/\w+")
        image_pattern = re.compile(r"/im/beers/\d+\.jpg")
        anchors = soup.find_all(
            "a", href=True
        )
        location_found = style_found = False
        for anchor in anchors:
            if location_found and style_found:
                break
            elif style_pattern.match(anchor['href']):
                poss_style = anchor.contents[0].string.strip()
                if poss_style != "View and learn more ...":
                    item['style'] = poss_style
            elif location_pattern.match(anchor['href']):  # doesn't get states
                item['location'] = anchor.contents[0].string.strip()

        images = soup.find_all(
            "img"
        )
        for image in images:
            if image_pattern.search(image['src']):
                item['image_url'] = image['src']
                break

        return item

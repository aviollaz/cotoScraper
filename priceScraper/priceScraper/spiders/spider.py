import scrapy
from priceScraper.items import cotoItem

class SpiderSpider(scrapy.Spider):
    name = "spider"
    allowed_domains = ["www.cotodigital3.com.ar"]
    start_urls = ["https://www.cotodigital3.com.ar/sitios/cdigi/browse/catalogo-almac%C3%A9n-golosinas-alfajores/_/N-1njwjm5"]

    curr_page = 1

    def parse(self, response):
        products = response.css('li[id^="li_prod"]')

        for product in products:
            

            product_id = product.attrib['id']
            description = product.css('div[id^="descrip_container_sku"]::text').get()
            price = product.css('span.atg_store_newPrice::text').get()

            # Clean the description and price fields
            description = description.strip() if description else None
            price = price.strip() if price else None

            # Save data in item
            coto_item = cotoItem()

            coto_item['product_id'] = product_id
            coto_item['description'] = description
            coto_item['price'] = price

            # Check if description is not available, and follow the product page link
            if not description:
                product_page_link = product.css('a::attr(href)').get()
                if product_page_link:
                    yield response.follow(product_page_link, callback=self.parse_product_page, meta={'coto_item': coto_item})
                else:
                    yield coto_item
            else:
                yield coto_item

        next_page_selector = f'li a[title="Ir a página {self.curr_page + 1}"]::attr(href)'

        next_page = response.css(next_page_selector).get()

        if next_page:
            next_page_link = 'https://www.cotodigital3.com.ar/' + next_page
            self.curr_page += 1
            yield response.follow(next_page_link, callback=self.parse)

    def parse_product_page(self, response):
        coto_item = response.meta['coto_item']
        description = response.css('div#productInfoContainer h1.product_page::text').get()

        # Clean the description field
        description = description.strip() if description else None

        coto_item['description'] = description
        yield coto_item

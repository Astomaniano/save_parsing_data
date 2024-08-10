import scrapy


class DivanDataSpider(scrapy.Spider):
    name = "divan_data"
    allowed_domains = ["divan.ru"]
    start_urls = ["https://www.divan.ru/category/divany-i-kresla/page-2"]

    def parse(self, response):
        # Извлечение данных с текущей страницы
        divans = response.css('div.LlPhw')
        for divan in divans:
            yield {
                'name': divan.css('div.lsooF span::text').get(),
                'price': divan.css('div.pY3d2 span::text').get(),
                'link': divan.css('a').attrib['href']
            }

        # Определение текущей страницы и построение URL следующей
        current_page = response.url.split('-')[-1]
        next_page_number = int(current_page) + 1
        next_page_url = f"https://www.divan.ru/category/divany-i-kresla/page-{next_page_number}"

        # Проверка существования следующей страницы

        yield scrapy.Request(url=next_page_url, callback=self.parse)
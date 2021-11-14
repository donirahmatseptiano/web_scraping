import requests, pprint, json
from scrapy import Selector

# function untuk mengambil source code page html
def request_page(url):
    response = requests.get(url)
    content = response.content

    return content

# function untuk mengambil setiap url dari masing-masing headline news
def detail_page(link):
    response = requests.get(link)
    page = response.content

    return page

# function untuk mengambil informasi berita 
def get_data(page):
    data = {}

    title = page.css('div.zox-post-head.zoxrel > h1 ::text').extract_first()
    data['title'] = title

    content =  page.css('div.zox-post-body.left.zoxrel.zox100 > p ::text').extract()
    content = "/".join(content) 
    data['content'] = content

    author = page.css('div.zox-author-name-wrap > span ::text').extract_first()
    data['author'] = author

    date_published = page.css('div.zox-post-date-wrap > span ::attr(datetime)').extract_first()
    data['date'] = date_published

    link = page.css('head > link ::attr(href)').extract_first()
    data['url_link'] = link

    return data


html_page = request_page('https://cleantechnica.com/')
html_sel = Selector(text=html_page)
pages = html_sel.css('.zox-art-title > a ::attr(href)').extract()

details = []

for page in pages:
    link_page = detail_page(page)
    link_page = Selector(text=link_page)
    data = get_data(link_page)
    details.append(data)

pp = pprint.PrettyPrinter(indent=2)

for detail in details:
  pp.pprint(detail)

with open("news2scrape.json", "w") as file:
  file.write(json.dumps(details))
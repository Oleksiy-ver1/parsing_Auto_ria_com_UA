import requests
from bs4 import BeautifulSoup # из bs4 вытаскиваем BeautifulSoup

URL="https://auto.ria.com/newauto/marka-nissan/" # адрес который будем парсить
HEADERS={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36', "accept":"*/*"}
#заголовки нужны чтоб сайт воспринемал нас как браузер, а не как бот
HOST ="https://auto.ria.com"

# params - переменная для передачи дополнительных параметров (номера страниц например)
s=0
def get_html(url, params=None):
    r=requests.get(url, headers=HEADERS, params=params)
    return r


def get_usd(item):
    s = item.find('div', {'class': 'proposition_price'}).get_text(strip=True).index('$') - 1
    usd = item.find('div', {'class': 'proposition_price'}).get_text(strip=True)[0:s]
    return usd


def get_uah(item):
    s1 = item.find('div', {'class': 'proposition_price'}).get_text(strip=True).index('$') +1
    s2 = item.find('div', {'class': 'proposition_price'}).get_text(strip=True).index('грн')
    uah=item.find('div', {'class': 'proposition_price'}).get_text(strip=True)[s1:s2].strip().replace('•','')
    return uah


def get_content(html):
    soup=BeautifulSoup(html, 'html.parser') # 'html.parser' - параметр указывающий, что разбераем html-формат
    # items=soup.findAll("h3", {"class": "proposition_name"})
    items=soup.findAll("div", {"class": "proposition_area"})
    cars=[] #создаем словарь с автомобилями
    for item in items:
        cars.append({
            # 'title': item.text.strip(' ')
            'title': item.find('h3', class_='proposition_name').get_text(strip=True),
            'link': HOST+item.find('a').get('href'),
            'price_usd':get_usd(item),
            'price_uah':get_uah(item),
            'city': item.find('svg', class_='svg svg-i16_pin').find_next('strong').get_text(strip=True),
        })
    return cars


def parse():
    html=get_html(URL)
    if html.status_code== 200:
        cars = get_content(html.text)
        print (cars)
    else:
        print ('ERROR')


parse()

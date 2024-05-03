import requests # подключение библиотеки для работы с http, необхадима предварительная установка
from bs4 import BeautifulSoup # подключение парсера для синтаксического разбора файлов html\xml, необходима предварительная установка
import csv

HOST = 'www.chitai-gorod.ru' # основная страница сайта который парсим
URL = 'https://www.chitai-gorod.ru/catalog/books/hudozhestvennaya-literatura-110001?page=' # конкретная страница откуда парсим
params = '&filters%5BonlyAvailableInCustomerCity%5D=1&filters%5BliteratureWorkPublishingYearsMin%5D=2020&filters%5BliteratureWorkPublishingYearsMax%5D=2023'
CSV = 'tasks.csv'   #Путь файла для сохранения.
HEADERS = {'accept': '*/*',
           'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Mobile Safari/537.36'}
#чтобы сайт не воспринимал программу ботом, нужно прописывать заголовки, информация из кода страницы
# Network - all - первая строка - заголовки user agent и accept

# ?filters%5BonlyAvailableInCustomerCity%5D=1&filters%5BliteratureWorkPublishingYearsMin%5D=2020&filters%5BliteratureWorkPublishingYearsMax%5D=2023

def get_html(url, params):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='product-card__text product-card__row')
    tasks = []

    for item in items:
        tasks.append(HOST + item.find('a', class_='product-card__title').get('href'))
    return tasks

def get_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='pagination__wrapper')
    pages = []
   

    for item in items:
        pages.append(
            {
                'page': item.find('span', class_='pagination__text').get_text(strip=True)
            }
        )

    # print(items)
    # print(pages)
    page_all = 3
    return page_all


def parser():
    html = get_html(URL, params={})
    if html.status_code == 200:
        #Количество страниц для парсинга.
        URL_page = URL + '1' + params
        html = get_html(URL_page, params={})
        page_all = get_page(html.text)

        #Получение ссылок на книги
        tasks = []
        for page in range(1, page_all+1):
            print(f'Парсим страницу: {page}')

            URL_page = URL + str(page) + params

            html = get_html(URL_page, params={})
            tasks.extend(get_content(html.text))

            print(tasks)
    else:
        print("Error")

parser()




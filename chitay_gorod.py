import requests # подключение библиотеки для работы с http, необхадима предварительная установка
from bs4 import BeautifulSoup # подключение парсера для синтаксического разбора файлов html\xml, необходима предварительная установка

HOST = 'https://www.chitai-gorod.ru' # основная страница сайта который парсим
HEADERS = {'accept': '*/*',
           'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Mobile Safari/537.36'}


def parser(URL, params):
    html = get_html(URL, params={})
    if html.status_code == 200:
        #Количество страниц для парсинга.
        # URL_page = URL + '1' + params
        # html = get_html(URL_page, params={})
        page_all = get_page(html.text)
        print(page_all)

        #Получение ссылок на книги
        url_book = []
        for page in range(1, page_all+1):
            #print(f'Парсим страницу: {page}')
            print(page, ' из ', page_all)
            URL_page = URL + str(page) + params

            html = get_html(URL_page, params={})
            url_book.extend(get_url_book(html.text))

            #print(url_book)

        #Получение информации о книгах
        books = []
        for book in url_book:
            #print(book)
            html = get_html(book, params={})
            books.extend(get_book(html.text))

            #print(books)
    else:
        print("Error")

    return books

#Загрузка страницы
def get_html(url, params):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

#Получение ссылок на книги
def get_url_book(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='product-card__text product-card__row')
    tasks = []

    for item in items:
        tasks.append(HOST + item.find('a', class_='product-card__title').get('href'))
    return tasks

#Получение количества страниц
def get_page(html):
    # soup = BeautifulSoup(html, 'html.parser')
    # items = soup.find_all('div', class_='pagination__button')
    # pages = []
    # for item in items:
    #     pages.append(
    #         {
    #             item.find('span', class_='pagination__text')
    #         }
    #     )
    # page_all = int(str(pages[-2])[41:44])
    page_all = 1
    return page_all

#Получение книг
def get_book(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='detail-product__wrapper')
    books = []
    for item in items:
        type_find = str(item.find_all('a', class_='product-breadcrumbs__link')).split('\n')[-2]
        type_find = ' '.join(type_find.split())

        #offer = item.find_all('a', class_='product-offer-shops__link')
        offer = item.find('div', 'product-offer-shops')

        #print(offer)

        try:
            isbn = item.find('span', itemprop='isbn').get_text(strip=True)
        except:
            isbn = ''
        try:
            status = item.find('svg', 'offer-availability-status--green offer-availability-status__icon')['alt']
        except:
            status = 'нет'

        books.append(
            {
                'book_title': item.find('h1', class_='detail-product__header-title').get_text(strip=True),
                'type': type_find,
                'autor': item.find('a', class_='product-info-authors__author').get_text(strip=True),
                'price': item.find('span', class_='product-offer-price__current product-offer-price__current--discount')['content'],
                'ID': item.find('span', class_='product-detail-features__item-value').get_text(strip=True),
                'publishing': item.find('a', class_='product-detail-features__item-value product-detail-features__item-value--link').get_text(strip=True),
                'year': item.find('span', itemprop='datePublished').get_text(strip=True),
                'isbn': isbn,
                'numberOfPages': item.find('span', itemprop='numberOfPages').get_text(strip=True),
                'size': item.find('span', itemprop='size').get_text(strip=True),
                'bookFormat': item.find('span', itemprop='bookFormat').get_text(strip=True),
                'circulation': 'не готово', #item.find('span', class_='product-detail-features__item-value').get_text(strip=True),
                'weight': 'не готово', #item.find('span', class_='product-detail-features__item-value').get_text(strip=True),
                'typicalAgeRange': 'не готово', # item.find('span', itemprop='typicalAgeRange').get_text(strip=True),
                'ratingValue': item.find('meta', itemprop='ratingValue')['content'],
                'reviewCount': item.find('meta', itemprop='reviewCount')['content'],
                'status': status,
                'offer': 'не готово', #offer,
                'description': item.find('article', class_='detail-description__text').get_text(strip=True)
            }
        )
        #print(books)
    
    return books







import chitay_gorod
import save


URL = [
    ['https://www.chitai-gorod.ru/catalog/books/hudozhestvennaya-literatura-110001?page=','&filters%5BonlyAvailableInCustomerCity%5D=1&filters%5BliteratureWorkPublishingYearsMin%5D=2020&filters%5BliteratureWorkPublishingYearsMax%5D=2023']
]

#print(URL[0][0])
#print(URL[0][1])

for url_page in range(0, 1):
    print('Всего страниц по', url_page + 1, 'ссылке: ', end='')
    books = chitay_gorod.parser(URL[url_page][0], URL[url_page][1])
    save.book_save(books)

#print(a)
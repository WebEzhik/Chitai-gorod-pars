





#try:
#    f = open(CSV)
#    f.close()
#except FileNotFoundError:
#    with open(CSV, 'w', newline='') as file:  # открытие файла для записи
#        writer = csv.writer(file,  delimiter=';')  # использование библиотеки csv с использованием в качестве разделителя ;
#        writer.writerow(
#            ['Дата парсинга', 'Время парсинга', 'Дата создания', 'Место погрузки', 'Место выгрузки', 'Культура', 'Объем, тонн',
#            'Расстояние, км', 'Цена, руб/кг', 'Номер зявки', 'Способо погрузки', 'Грузоподъемность весов на погрузке, тонн', 'Экспортер'])  # первая строка таблицы

#try:
#    f = open(DAT)
#    f.close()
#except FileNotFoundError:
#    with open(DAT, 'w', newline='') as file:  # открытие файла для записи
#        writer = csv.writer(file,  delimiter=';')  # использование библиотеки csv с использованием в качестве разделителя ;
#        writer.writerow(['Дата парсинга', 'Время парсинга', 'Название', 'Количество'])  # первая строка таблицы





respond = session.post(url_login, data=d, headers=HEADERS).text

def get_html(url, i, params=''):  # функция для получения html

    r = session.post(url, data=i, headers=HEADERS, params=params)  # запрос на считывание html
    return r

def get_content(html):  # функция для считывания данных

    soup = BeautifulSoup(html, 'html.parser')  # в переменную soup будут записываться данные со страницы
    # print(soup)
    items = soup.find_all('div', class_='old-tr rows oldRows panel panel-default')  # с кода страницы берем блок в котором хранятся нужные данные
    # print(items) #вывод элементов для проверки
    date = []  # справочник, куда будем сохранять нужные данные

    for item in items:
        tit = item.find('div', class_='panel-body nopadding phoneFormSearch')
        titles = tit.find_all('div', class_='form-group')
        s = titles[3].text

        if "Экспортер" in s:
            exporter = titles[3].find('div', class_='col-sm-8').get_text(strip=True)
        else:
            exporter = ""
        date.append({
            # в коде страницы ищем где находятся нужные данные и прописываем считывание в соответствующие переменные
            'data_soz': item.find('div', class_='date-td').get_text(strip=True)[5:],
            'pogruzka': item.find('div', class_='A-td').get_text(strip=True),
            'vygruzka': item.find('div', class_='B-td').get_text(strip=True),
            'product': item.find('div', class_='product-td').get_text(strip=True),
            'volume': item.find('div', class_='scope-td').get_text(strip=True),
            'distance': item.find('div', class_='distance-td').get_text(strip=True),
            'price': item.find('div', class_='price-td').get_text(strip=True).replace('.', ',')[:4],
            'nomer_zayavki': titles[0].find('span', class_='request-number').get_text(strip=True),
            'sposob_pogr': titles[1].find('div', class_='col-sm-8').get_text(strip=True),
            'gruzopod_vesov': titles[2].find('div', class_='col-sm-8').get_text(strip=True),
            'exporter': exporter
        })

    return date  # результат работы функции справочник date

def save_file(items):  # запись данных в файл
    db = MySQLdb.connect(charset='utf8',
                         init_command='SET NAMES UTF8',
                         host="kulakov-anton.ru",  # host
                         user="u1491686_pars1",  # логин
                         passwd="fP0lW5bE9ggA0u",  # пароль
                         db="u1491686_parser")  # имя базы данных

    cur = db.cursor()

    # Отправляем данные в базу данных
    for item in items:
        x1 = "INSERT INTO zernovoz VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}', '{9}', '{10}', '{11}', '{12}')".format(
            DAY,
            TIME,
            item['data_soz'],
            item['pogruzka'],
            item['vygruzka'],
            item['product'],
            item['volume'],
            item['distance'],
            item['price'],
            item['nomer_zayavki'],
            item['sposob_pogr'],
            item['gruzopod_vesov'],
            item['exporter']
        )

        cur.execute(x1)

    cur.execute("SELECT * FROM zernovoz")
    for row in cur.fetchall():
        print(row)

    db.commit()
    db.close()


#    with open(path, 'a', newline='') as file:  # открытие файла для записи
#        writer = csv.writer(file, delimiter=';')  # использование библиотеки csv с использованием в качестве разделителя ;
#        # writer.writerow(['Дата парсинга', 'Время парсинга', 'Дата создания', 'Место погрузки', 'Место выгрузки','Культура', 'Объем, тонн',
#        # 'Расстояние, км', 'Цена, руб/кг', 'Номер зявки', 'Способо погрузки', 'Грузоподъемность весов на погрузке, тонн', 'Экспортер'])  # первая строка таблицы
#        for item in items:  # перебор всех данных в справочнике и запись их в отдельные строки
#            writer.writerow(
#                [DAY, TIME, item['data_soz'], item['pogruzka'], item['vygruzka'], item['product'], item['volume'],
#                item['distance'], item['price'], item['nomer_zayavki'], item['sposob_pogr'], item['gruzopod_vesov'], item['exporter']])

#def save_file_2(item1, item2, path):  # запись данных в файл
#    with open(path, 'a', newline='') as file:  # открытие файла для записи
#        writer = csv.writer(file, delimiter=';')  # использование библиотеки csv с использованием в качестве разделителя ;
#        # writer.writerow(['Дата парсинга', 'Время парсинга', 'Название', 'Количество'])  # первая строка таблицы
#        for i in range(3):  # перебор всех данных в справочнике и запись их в отдельные строки
#            writer.writerow([DAY, TIME, item1[i], item2[i]])

n = session.post('http://zernovozam.ru/cpanel', headers=HEADERS).text

nu = BeautifulSoup(n, 'html.parser')

nums = nu.find_all('div', class_='col-md-4')
n = []
k = []
for num in nums:
    name = num.find('h5', class_='md-title nomargin').get_text(strip=True)
    kol = num.find('h1', class_='mt5').get_text(strip=True)
    n.append(name)
    k.append(kol)
kol1 = int(k[1]) + 30
#save_file_2(n, k, DAT)

def parser():  # итоговая функция для парсинга, задействует все предыдущие
    htm = session.get(URL_top, headers=HEADERS)
    if htm.status_code == 200:  # проверка на получение html с сайта
        htm = session.get(URL_top, headers=HEADERS)

        date = get_content(htm.text)  # формирование справочника с нужными данными
        save_file(date)  # сохранение справочника в файл указанный в константе CSV
    else:
        print('Error')
    for k in range(15, kol1, 15):
        k = str(k)
        n = {'i': k}
        html = get_html(URL, n)
        if html.status_code == 200:  # проверка на получение html с сайта
            html = get_html(URL, n)

            date = get_content(html.text)  # формирование справочника с нужными данными
            save_file(date)  # сохранение справочника в файл указанный в константе CSV
        else:
            print('Error')

parser()
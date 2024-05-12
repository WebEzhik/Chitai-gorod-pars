import pandas as pd
import os.path


def book_save(books):
    if os.path.isfile('./Книги.xlsx'):
        print('Добавление строк в Excel.')
        #Количество строк в файле
        df_col = pd.read_excel('./Книги.xlsx', sheet_name="Книги") 
        col = len(df_col)

        #Файл уже есть
        df = pd.DataFrame(books)
        with pd.ExcelWriter("./Книги.xlsx",
                         mode="a", 
                         engine="openpyxl", 
                         if_sheet_exists="overlay") as writer:
            df.to_excel(writer, sheet_name="Книги", startrow=col+1, index=False, header=False)
    else:
        #Файла нет
        print("Создание файла Excel и добавление строк.")
        df = pd.DataFrame(books)
        df.to_excel('./Книги.xlsx', sheet_name='Книги', index=False)
  

#book_save(a)

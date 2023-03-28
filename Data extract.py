import csv
import psycopg2
import pandas as pd
import bs4 as bs
from bs4 import BeautifulSoup
import requests
import string
# pass_harsh = 'Use your own password'
# conn = psycopg2.connect(database='Round_Diamond', user='use your username', password=pass_harsh)
# cur = conn.cursor()
# cur.execute('''
#         CREATE TABLE Round_diamonds(
#          diamond_id SERIAL PRIMARY KEY,
#          description_dia VARCHAR(100),
#          diamond_type VARCHAR(100),
#          price_dia VARCHAR(50),
#          links_certi VARCHAR(500)
#          )
# ''')
# conn.commit()
# cur.close()
# conn.close()

all_data = []
for page in range(1, 5):
    html_text = requests.get('https://www.ritani.com/collections/round-cut-lab-grown-diamonds'.format(page))
    soup = BeautifulSoup(html_text.content, "html.parser")
    diamonds = soup.find_all('div', class_='FilterCard__Wrapper-sc-10ssyx-0 iRrAfw')
    for diamond in diamonds:
        diamond_name = diamond.find('a', class_='Link___StyledA2-sc-1v26jtv-1 VbEEM').text
        diamond_type = diamond.find('div', class_='Typography__Wrapper-sc-956puz-0 ekrjol mt-0 mb-1').text
        diamond_price = diamond.find('div', class_='mb-0').text
        link = diamond.find('a', class_='Link___StyledA-sc-1v26jtv-0 bKBJgf')
        if link is not None:
            href_1 = link['href']
            # cur.execute('''INSERT INTO Round_diamonds(description_dia, diamond_type, price_dia, links_certi)
            #                  VALUES (%s,%s,%s,%s)''', (diamond_name, diamond_type, diamond_price, href_1))
            # conn.commit()
            data_dia = {"Description": [diamond_name], "Type": [diamond_type], "Price": [diamond_price],
                        "Link": [href_1]}
            all_data.append(data_dia)

df = pd.DataFrame(data=all_data)
# data cleaning processes
df['Description'] = df['Description'].apply(lambda x: x[0]).str.replace('Carat', '', regex=True).\
    str.replace('Lab Diamond', '', regex=True)
df['Type'] = df['Type'].apply(lambda x: x[0]).str.replace('|', '', regex=True)
df['Price'] = df['Price'].apply(lambda x: x[0]).str.replace('$', '', regex=True).str.replace('.00', '', regex=True).\
    astype(int)
df['Link'] = df['Link'].apply(lambda x: x[0])
df[['Type', 'Color', 'Clarity']] = df['Type'].str.split('  ', expand=True)
df[['Carat', 'Description']] = df['Description'].str.split('  ', expand=True)
df['Carat'] = df['Carat'].astype(float).astype(int)
print(df.info())







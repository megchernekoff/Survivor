import requests
import random
import re
import pandas as pd
from bs4 import BeautifulSoup as bs
from io import StringIO
import sqlite3
import warnings
import numpy as np
warnings.filterwarnings("ignore")


FILEPATH = "https://en.wikipedia.org/wiki/Survivor_(American_TV_series)"

def create_connection(db):
    conn = None
    try:
        print('here')
        conn = sqlite3.connect(db)
        return conn
    except Error as e:
        print(e)

    return conn

def create_table(conn):
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS survivor (
        Contestant text,
        Age integer,
        Hometown text,
        Season integer
    );""")

def get_html():
    web = requests.get(FILEPATH)
    web_html = bs(web.content)
    table = web_html.find("table", {"class":'wikitable sortable'})
    df = pd.read_html(StringIO(str(table)))[0]
    season_name, season_loc, season_prem =  df.loc[df['Season'] == int(NUM),
                                               ['Subtitle', 'Location', 'Original tribes']].values.tolist()[0]
    website_str = table.find('a', text='{}'.format(NUM))['href']
    if website_str.startswith('http://'):
        req = requests.get(website_str)
    else:
        website_str = 'http://wikipedia.org' + website_str
        req = requests.get(website_str)
    html = bs(req.content)
    return html, season_name, season_loc, season_prem


def get_contestant_table(html):
    pot_cont_table = html.select('table[class*="wikitable"]')
    for tab in pot_cont_table:
        for col in tab.find_all('th'):
            if 'contestant' in col.text.strip('\n').lower():
                cont_table = tab
    return cont_table


def remove_italics(ct):
    cont_table_body = ct.find_all('tbody')[0]
    new_cont_table_body = bs(re.sub(re.compile('<i>.+</i>'), '', str(cont_table_body)))
    new_cont_table_body = bs(re.sub(re.compile('\[.+\]'), '', str(new_cont_table_body)))
    new_html = bs(str(html).replace(str(cont_table_body), str(new_cont_table_body)))
    return new_html


def get_clean_df(tab):
    df = pd.read_html(StringIO(str(tab)))[0]
    col_list  = [i + ' ' + j if j != i else i for i,j in df.columns]
    df.columns=col_list

    df.fillna(0, inplace=True)
    df = df.loc[df['Contestant'] != 0]
    df.rename(columns={'From':'Hometown'} ,inplace=True)
    df_keep = df[['Contestant', 'Age', 'Hometown']]
    df_keep = df_keep.sample(frac = 1).reset_index(drop=True)
    df_keep['Age'] = df_keep['Age'].apply(lambda x: int(x))
    df_keep['Season'] = NUM
    # df_keep['index'] = np.arange(1, len(df)+ 1)
    print(df_keep)
    return df_keep
    # return df_keep.to_dict('records')


if __name__ == '__main__':
    conn = create_connection('db.sqlite3')
    # create_table(conn)
    # create_table(conn)
    # NUM = input('Enter the Survivor season number: ')
    for NUM in range(1, 43):
        print(NUM)
        html, season_name, season_loc, season_prem = get_html()
        cont_table = get_contestant_table(html)
        new_html = remove_italics(cont_table)
        new_cont_table = get_contestant_table(new_html)
        df_keep = get_clean_df(new_cont_table)
        df_keep.to_sql('survivor', conn, index=False, if_exists='append')

import requests
import random
import re
import pandas as pd
from bs4 import BeautifulSoup as bs
from io import StringIO
import warnings
warnings.filterwarnings("ignore")

FILEPATH = "https://en.wikipedia.org/wiki/Survivor_(American_TV_series)"


def get_html(num):
    web = requests.get(FILEPATH)
    web_html = bs(web.content)
    table = web_html.find("table", {"class":'wikitable sortable'})
    df = pd.read_html(StringIO(str(table)))[0]
    season_name, season_loc, season_prem =  df.loc[df['Season'] == num,
                                               ['Subtitle', 'Location', 'Original tribes']].values.tolist()[0]
    website_str = table.find('a', text='{}'.format(num))['href']
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
    else:
        return('no contestant table')

def remove_italics(cont_table, season_prem, season_loc):
    cont_table.find_all('caption')[-1].insert_after('<caption>{}</caption>'.format(season_loc))
    cont_table.find_all('caption')[-1].insert_after('<caption>{}</caption>'.format(season_prem))
    #Insert season premise and location into
    cap_index = str(cont_table).index('</caption>') + len('</caption>')
    cont_table = str(cont_table)[:cap_index] + '<caption>{}</caption>'.format(season_prem) + str(cont_table)[cap_index:]
    cont_table = bs(str(cont_table)[:cap_index] + '<caption>{}</caption>'.format(season_loc) + str(cont_table)[cap_index:])
    # Remove all footnotes
    cont_table_new = bs(re.sub(re.compile('\[.+\]'), '', str(cont_table))) # str(new_cont_table)
    cont_table_body = cont_table_new.find_all('tbody')[0]
    # Remove italics from Contestants Names
    new_cont_table_body = bs(re.sub(re.compile('<i>.+</i>'), '', str(cont_table_body)))
    new_html= bs(str(cont_table_new).replace(str(cont_table_body), str(new_cont_table_body)))
    return new_html

def get_clean_df(tab, shuffle = 'yes'):
    print('getting df')
    df = pd.read_html(StringIO(str(tab)))[0]
    print('changing column list')
    col_list  = [i + ' ' + j if j != i else i for i,j in df.columns]
    df.columns=col_list
    print('removing nulls')
    df.fillna(0, inplace=True)
    print('restructuring df')
    df = df.loc[df['Contestant'] != 0]
    df_keep = df[['Contestant', 'Age', 'From']]
    print('checking shuffler')
    if shuffle.lower() == 'yes':
        print('shuffling df')
        df_keep = df_keep.sample(frac = 1).reset_index(drop=True)
    # print('fixing age')
    # df_keep['Age'] = df_keep['Age'].apply(lambda x: int(x))
    print('returning df keep')
    print(df_keep)
    return df_keep

def main_function(num, shuffle):
    print('getting html')
    html, season_name, season_loc, season_prem = get_html(num)
    print('getting first contestant table')
    cont_table = get_contestant_table(html)
    print('getting new html')
    new_html = remove_italics(cont_table, season_prem, season_loc)
    print('getting new contestant table')
    new_cont_table = get_contestant_table(new_html)
    print('returning df')
    df_keep = get_clean_df(new_cont_table, shuffle)
    print('python script done')
    df_dict = df_keep.to_dict()
    list(df_dict['Contestant'].values())
    return season_name, season_prem, list(df_dict['Contestant'].values()), list(df_dict['Age'].values()), list(df_dict['From'].values())

if __name__ == '__main__':
        main_function(16, shuffle='No')


# if __name__ == '__main__':
#     main_function()
#     NUM = int(input('Enter a season number: '))
#     shuffle = input('\n Do you want the boot ordered shuffled? (write yes or no) ')
#     html, season_name, season_loc, season_prem = get_html()
#     cont_table = get_contestant_table(html)
#     new_html = remove_italics(cont_table, season_prem, season_loc)
#     new_cont_table = get_contestant_table(new_html)
#     df_keep = get_clean_df(new_cont_table, shuffle)
#
#     table_html = bs(re.sub(re.compile('\n'), '', str(df_keep.to_html())))
#     with open(f'Season {NUM} Contestants.html', 'w') as file:
#         file.write(str(table_html))

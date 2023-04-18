from flask import Flask, request, render_template
import requests
import random
import re
import pandas as pd
from bs4 import BeautifulSoup as bs


FILEPATH = "https://en.wikipedia.org/wiki/Survivor_(American_TV_series)"


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def survivor():
    return render_template('survivor.html', template_folder='templates')


@app.route('/result', methods=['GET', 'POST'])
def get_inputs():
    print(request.method)
    if request.method == 'POST':
        print(request.form.get("season"))
        num = int(request.form.get("season"))
        print('num')
        print(num)
        shuffle = request.form.get("radioname")
        conn = conn = sqlite3.connect('db.sqlite3')
        cursor = conn.execute("""Select * from survivor where Season = {}""".format(num))
        results = pd.DataFrame(cursor.fetchall(), columns=['Contestant', 'Age', 'From', 'Season', 'Season Name', 'Season Premise'])
        snum, sname, snprem = results.iloc[0][['Season', 'Season Name', 'Season Premise']].tolist()
        conts, ags, fs = results['Contestant'].tolist(), results['Age'].tolist(), results['From'].tolist()
        if shuffle == 'Yes':
            random.shuffle(conts)
        # print(pd.DataFrame(results, columns=['Contestant', 'Age', 'From', 'Season', 'Season Name', 'Season Premise']))
        # sn, sp, conts, ags, fs = main_function(num, shuffle)
        # print('TABLE')
        # table_html = bs(re.sub(re.compile('\n'), '', str(df.to_html())))
        # html_index = str(table_html).index('<html>') + len('<html>')
        # table_html = bs(str(table_html)[:html_index] + '<head><title>Survivor Season</title></head>' + str(table_html)[html_index:])
        # print(table_html)
        print('returning html')
        return render_template('result.html', template_folder='templates', season_name=sname, season_prem=snprem, contestants=conts, ages = ags, froms = fs)



# @app.route('/result', methods=['GET', 'POST'])
# def get_inputs():
#     print(request.method)
#     if request.method == 'POST':
#         num = int(request.form.get("season"))
#         shuffle = request.form.get("radioname")
#         df = main_function(num, shuffle)
#         # print('TABLE')
#         # table_html = bs(re.sub(re.compile('\n'), '', str(df.to_html())))
#         # html_index = str(table_html).index('<html>') + len('<html>')
#         # table_html = bs(str(table_html)[:html_index] + '<head><title>Survivor Season</title></head>' + str(table_html)[html_index:])
#         # print(table_html)
#         print('returning html')
#         return df
#
#     else:
#         return 'method was not post'


if __name__ == "__main__":
    app.run(debug=True)
    # survivor()
    # run_main()

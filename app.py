from flask import Flask, request, render_template
from Survivor_Shuffle import main_function
import requests
import random
import re
import pandas as pd
from bs4 import BeautifulSoup as bs
from io import StringIO

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
        sn, sp, conts, ags, fs = main_function(num, shuffle)
        # print('TABLE')
        # table_html = bs(re.sub(re.compile('\n'), '', str(df.to_html())))
        # html_index = str(table_html).index('<html>') + len('<html>')
        # table_html = bs(str(table_html)[:html_index] + '<head><title>Survivor Season</title></head>' + str(table_html)[html_index:])
        # print(table_html)
        print('returning html')
        return render_template('result.html', template_folder='templates', season_name=sn, season_prem=sp, contestants=conts, ages = ags, froms = fs)



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

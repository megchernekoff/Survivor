from flask import Flask, request, render_template
import requests
import random
import sqlite3
import re
import pandas as pd
from bs4 import BeautifulSoup as bs



app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def survivor():
    return render_template('survivor.html', template_folder='templates')


@app.route('/result', methods=['GET', 'POST'])
def get_inputs():
    print(request.method)
    if request.method == 'POST':
        num = int(request.form.get("season"))
        shuffle = request.form.get("radioname")
        conn = conn = sqlite3.connect('db.sqlite3')
        cursor = conn.execute("""Select * from survivor where Season = {}""".format(num))
        results = pd.DataFrame(cursor.fetchall(), columns=['Contestant', 'Age', 'From', 'Season', 'Season Name', 'Season Premise'])
        snum, sname, snprem = results.iloc[0][['Season', 'Season Name', 'Season Premise']].tolist()
        caf_list = list(zip(df['Contestant'], df['Age'], df['From']))
        # conts, ags, fs = results['Contestant'].tolist(), results['Age'].tolist(), results['From'].tolist()
        if shuffle == 'Yes':
            random.shuffle(caf_list)
            # random.shuffle(conts)
        caf_uz = list(zip(*caf_list))
        conts, ags, fs = caf_uz[0], caf_uz[1], caf_uz[2]
        return render_template('result.html', template_folder='templates', season_name=sname, season_prem=snprem, contestants=conts, ages = ags, froms = fs)
    else:
        render_template('survivor.html', template_folder='templates')



if __name__ == "__main__":
    app.run(debug=True)
    # survivor()
    # run_main()

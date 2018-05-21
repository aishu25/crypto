from flask import Flask, session, request, render_template, redirect, send_from_directory
import random
import urllib
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import os
from io import StringIO, BytesIO
from datetime import datetime
import base64
# from bokeh.plotting import figure
# from bokeh.io import output_file, show
import datetime
# import mpld3

app = Flask(__name__, static_folder = 'static')
app.secret_key = "Thisissecret"

@app.route("/")
def show():
	return render_template('data.html')

@app.route("/result", methods=['POST'])
def price():
    symbol = request.form['symbol']
    checkbox = request.form.getlist('check')
    url = 'https://min-api.cryptocompare.com/data/price?fsym={}'.format(symbol)

    if len(checkbox) > 0:
        url += '&tsyms='
        for i in checkbox:
            print i
            url += i+','
    page = requests.get(url)
    data = page.json()    
    return render_template('result.html', data=data, symbol=symbol,checkbox=checkbox)

@app.route("/data", methods=['POST'])
def process():
    symbol = request.form['symbol']
    exchange = request.form['exchange']
    checkbox = request.form.getlist('check')
    url = 'https://min-api.cryptocompare.com/data/price?fsym={}'.format(symbol)

    if len(checkbox) > 0:
        url += '&tsyms='
        for i in checkbox:
            print i
            url += i+','
    
    if exchange:
        url += '&e={}'.format(exchange)
    else:
        url = url
    page = requests.get(url)
    data = page.json()    
    return render_template('result.html', data=data, symbol=symbol,checkbox=checkbox )

@app.route("/getdata", methods=['POST'])
def display():
    interest_symbol = request.form['int_symbol']
    convert_symbol  = request.form['cov_symbol']
    print "interest_symbol",interest_symbol
    print "convert_symbol", convert_symbol
    
    url = "https://min-api.cryptocompare.com/data/histohour?fsym={}&tsym={}&limit=500".format(interest_symbol,convert_symbol)
    page = requests.get(url)
    data = page.json()['Data']
    print "into sendfile"
    df = pd.DataFrame(data)
    df['timestamp'] = [datetime.datetime.fromtimestamp(d) for d in df.time]
    plt.plot(df.timestamp, df.close)
    fig = BytesIO()
    plt.savefig(fig, format='png', dpi=180)
    fig.seek(0)
    plot_url = base64.b64encode(fig.getvalue())    
    return render_template("details.html", interest_symbol=interest_symbol, convert_symbol=convert_symbol, data=data, plot_url=plot_url )

    
app.run(debug=True)
























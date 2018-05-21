from flask import Flask
from flask import render_template
from flask import request
from requests.exceptions import ConnectionError
import requests
import random
import json
import math

from stocks import Options, roundSet
from rest import *

app = Flask(__name__)

app.config["CACHE_TYPE"] = "null"

# Routes
@app.route("/report", methods=['POST', 'GET'])
def listener():
    amount = 0
    report = {}
    options = ['Growth Investing']

    if request.method == POST:
        amount = float(request.form['amount'])
        options = request.form.getlist('investment_choices')  # options are in this array

    print("options length ", len(options))

    stock_info, str_header = Options(options).fetch()

    print('Using the selected investment strategy')

    random_nums = random.sample(range(1, 50), len(stock_info))
    sum_of_random = sum(random_nums)
    ratio = [(i / sum_of_random) * 100 for i in random_nums]
    ratio = roundSet(ratio)

    # print("ratio",ratio)

    total_history = {}
    compiled_data = {}
    symbols = []
    pie_values = []
    projected_amount = 0
    i = 0

    # iterate through all stock and get respective data

    for sym in stock_info:

        tickerSymbol = sym.upper()
        url = RestURL(tickerSymbol).build()
        r = ''

        try:
            r = requests.get(url)
        except ConnectionError as e:
            return 'Cannot connect to API.'

        if r.status_code != ERROR_200:
            return 'Bad request'

        data = r.json()

        if 'Error Message' in data:
            print('Error in data')
            return 'Invalid Stock code'

        # populate the dictionary with all relevant values
        val = list(data['Time Series (Daily)'].values())

        jobs = [{"idType": "TICKER", "idValue": tickerSymbol}]

        if sym not in Options.INDEX_STOCK:
            print("sym not in index ")
            openfigi_headers = {'Content-Type': 'text/json'}
            openfigi_headers['X-OPENFIGI-APIKEY'] = "bdb67ff0-a8a1-4a2c-98a3-49398ec68a53"
            openfigi_url = 'https://api.openfigi.com/v1/mapping'
            print('---------------------------------------------------------------------')
            print(jobs)
            print(openfigi_headers)
            print(openfigi_url)
            print('---------------------------------------------------------------------')
            res = requests.post(url=openfigi_url, headers=openfigi_headers, data=json.dumps(jobs))
            inp = res.json();
            data['cname'] = res.json()[0]['data'][0]['name']
        # print("cname",data['cname'])
        else:
            # print("sym in index ")
            data['cname'] = data['Meta Data']['2. Symbol']
        # print(data['cname'])

        compiled_data[sym] = {'time': getLineGraphData(data['Time Series (Daily)'], total_history),
                              'companyName': data['cname']}
        compiled_data[sym]['latest'] = float(val[0]['4. close'])
        compiled_data[sym]['historical'] = val
        compiled_data[sym]['ratio'] = ratio[i]
        compiled_data[sym]['amount'] = float(amount) * ratio[i] / 100;

        pie_values.append(compiled_data[sym]['amount']);
        symbols.append(sym);
        projected_amount = projected_amount + grahamsForumla(val, compiled_data[sym]['amount'])
        i = i + 1

    report['strategy'] = {'data': compiled_data, 'history': total_history,
                          'history_label': json.dumps(list(total_history.keys())),
                          'history_data': json.dumps(list(total_history.values())), 'pie_labels': json.dumps(symbols),
                          'pie_values': pie_values, 'projected_amount': round(projected_amount, 2)}
    report['strategies_header'] = str_header;
    return render_template('report.html', report_data=report);


@app.route("/", methods=['POST', 'GET'])
def index():
    return render_template('index.html')


def round_to_100_percent(number_set):
    unround_numbers = [x / float(sum(number_set)) * 100 * 10 for x in number_set]
    decimal_part_with_index = sorted([(index, unround_numbers[index] % 1) for index in range(len(unround_numbers))],
                                     key=lambda y: y[1], reverse=True)
    remainder = 100 * 10 - sum([int(x) for x in unround_numbers])
    index = 0
    while remainder > 0:
        unround_numbers[decimal_part_with_index[index][0]] += 1
        remainder -= 1
        index = (index + 1) % len(number_set)
    return [int(x) / 10 for x in unround_numbers]


def grahamsForumla(timeseries, amount):
    days = 1
    total = 0;
    for tt in timeseries:
        total = total + round(float(tt['4. close']), 2)
        days = days + 1

    eps = total / days
    g = 5  # projected for 10 years

    no_of_shares = amount / eps;

    pr = eps * (8.5 + g) / 10

    return pr * no_of_shares;


def getLineGraphData(data, total_history):
    graph = {}
    j = 0

    for data_key in data.keys():

        if (j > 10):
            break

        graph[data_key] = float(data[data_key]['4. close'])

        if data_key in total_history:
            total_history[data_key] += round(float(data[data_key]['4. close']), 2)
        else:
            total_history[data_key] = round(float(data[data_key]['4. close']), 2);

        j += 1

    return graph


app.run(port=8080)

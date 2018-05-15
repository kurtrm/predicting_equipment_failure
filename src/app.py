"""
Basic flask app to display D3 chart.
"""
import os

import yaml
import pandas as pd
import numpy as np
import psycopg2 as pg2
from sklearn.externals import joblib
from flask import (Flask,
                   render_template,
                   request,
                   jsonify)

from profit_curve import generate_cost_matrix, generate_profit_curve

application = Flask(__name__)

model = joblib.load('static/models/final_grad_boost.pkl')


@application.route('/')
def index_page():
    """
    Test for bootstrap template.
    """
    return render_template('index.html')


@application.route('/unit_analysis')
def unit_analysis():
    """
    Renders a form to receive inputs on a transformer,
    then outputs a prediction.
    """
    return render_template('unit_analysis.html')


@application.route('/transformer_prediction', methods=['POST'])
def transformer_prediction():
    """
    Make a prediction based on inputs from a form.
    """
    data = request.json
    binary = ['VegMgmt', 'PMLate', 'WaterExposure', 'MultipleConnects', 'Storm']
    categorical = ['Manufacturer_GE', 'Manufacturer_Other',
                   'Manufacturer_Schneider Electric', 'Manufacturer_Siemens',
                   'Repairs_Original', 'Repairs_Rebuild+1', 'Repairs_Rebuild+2',
                   'Repairs_Rebuild+3', 'AssetType_1-Phase Pole Transformer',
                   'AssetType_3-Phase Transformer', 'AssetType_DF-series Transformer',
                   'AssetType_Padmount Transformer', 'AssetType_Voltage Transformer']
    listy = []
    for header in binary:
        listy.append(data[header] == "1")
    listy.append(int(data['Age']))
    for category in categorical:
        if category in data:
            listy.append(True)
        else:
            listy.append(False)
    # Need to save this threshold
    threshold = .5  # Get threshold
    probs = model.predict_proba(np.array(listy).reshape(1, -1))[:, 1]
    return jsonify({'threshold': f'{threshold * 100}',
                    'probability': f'{probs[0] * 100:.2f}'})


@application.route('/profit_curve')
def profit_curve():
    """
    This route renders the profit curve template.
    """
    return render_template('profit_curve.html')


@application.route('/generate', methods=['POST'])
def make_profit_curve():
    """
    Route that generates new profit curve data from
    user inputs on revenue, maintenance, and repair costs.
    """
    data = request.json
    revenue, maintenance, repair = [float(x) for x in data['user_input']]
    test_set = pd.read_csv('static/data/test_set.csv',
                           sep=';',
                           header=None).values
    X_test, y_test = test_set[:, :-1], test_set[:, -1]
    cost_matrix = generate_cost_matrix(revenue, maintenance, repair)
    thresholds, totals = generate_profit_curve(cost_matrix,
                                               model,
                                               X_test,
                                               y_test)
    return jsonify([{'threshold': threshold, 'loss': total}
                    for threshold, total in zip(thresholds, totals)])


@application.route('/map')
def show_map():
    """
    Show map of all transformers.
    """
    try:
        with open('/home/kurtrm/.secrets/map.yaml', 'r') as f:
            yaml_creds = yaml.load(f)
            key = yaml_creds['API_KEY']
    except FileNotFoundError:
        key = os.environ['API_KEY']

    return render_template('map.html', API_KEY=key)


@application.route('/login')
def login():
    """
    Render template for login page.
    """
    return render_template('login.html')


@application.route('/database_stuff')
def database_test():
    """
    try to get a response from a database.
    """
    conn = pg2.connect(dbname='kurtrm', user='kurtrm', host='localhost')
    cur = conn.cursor()
    cur.execute('SELECT * FROM buy LIMIT 1;')
    fetched = cur.fetchall()
    return '<p>'


@application.route('/retrieve_data', methods=['GET'])
def database_retrieval():
    conn = pg2.connect(dbname='kurtrm', user='kurtrm', host='localhost')
    cur = conn.cursor()
    cur.execute('SELECT * FROM profit_curve;')
    fetched = cur.fetchall()
    return jsonify([{'loss': loss, 'threshold': threshold}
                    for _, loss, threshold in fetched])



if __name__ == '__main__':
    application.run(host='0.0.0.0', port=8080, debug=True)

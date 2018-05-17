"""
Basic flask app to display D3 chart.
"""
import os

import numpy as np
import pytz
from flask import (Flask,
                   render_template,
                   request,
                   jsonify)
from sklearn.externals import joblib

from scripts import db
from scripts.profit_curve import generate_cost_matrix, generate_profit_curve


application = Flask(__name__)

model = joblib.load('static/models/final_grad_boost.pkl')


@application.route('/')
def index_page():
    """
    Display the dashboard including roc and profit curve and
    various other stats.
    """
    _, threshold, cost, revenue, maintenance, repair, time = db.fetch_all_threshold()
    utc = pytz.timezone('UTC')
    pacific = pytz.timezone('US/Pacific')
    fixed_time = utc.localize(time).astimezone(pacific)
    formatted_time = fixed_time.strftime('%Y-%m-%d %I:%M %p %Z')
    return render_template('index.html',
                           threshold=threshold/100,
                           cost=-cost,
                           revenue=revenue,
                           maintenance=-maintenance,
                           repair=-repair,
                           time=formatted_time)


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
    fetched = db.select_threshold()
    threshold = fetched[0]
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
    fetched = db.fetch_test_data()
    test_set = np.array(fetched)[:, 1:]
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
    key = os.environ['API_KEY']
    return render_template('map.html', API_KEY=key)


@application.route('/login')
def login():
    """
    Render template for login page.
    """
    return render_template('login.html')


@application.route('/retrieve_profit_curve', methods=['GET'])
def profit_table_retrieval():
    """
    Retrieves data from database and returns a jsonified list of dictionaries
    back to d3.
    """
    fetched = db.get_profit_curve_data()
    return jsonify([{'loss': loss, 'threshold': threshold}
                    for _, loss, threshold in fetched])


@application.route('/retrieve_roc', methods=['GET'])
def roc_table_retrieval():
    """
    Retrieve roc data for display by d3.
    """
    fetched = db.get_roc_data()
    return jsonify([{'fpr': fpr, 'lin': lin, 'thresh': thresh, 'tpr': tpr}
                    for _, fpr, lin, thresh, tpr in fetched])


@application.route('/save_profit_curve', methods=['POST'])
def save_profit_curve():
    """
    Save the data from the profit curve page.
    """
    data = request.json
    threshold = float(data['threshold'])
    revenue, maintenance, repair = [float(x)
                                    for x in data["metrics"]["user_input"]]
    max_cost = max([num['loss'] for num in data['data']])
    db.update_threshold(threshold, max_cost, revenue, maintenance, repair)
    db.purge_update_profit_curve(data['data'])
    return '200 OK'


@application.route('/map_data', methods=['GET'])
def get_map_data():
    """
    Retrieves map data from the database.
    """
    fetched = db.fetch_map_data()
    return jsonify([{"Latitude": latitude,
                     "Longitude": longitude,
                     "Status": status}
                    for _, latitude, longitude, status in fetched])


if __name__ == '__main__':
    application.run(host='0.0.0.0', port=8080, debug=True)

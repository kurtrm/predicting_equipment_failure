"""
Basic flask app to display D3 chart.
"""
import os

import yaml
import pandas as pd
import numpy as np
from sklearn.externals import joblib
from flask import (Flask,
                   render_template,
                   request,
                   jsonify)

import profit_curve

application = Flask(__name__)


@application.route('/')
def show_chart():
    """
    This route renders the chart template.
    """
    return render_template('chart.html')


@application.route('/new_transformer')
def new_transformer():
    """
    """
    return render_template('new_transformer.html')


@application.route('/transformer_prediction', methods=['POST'])
def transformer_prediction():
    """
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
    import pdb; pdb.set_trace()
    return np.array(listy)


@application.route('/profit_curve')
def show_profit_curve():
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
    model = joblib.load('static/models/final_grad_boost.pkl')
    X_test, y_test = test_set[:, :-1], test_set[:, -1]
    cost_matrix = profit_curve.generate_cost_matrix(revenue, maintenance, repair)
    thresholds, totals = profit_curve.generate_profit_curve(cost_matrix,
                                                            model,
                                                            X_test,
                                                            y_test)
    return jsonify([{'threshold': threshold, 'loss': total}
                    for threshold, total in zip(thresholds, totals)])


@application.route('/map')
def show_map():
    """
    Get data from a database at period intervals.
    """
    try:
        with open('/home/kurtrm/.secrets/map.yaml', 'r') as f:
            key = yaml.load(f)
    except FileNotFoundError:
        key = os.environ['API_KEY']

    return render_template('map.html', API_KEY=key)


@application.route('/index')
def show_index():
    """
    Test for bootstrap template.
    """
    return render_template('index.html')

"""
Todo flow:
I can't back calculate the confusion matrix values from the ROC
curve alone. I'll need the actual data from sklearn's
confusion_matrix function to be able to do this.
Work flow:
it may be beneficial to use the ROC curve you implemented a while ago.

1. For the final model, use the predict_proba method to obtain
probabilities for the test data.

2. Alter ROCandAUC class to return FPRs, TPRs, and TPs, FPs, FNs, TNs.

3. From the array returned in #2, make a list of dictionaries for use
    in D3.

4. When the user hovers mouse over graph, the bisect function returns the
index of the object to retrieve data. We can then grab the whole numbers
inside of the object instead of the rates. The javascript file has
been annotated with the prospective change, see ~line 104.

5. When the user hovers mouse over graph, the confusion matrix is updated
with the numbers, similar to the procedure in #4.

6. The caculates are shown using the numbers in #5.
"""

if __name__ == '__main__':
    application.run(host='0.0.0.0', port=8080, debug=True)

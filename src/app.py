"""
Basic flask app to display D3 chart.
"""
import os

import yaml
import pandas as pd
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


@application.route('/profit_curve')
def show_profit_curve():
    """
    This route renders the profit curve template.
    """
    return render_template('profit_curve.html')


@application.route('/profit_curve', methods=['POST'])
def make_profit_curve():
    """
    Route that generates new profit curve data from
    user inputs on revenue, maintenance, and repair costs.
    """
    test_set = pd.read_csv('static/data/test_set.csv',
                           sep=';',
                           headers=None).values
    X_test, y_test = test_set[:, :-1], test_set[:, -1]
    data = request.json
    revenue, maintenance, repair = data['user_input']
    payout = profit_curve.generate_cost_matrix(revenue, maintenance, repair)
    thresholds, totals = profit_curve.generate_profit_curve(cost_matrix,
                                                            model,
                                                            X_test,
                                                            y_test)




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

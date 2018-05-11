"""
Basic flask app to display D3 chart.
"""
import yaml
from flask import (Flask,
                   render_template)

app = Flask(__name__)


@app.route('/')
def show_chart():

    return render_template('chart.html')


@app.route('/profit_curve')
def show_profit_curve():

    return render_template('profit_curve.html')


@app.route('/get_data')
def get_data():
    """
    Get data from a database at period intervals.
    """
    pass


@app.route('/map')
def show_map():
    """
    Get data from a database at period intervals.
    """
    with open('/home/kurtrm/.secrets/map.yaml', 'r') as f:
        key = yaml.load(f)
    return render_template('map.html', API_KEY=key['API_KEY'])


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
    app.run(host='0.0.0.0', port=8080, debug=True)

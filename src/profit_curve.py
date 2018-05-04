"""
Rough outline of how I want to display
the actual profit curve.
"""

# X-axis: thresholds (0-1.0)
# y-axis: profits (large integers)
"""
Using the trained model, the test data, and a given threshold
calculate the confusion matrix
"""

"""
Have a cost confusion matrix consisting of the costs.
So:

 Actual ->          [Failure | Nominal]
 Predicted [Failure]   -100     -100
     |
     |     [Nominal]   -1000      0

-The cost of repair and failure would each have their own slide bar
-When the slide bar is changed, the values in this matrix would change
"""
# Multiply the cost matrix by the confusion matrix to get dollar values.
# For each threshold, perform the previous step and sum the resulting matrix
# Pass to D3 to graph
"""
Actual ->          [Failure | Nominal]
 Predicted [Failure]   -100      0
     |
     |     [Nominal]   -1000     100
"""
#  Assume 1 hour equates to $100 revenue
#  Repair costs $100 upfront
#  Failure costs $1000

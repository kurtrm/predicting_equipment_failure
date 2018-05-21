# Predicting Transformer Maintenance in the Atlanta Metropolitan Area

## Business Understanding
  Many businesses are forced to extend equipment life due to costs or extraneous situations that demand continued use.
Pumps, compressors, turbines, etc. have operating specifications, but their behavior may vary in the context of the systems they're embedded in, which may lead to unexpected or unpredictable failures. Given that these failures are commonplace, can we predict and therefore prevent equipment failure and subsequent shutdowns?

  Commercial plants or other entities that rely on continual operation of heavy machinery would conduct this analysis in the interest of reducing overhead and thus maximizing profits. Ultimately we want to:
  
  - Reduce equipment downtime
  - Prefer maintenance over repair (recovery from a failure)
  - Perform extra maintenance only on machines that are identified to be "trouble" machines
  
 Ultimately, our model will be used to identify what equipment should maintain a __normal maintenance schedule__ or an __enhanced maintenance schedule__. For the sake of simplicity, we will define a normal maintenance schedule as the maintenance schedule recommended by the manufacturer, and an enhanced maintenance schedule is one that contains supplemental measures to aid in preventing failure, and _total costs are less than the cost of repair_.

## Data Understanding
  The idea of this project came from a field where operating equipment data is classified and destroyed after a set period of time. Additionally, commercial businesses are also hesitant to disclose this information due to security and competitive reasons.
  
  After several failed attempts to obtain this data, a data scientist at SAP SE graciously shared a portion of data centered on electrical transformers in Atlanta, Georgia. This project thus explores machine learning applications to reduce equipment failure/expenses through the analysis of this data set.

## Data Preparation
  The data came labeled, with the "status" column being the target feature. (1) means the electrical transformer has not had a significant history of failure, and (0) means a unit is a "trouble" transformer. Most features are categorical with the only continuous feature used being age.
  
  There were some anomolous features, particularly longitude/latitude, distance from ocean, and average repair cost. To correct longitude/latitude, the Google Maps API was used to geocode the provided address features. Models were still created used the distance from ocean to see if this feature contained predictive power, but it was ultimately dropped. Average repair cost was not useful to aid in determining decision thresholds for the model and was left out of the final model or profit curves.

## Modeling

  The following classification models were used:

    - Logistic Regression
    - Random Forest
    - Gradient Boosting
    - K-Nearest Neighbors

  After building some initial models, there was clear evidence of data leakage. All of the supervised models overfit, and after exploring feature importances and regression coefficients, "overload status" was the problem feature. After researching transformer overloading, it made more sense that this may actually be a strongly correlated feature rather than data leakage, as overloading causes overheating, subsequent insulation deterioration, and ultimate loss of useful life. Still, leaving this feature out resulted in more realistic results, and a note was made on the final dashboard.
  
  K-Nearest Neighbors was applied to latitude and longitude, but the results provided marginal predictive power, and was left out of the final analysis due to time constraints.

## Evaluation
  Review:
  - There may be factors determining transformer performance that are not captured in the provided features.
  - An interface to choose a model decision threshold was provided due to a lack of information on revenue/costs.
  - Additional correspondence from the client is greatly needed to gain clarity on some of the features and perhaps improve model performance.
  
  To evaluate the performance of the model, we will need to observe both difference in costs and reduction in failures post implementation. The model's decision threshold may be changed as profits and costs vary.

## Deployment

  The model is deployed via a web dashboard. As new data becomes available, periodic retraining and evaluation of the model will be performed to ensure maximum predictive power. 

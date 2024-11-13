# Classifier Models for Predicting Bank Fraud 

This project involved building classifier models for identifying fraudulent transactions. 

Of particular interest here may be the use of Anomaly Detection and clustering algorithms to generate new features that flag certain transactions as unusual. These forms of feature engineering turned out to be effective, such that even a simple Logistic Regression model using these features could effectively identify cases of fraud in unseen testing data. These features are engineered only with training data, but then integrated into the modelling pipeline so that the features can be generated for unseen validation and testing data before a prediction is returned. 

The core notebook <i>fraud_classifiers.ipynb</i> will also walk you through: 

- Data Importation. 
- Data Exploration. 
- Cleaning. 
- Preprocessing.
- Feature Engineering. 
- Exploratory Data Analysis. 
- Model training, hyperparamter tuning and evaluation with: 

    - 


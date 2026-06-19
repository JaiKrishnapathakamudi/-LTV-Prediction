import pandas as pd
import joblib

# ML Models
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor

# Metrics
from sklearn.metrics import (
    mean_absolute_error,
    r2_score
)

# -----------------------------------
# LOAD DATA
# -----------------------------------
data = pd.read_csv("data/online_retail.csv")

# -----------------------------------
# CLEANING
# -----------------------------------
data.dropna(inplace=True)

data.drop_duplicates(inplace=True)

data = data[data['Quantity'] > 0]

data = data[data['UnitPrice'] > 0]

# -----------------------------------
# TOTAL PRICE
# -----------------------------------
data['TotalPrice'] = (
    data['Quantity'] * data['UnitPrice']
)

# -----------------------------------
# DATE
# -----------------------------------
data['InvoiceDate'] = pd.to_datetime(
    data['InvoiceDate']
)

snapshot_date = data['InvoiceDate'].max()

# -----------------------------------
# RFM
# -----------------------------------
rfm = data.groupby('CustomerID').agg({

    'InvoiceDate': lambda x:
        (snapshot_date - x.max()).days,

    'InvoiceNo': 'nunique',

    'TotalPrice': 'sum'

})

rfm.rename(columns={

    'InvoiceDate': 'Recency',

    'InvoiceNo': 'Frequency',

    'TotalPrice': 'Monetary'

}, inplace=True)

# -----------------------------------
# BETTER TARGET
# -----------------------------------
rfm['LTV'] = (

    rfm['Monetary'] * 0.5 +

    rfm['Frequency'] * 200 -

    rfm['Recency'] * 5

)

# -----------------------------------
# FEATURES
# -----------------------------------
X = rfm[[
    'Recency',
    'Frequency',
    'Monetary'
]]

y = rfm['LTV']

# -----------------------------------
# SPLIT
# -----------------------------------
X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,

    test_size=0.2,

    random_state=42
)

# -----------------------------------
# LINEAR REGRESSION
# -----------------------------------
lr_model = LinearRegression()

lr_model.fit(X_train, y_train)

lr_predictions = lr_model.predict(X_test)

lr_r2 = r2_score(
    y_test,
    lr_predictions
)

# -----------------------------------
# RANDOM FOREST
# -----------------------------------
rf_model = RandomForestRegressor(

    n_estimators=100,

    random_state=42
)

rf_model.fit(X_train, y_train)

rf_predictions = rf_model.predict(X_test)

rf_r2 = r2_score(
    y_test,
    rf_predictions
)

# -----------------------------------
# RESULTS
# -----------------------------------
print("\nMODEL COMPARISON\n")

print(f"Linear Regression R2: {lr_r2}")

print(f"Random Forest R2: {rf_r2}")

# -----------------------------------
# SAVE BEST MODEL
# -----------------------------------
joblib.dump(
    rf_model,
    "models/advanced_ltv_model.pkl"
)

print(
    "\nAdvanced model saved successfully!"
)

# -----------------------------------
# FEATURE IMPORTANCE
# -----------------------------------
importance = rf_model.feature_importances_

features = X.columns

print("\nFEATURE IMPORTANCE\n")

for feature, score in zip(features, importance):

    print(f"{feature}: {score:.4f}")
    # -----------------------------------
# SAVE FEATURE IMPORTANCE
# -----------------------------------
feature_df = pd.DataFrame({

    'Feature': features,

    'Importance': importance

})

feature_df.to_csv(

    "models/feature_importance.csv",

    index=False

)

# -----------------------------------
# SAVE MODEL COMPARISON
# -----------------------------------
comparison_df = pd.DataFrame({

    'Model': [

        'Linear Regression',

        'Random Forest'

    ],

    'R2 Score': [

        lr_r2,

        rf_r2

    ]

})

comparison_df.to_csv(

    "models/model_comparison.csv",

    index=False

)

print("\nAnalytics files saved successfully!")
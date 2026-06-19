import pandas as pd
import joblib
from datetime import datetime

# ML Libraries
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score

# -----------------------------
# LOAD DATASET
# -----------------------------
data = pd.read_csv("data/online_retail.csv")

# -----------------------------
# DATA CLEANING
# -----------------------------
data.dropna(inplace=True)

data.drop_duplicates(inplace=True)

data = data[data['Quantity'] > 0]

data = data[data['UnitPrice'] > 0]

# -----------------------------
# TOTAL PRICE
# -----------------------------
data['TotalPrice'] = data['Quantity'] * data['UnitPrice']

# -----------------------------
# DATE CONVERSION
# -----------------------------
data['InvoiceDate'] = pd.to_datetime(data['InvoiceDate'])

# -----------------------------
# RFM ANALYSIS
# -----------------------------
snapshot_date = data['InvoiceDate'].max()

rfm = data.groupby('CustomerID').agg({

    'InvoiceDate': lambda x: (snapshot_date - x.max()).days,

    'InvoiceNo': 'nunique',

    'TotalPrice': 'sum'

})

rfm.rename(columns={

    'InvoiceDate': 'Recency',

    'InvoiceNo': 'Frequency',

    'TotalPrice': 'Monetary'

}, inplace=True)

# -----------------------------
# CREATE TARGET VARIABLE
# -----------------------------
rfm['LTV'] = rfm['Monetary']

# -----------------------------
# FEATURES & TARGET
# -----------------------------
X = rfm[['Recency', 'Frequency', 'Monetary']]

y = rfm['LTV']

# -----------------------------
# TRAIN TEST SPLIT
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(

    X, y,
    test_size=0.2,
    random_state=42

)

# -----------------------------
# MODEL TRAINING
# -----------------------------
model = LinearRegression()

model.fit(X_train, y_train)

# -----------------------------
# PREDICTIONS
# -----------------------------
predictions = model.predict(X_test)

# -----------------------------
# MODEL EVALUATION
# -----------------------------
mae = mean_absolute_error(y_test, predictions)

r2 = r2_score(y_test, predictions)

print("\nMODEL PERFORMANCE\n")

print("Mean Absolute Error:", mae)

print("R2 Score:", r2)
# -----------------------------
# SAVE MODEL
# -----------------------------
joblib.dump(model, "models/ltv_model.pkl    ")

print("\nModel saved successfully!")
import pandas as pd
from datetime import datetime

# Load dataset
data = pd.read_csv("data/online_retail.csv")

# -----------------------------
# DATA CLEANING
# -----------------------------
data.dropna(inplace=True)

data.drop_duplicates(inplace=True)

data = data[data['Quantity'] > 0]

data = data[data['UnitPrice'] > 0]

# -----------------------------
# CREATE TOTAL PRICE
# -----------------------------
data['TotalPrice'] = data['Quantity'] * data['UnitPrice']

# -----------------------------
# CONVERT DATE
# -----------------------------
data['InvoiceDate'] = pd.to_datetime(data['InvoiceDate'])

# -----------------------------
# CREATE REFERENCE DATE
# -----------------------------
snapshot_date = data['InvoiceDate'].max()

# -----------------------------
# RFM CALCULATION
# -----------------------------
rfm = data.groupby('CustomerID').agg({

    'InvoiceDate': lambda x: (snapshot_date - x.max()).days,

    'InvoiceNo': 'nunique',

    'TotalPrice': 'sum'

})

# Rename columns
rfm.rename(columns={

    'InvoiceDate': 'Recency',

    'InvoiceNo': 'Frequency',

    'TotalPrice': 'Monetary'

}, inplace=True)


# -----------------------------
# CUSTOMER SEGMENTATION
# -----------------------------

def customer_segment(row):

    if row['Monetary'] > 10000 and row['Frequency'] > 10:
        return 'VIP Customer'

    elif row['Frequency'] > 5:
        return 'Loyal Customer'

    elif row['Recency'] > 100:
        return 'At Risk Customer'

    else:
        return 'Regular Customer'

# Apply segmentation
rfm['Segment'] = rfm.apply(customer_segment, axis=1)

# Show results
print("\nCUSTOMER SEGMENTS\n")

print(rfm.head(20))

# -----------------------------
# SHOW RESULTS
# -----------------------------
print("\nRFM ANALYSIS\n")

print(rfm.head())
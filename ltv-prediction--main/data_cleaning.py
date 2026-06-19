import pandas as pd

# Load dataset
data = pd.read_csv("data/online_retail.csv")

# Show original shape
print("Original Shape:", data.shape)

# Remove missing values
data.dropna(inplace=True)

# Remove duplicate rows
data.drop_duplicates(inplace=True)

# Convert InvoiceDate to datetime
data['InvoiceDate'] = pd.to_datetime(data['InvoiceDate'])

# Remove negative quantity
data = data[data['Quantity'] > 0]

# Remove zero/negative price
data = data[data['UnitPrice'] > 0]

# Show cleaned shape
print("Cleaned Shape:", data.shape)

# Dataset info
print(data.info())

# Missing values after cleaning
print(data.isnull().sum())

# Show first rows
print(data.head())
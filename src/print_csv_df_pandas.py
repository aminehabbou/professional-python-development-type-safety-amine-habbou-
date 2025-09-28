import pandas as pd

# Load CSV into pandas DataFrame
df = pd.read_csv("data/documents.csv")

# Print the DataFrame content
print("=== PANDAS DATAFRAME CONTENT ===")
print(df)
print("\n=== FIRST 5 ROWS ===")
print(df.head())
print("\n=== COLUMNS AND DATA TYPES ===")
print(df.dtypes)
print("\n=== BASIC STATISTICS ===")  # for numerical columns
print(df.describe())

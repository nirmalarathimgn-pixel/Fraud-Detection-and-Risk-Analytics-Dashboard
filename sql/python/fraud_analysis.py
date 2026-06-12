# ==========================================
# FRAUD DETECTION & RISK ANALYTICS PROJECT
# ==========================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# LOAD DATA
# ==========================================

df = pd.read_csv("fraud_transactions.csv")

print("="*50)
print("FRAUD DETECTION & RISK ANALYTICS")
print("="*50)

# ==========================================
# DATA INSPECTION
# ==========================================

print("\nFIRST 5 RECORDS")
print(df.head())

print("\nDATA SHAPE")
print(df.shape)

print("\nDATA TYPES")
print(df.dtypes)

print("\nSUMMARY STATISTICS")
print(df.describe())

# ==========================================
# DATA CLEANING
# ==========================================

print("\nMISSING VALUES")
print(df.isnull().sum())

df.fillna(0, inplace=True)

print("\nREMOVING DUPLICATES")
df.drop_duplicates(inplace=True)

# ==========================================
# DATE CONVERSION
# ==========================================

df["Transaction_Date"] = pd.to_datetime(df["Transaction_Date"])

df["Month"] = df["Transaction_Date"].dt.month_name()

# ==========================================
# NUMPY FEATURE ENGINEERING
# ==========================================

df["Risk_Level"] = np.where(
    df["Risk_Score"] >= 80,
    "High Risk",
    np.where(
        df["Risk_Score"] >= 50,
        "Medium Risk",
        "Low Risk"
    )
)

# ==========================================
# KPI CALCULATIONS
# ==========================================

total_transactions = len(df)

fraud_transactions = df["Fraud_Flag"].sum()

non_fraud_transactions = total_transactions - fraud_transactions

fraud_rate = round(
    (fraud_transactions / total_transactions) * 100,
    2
)

total_amount = round(
    df["Amount"].sum(),
    2
)

fraud_amount = round(
    df[df["Fraud_Flag"] == 1]["Amount"].sum(),
    2
)

average_transaction = round(
    df["Amount"].mean(),
    2
)

print("\nKPI SUMMARY")
print("="*50)

print("Total Transactions :", total_transactions)
print("Fraud Transactions :", fraud_transactions)
print("Non Fraud Transactions :", non_fraud_transactions)
print("Fraud Rate (%) :", fraud_rate)
print("Total Amount :", total_amount)
print("Fraud Amount :", fraud_amount)
print("Average Transaction :", average_transaction)

# ==========================================
# REGION ANALYSIS
# ==========================================

region_analysis = (
    df.groupby("Region")
    .agg(
        Transactions=("Transaction_ID","count"),
        Amount=("Amount","sum"),
        Fraud_Count=("Fraud_Flag","sum")
    )
)

print("\nREGION ANALYSIS")
print(region_analysis)

# ==========================================
# PAYMENT METHOD ANALYSIS
# ==========================================

payment_analysis = (
    df.groupby("Payment_Method")
    .agg(
        Transactions=("Transaction_ID","count"),
        Fraud_Count=("Fraud_Flag","sum")
    )
)

print("\nPAYMENT METHOD ANALYSIS")
print(payment_analysis)

# ==========================================
# TRANSACTION TYPE ANALYSIS
# ==========================================

transaction_analysis = (
    df.groupby("Transaction_Type")
    .agg(
        Transactions=("Transaction_ID","count"),
        Fraud_Count=("Fraud_Flag","sum")
    )
)

print("\nTRANSACTION TYPE ANALYSIS")
print(transaction_analysis)

# ==========================================
# TOP RISKY CUSTOMERS
# ==========================================

top_risky_customers = (
    df.groupby("Customer_ID")
    .agg(
        Max_Risk=("Risk_Score","max"),
        Total_Amount=("Amount","sum")
    )
    .sort_values(
        by="Max_Risk",
        ascending=False
    )
    .head(10)
)

print("\nTOP RISKY CUSTOMERS")
print(top_risky_customers)

# ==========================================
# HIGH RISK TRANSACTIONS
# ==========================================

high_risk_transactions = df[
    df["Risk_Level"] == "High Risk"
]

# ==========================================
# EXPORT FILES
# ==========================================

region_analysis.to_csv(
    "region_analysis.csv"
)

payment_analysis.to_csv(
    "payment_analysis.csv"
)

transaction_analysis.to_csv(
    "transaction_analysis.csv"
)

top_risky_customers.to_csv(
    "top_risky_customers.csv"
)

high_risk_transactions.to_csv(
    "high_risk_transactions.csv",
    index=False
)

cleaned_data = "cleaned_fraud_data.csv"

df.to_csv(
    cleaned_data,
    index=False
)

# ==========================================
# CHART 1
# FRAUD VS NON FRAUD
# ==========================================

plt.figure(figsize=(6,4))

df["Fraud_Flag"].value_counts().plot(
    kind="bar"
)

plt.title("Fraud vs Non Fraud")
plt.xlabel("Fraud Flag")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig("fraud_vs_nonfraud.png")
plt.close()

# ==========================================
# CHART 2
# FRAUD BY REGION
# ==========================================

plt.figure(figsize=(8,4))

df[df["Fraud_Flag"] == 1] \
.groupby("Region") \
.size() \
.plot(kind="bar")

plt.title("Fraud by Region")
plt.xlabel("Region")
plt.ylabel("Fraud Count")
plt.tight_layout()
plt.savefig("fraud_by_region.png")
plt.close()

# ==========================================
# CHART 3
# PAYMENT METHOD
# ==========================================

plt.figure(figsize=(8,4))

df[df["Fraud_Flag"] == 1] \
.groupby("Payment_Method") \
.size() \
.plot(kind="bar")

plt.title("Fraud by Payment Method")
plt.xlabel("Payment Method")
plt.ylabel("Fraud Count")
plt.tight_layout()
plt.savefig("fraud_by_payment_method.png")
plt.close()

# ==========================================
# CHART 4
# TRANSACTION TYPE
# ==========================================

plt.figure(figsize=(8,4))

df[df["Fraud_Flag"] == 1] \
.groupby("Transaction_Type") \
.size() \
.plot(kind="bar")

plt.title("Fraud by Transaction Type")
plt.xlabel("Transaction Type")
plt.ylabel("Fraud Count")
plt.tight_layout()
plt.savefig("fraud_by_transaction_type.png")
plt.close()

# ==========================================
# CHART 5
# TOP RISKY CUSTOMERS
# ==========================================

plt.figure(figsize=(10,4))

top_risky_customers["Max_Risk"].plot(
    kind="bar"
)

plt.title("Top Risky Customers")
plt.xlabel("Customer ID")
plt.ylabel("Risk Score")
plt.tight_layout()
plt.savefig("top_risky_customers.png")
plt.close()

# ==========================================
# MONTHLY FRAUD TREND
# ==========================================

monthly_fraud = (
    df[df["Fraud_Flag"] == 1]
    .groupby("Month")
    .size()
)

plt.figure(figsize=(10,4))

monthly_fraud.plot(
    kind="line",
    marker="o"
)

plt.title("Monthly Fraud Trend")
plt.xlabel("Month")
plt.ylabel("Fraud Count")
plt.tight_layout()
plt.savefig("monthly_fraud_trend.png")
plt.close()

# ==========================================
# FINAL MESSAGE
# ==========================================

print("\nFILES CREATED")
print("cleaned_fraud_data.csv")
print("region_analysis.csv")
print("payment_analysis.csv")
print("transaction_analysis.csv")
print("top_risky_customers.csv")
print("high_risk_transactions.csv")

print("\nCHARTS CREATED")
print("fraud_vs_nonfraud.png")
print("fraud_by_region.png")
print("fraud_by_payment_method.png")
print("fraud_by_transaction_type.png")
print("top_risky_customers.png")
print("monthly_fraud_trend.png")

print("\nPROJECT COMPLETED SUCCESSFULLY")

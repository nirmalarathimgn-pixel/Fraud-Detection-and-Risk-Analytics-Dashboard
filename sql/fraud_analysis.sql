-- ==========================================
-- FRAUD DETECTION & RISK ANALYTICS PROJECT
-- ==========================================

DROP DATABASE IF EXISTS fraud_dw;

CREATE DATABASE fraud_dw;

USE fraud_dw;

-- ==========================================
-- CREATE TABLE
-- ==========================================

CREATE TABLE fraud_transactions (
    Transaction_ID INT PRIMARY KEY,
    Transaction_Date DATE,
    Customer_ID VARCHAR(20),
    Region VARCHAR(50),
    Transaction_Type VARCHAR(50),
    Payment_Method VARCHAR(50),
    Amount DECIMAL(12,2),
    Risk_Score INT,
    Fraud_Flag INT
);

-- ==========================================
-- SAMPLE DATA
-- ==========================================

INSERT INTO fraud_transactions VALUES
(1,'2024-01-01','C101','North','Online','Credit Card',1200,85,1),
(2,'2024-01-02','C102','South','POS','Debit Card',300,20,0),
(3,'2024-01-03','C103','East','Online','UPI',4500,95,1),
(4,'2024-01-04','C104','West','ATM','Debit Card',800,35,0),
(5,'2024-01-05','C105','North','Online','Credit Card',6000,99,1),
(6,'2024-01-06','C106','East','POS','Credit Card',700,25,0),
(7,'2024-01-07','C107','South','Online','UPI',2200,88,1),
(8,'2024-01-08','C108','West','POS','Debit Card',500,15,0),
(9,'2024-01-09','C109','North','ATM','Debit Card',900,30,0),
(10,'2024-01-10','C110','East','Online','Credit Card',8500,100,1);

-- ==========================================
-- KPI QUERIES
-- ==========================================

SELECT COUNT(*) AS Total_Transactions
FROM fraud_transactions;

SELECT COUNT(*) AS Fraud_Transactions
FROM fraud_transactions
WHERE Fraud_Flag = 1;

SELECT ROUND(
(COUNT(CASE WHEN Fraud_Flag = 1 THEN 1 END) * 100.0)
/ COUNT(*),2) AS Fraud_Rate_Percent
FROM fraud_transactions;

SELECT ROUND(SUM(Amount),2)
AS Total_Transaction_Amount
FROM fraud_transactions;

SELECT ROUND(AVG(Amount),2)
AS Avg_Transaction_Value
FROM fraud_transactions;

-- ==========================================
-- FRAUD VS NON FRAUD
-- ==========================================

SELECT
Fraud_Flag,
COUNT(*) AS Transaction_Count
FROM fraud_transactions
GROUP BY Fraud_Flag;

-- ==========================================
-- FRAUD AMOUNT
-- ==========================================

SELECT
SUM(Amount) AS Fraud_Amount
FROM fraud_transactions
WHERE Fraud_Flag = 1;

-- ==========================================
-- REGION ANALYSIS
-- ==========================================

SELECT
Region,
COUNT(*) AS Fraud_Count
FROM fraud_transactions
WHERE Fraud_Flag = 1
GROUP BY Region
ORDER BY Fraud_Count DESC;

-- ==========================================
-- PAYMENT METHOD ANALYSIS
-- ==========================================

SELECT
Payment_Method,
COUNT(*) AS Fraud_Count
FROM fraud_transactions
WHERE Fraud_Flag = 1
GROUP BY Payment_Method
ORDER BY Fraud_Count DESC;

-- ==========================================
-- TRANSACTION TYPE ANALYSIS
-- ==========================================

SELECT
Transaction_Type,
COUNT(*) AS Fraud_Count
FROM fraud_transactions
WHERE Fraud_Flag = 1
GROUP BY Transaction_Type
ORDER BY Fraud_Count DESC;

-- ==========================================
-- MONTHLY FRAUD TREND
-- ==========================================

SELECT
MONTH(Transaction_Date) AS Month_No,
COUNT(*) AS Fraud_Count
FROM fraud_transactions
WHERE Fraud_Flag = 1
GROUP BY MONTH(Transaction_Date)
ORDER BY Month_No;

-- ==========================================
-- HIGH RISK TRANSACTIONS
-- ==========================================

SELECT *
FROM fraud_transactions
WHERE Risk_Score >= 80
ORDER BY Risk_Score DESC;

-- ==========================================
-- RISK LEVEL CLASSIFICATION
-- ==========================================

SELECT
CASE
WHEN Risk_Score >= 80 THEN 'High Risk'
WHEN Risk_Score >= 50 THEN 'Medium Risk'
ELSE 'Low Risk'
END AS Risk_Level,
COUNT(*) AS Total_Transactions
FROM fraud_transactions
GROUP BY Risk_Level;

-- ==========================================
-- TOP RISKY CUSTOMERS
-- ==========================================

SELECT
Customer_ID,
MAX(Risk_Score) AS Highest_Risk_Score,
SUM(Amount) AS Total_Amount
FROM fraud_transactions
GROUP BY Customer_ID
ORDER BY Highest_Risk_Score DESC
LIMIT 10;

-- ==========================================
-- TOP FRAUD TRANSACTIONS
-- ==========================================

SELECT
Transaction_ID,
Customer_ID,
Amount,
Risk_Score
FROM fraud_transactions
WHERE Fraud_Flag = 1
ORDER BY Amount DESC
LIMIT 10;

-- ==========================================
-- EXECUTIVE SUMMARY KPIs
-- ==========================================

SELECT
COUNT(*) AS Total_Transactions,
SUM(Amount) AS Total_Amount,
COUNT(CASE WHEN Fraud_Flag = 1 THEN 1 END) AS Fraud_Count,
ROUND(
COUNT(CASE WHEN Fraud_Flag = 1 THEN 1 END)*100.0
/COUNT(*),2) AS Fraud_Percentage
FROM fraud_transactions;

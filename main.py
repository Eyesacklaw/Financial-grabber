# Disclaimer: This is for educational/testing purposes only. Data gathered may not be
# accurate, and may not always be real time. This is only a project I've been working
# on just for fun and convenience so I can get information about stocks quickly.

import yfinance as yf
import pandas as pd
import os

StockName = input("Type in Ticker >>> ")
Stock = yf.Ticker(StockName)

info = Stock.info

pd.DataFrame(Stock.financials).to_csv(f'{StockName}_1.csv')
pd.DataFrame(Stock.balance_sheet).to_csv(f'{StockName}_2.csv')
pd.DataFrame(Stock.cashflow).to_csv(f'{StockName}_3.csv')

dates = []

def iterator(parameter, dataset):
    for i in range(len(dataset)):
        if dataset[i][0] == parameter:
            return dataset[i][1:]

with open(f"{StockName}.csv", "x") as f:
    for i in range(3):
        with open(f"{StockName}_{i+1}.csv", "r") as g:
            data = g.read().splitlines()
            if i == 1:
                dates = data[0]
            if i+1 > 1:
                data = data[1:]
        for n in range(len(data)):
            f.write(data[n])
            f.write("\n")
    f.write("\n")
f.close()

with open(f"{StockName}.csv", "r") as f:
    data = f.read().splitlines()

for i in range(len(data)):
    data[i] = data[i].split(",")

for i in range(len(data)):
    for n in range(len(data[i])):
        if data[i][n] == "":
            data[i][n] = 0

# Reorder data
reconstructed_data = []

# Income Statement, Balance Sheet - Assets, Liabilites, Shareholder's Equity, 
# Cashflow Statement
order = ["Total Revenue", "Cost Of Revenue", "Gross Profit", "Total Operating Expenses",
"Selling General Administrative", "Research Development", "Other Operating Expenses",
"Operating Income", "Interest Expense", "Extraordinary Items", "Non Recurring", 
"Other Items", "Total Other Income Expense Net", "Income Before Tax", 
"Income Tax Expense", "Net Income", "Minority Interest", "Ebit", 

 "Cash", "Short Term Investments", "Net Receivables", "Inventory",
 "Other Current Assets", "Total Current Assets",
 "Property Plant Equipment",
 "Deferred Long Term Asset Charges", 
 "Good Will", "Long Term Investments",
 "Net Tangible Assets", "Intangible Assets", "Other Assets", "Total Assets",
 
 "Accounts Payable", "Short Long Term Debt", "Other Current Liab", 
 "Total Current Liabilities", "Long Term Debt", 
 "Minority Interest", "Other Liab", "Total Liab",
 
 "Retained Earnings", "Capital Surplus", 
 "Gains Losses Not Affecting Retained Earnings", "Common Stock", 
 "Other Stockholder Equity", "Total Stockholder Equity",
 
 "Net Borrowings", "Issuance Of Stock", "Capital Expenditures",
 "Depreciation", "Dividends Paid",
 "Change To Inventory", "Change To Liabilities", "Change To Operating Activities",
 "Change To Account Receivables", "Change To Netincome", 
 "Total Cashflows From Investing Activities",
 "Total Cash From Financing Activities", 
 "Total Cash From Operating Activities", "Change In Cash", "Effect Of Exchange Rate"]

for i in range(len(order)):
    for n in range(len(data)):
        if data[n][0] == order[i]:
            reconstructed_data.append(data[n])
            break

for i in range(len(reconstructed_data)):
    for n in range(1, len(reconstructed_data[i])):
        try:
            reconstructed_data[i][n] = float(reconstructed_data[i][n][:-6]) # Convert numbers to millions
        except:
            continue

# Perform Calculations
Calculations = ["Gross Profit Margin", "SGA to Gross Profit", "R&D to Gross Profit", 
"Interest Expense to Operating Income", "Net Profit Margin", "ROA", "DTE", "ROE"]

def division(calculation_name, parameters, putbehind, dataset):
    data = []
    end_data = []
    index = 0

    data.append(iterator(parameters[0], dataset))
    data.append(iterator(parameters[1], dataset))

    for i in range(len(dataset)):
        if dataset[i][0] == putbehind:
            index = i + 1
            break   
    
    for i in range(len(data[0])):
         # Formatting
        end_data.append(str(round(((data[0][i]/data[1][i])*100), 2)) + "%")
         # Performs calculation, rounds answer to 2 d.p. and adds a "%" symbol after it

    end_data.insert(0, calculation_name)
    dataset.insert(index, end_data)

    return dataset

reconstructed_data = division(Calculations[0], ["Gross Profit", "Total Revenue"], "Gross Profit", reconstructed_data)
reconstructed_data = division(Calculations[1], ["Selling General Administrative", "Gross Profit"], "Selling General Administrative", reconstructed_data)
reconstructed_data = division(Calculations[2], ["Research Development", "Gross Profit"], "Research Development", reconstructed_data)
reconstructed_data = division(Calculations[3], ["Interest Expense", "Operating Income"], "Interest Expense", reconstructed_data)
reconstructed_data = division(Calculations[4], ["Net Income", "Total Revenue"], "Net Income", reconstructed_data)
reconstructed_data = division(Calculations[5], ["Net Income", "Total Assets"], "Total Assets", reconstructed_data)
reconstructed_data = division(Calculations[6], ["Total Liab", "Total Stockholder Equity"], "Total Stockholder Equity", reconstructed_data)
reconstructed_data = division(Calculations[7], ["Net Income", "Total Stockholder Equity"], "DTE", reconstructed_data)

with open(f"{StockName}.csv", "w") as f:
    f.write(f"{StockName}\n")
    f.write("Sector: " + info["sector"] + "\n")
    f.write(info["longBusinessSummary"] + "\n")
    f.write("All Numbers in Millions\n")
    for i in range(len(reconstructed_data)):
        data = ""
        for n in range(len(reconstructed_data[i])):
            if reconstructed_data[i][n] == "Total Revenue": f.write(f"\n \nIncome Statement{dates}\n")
            elif reconstructed_data[i][n] == "Cash": f.write("\n \nBalance Sheet\n")
            elif reconstructed_data[i-1][n] == "ROE": f.write("\n \nCashflow Statement\n")
            data += str(reconstructed_data[i][n]) + ","
        f.write(data)
        f.write("\n")

for i in range(3): os.remove(f'{StockName}_{i+1}.csv')
import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Function to calculate Discounted Cash Flow (DCF)
def discounted_cash_flow(free_cash_flows, discount_rate, terminal_growth_rate, terminal_year):
    """
    Calculate the Discounted Cash Flow (DCF) for a given set of free cash flows.
    """
    # Calculate the present value of future cash flows
    years = len(free_cash_flows)
    present_value_cash_flows = sum([cf / (1 + discount_rate) ** (i + 1) for i, cf in enumerate(free_cash_flows)])

    # Calculate terminal value
    terminal_value = free_cash_flows[-1] * (1 + terminal_growth_rate) / (discount_rate - terminal_growth_rate)
    terminal_value_discounted = terminal_value / (1 + discount_rate) ** terminal_year

    # Calculate the enterprise value (DCF value)
    enterprise_value = present_value_cash_flows + terminal_value_discounted
    return enterprise_value

# Download Nvidia financial data from Yahoo Finance
ticker = "NVDA"
nvda = yf.Ticker(ticker)

# Get Nvidia's Cash Flow statement
cashflow = nvda.cashflow

# Check the available data and inspect the first few rows to find Free Cash Flow
print(cashflow.head())  # Shows a preview of the data
print(cashflow.columns)  # Shows the column names

# Retrieve the Free Cash Flow (FCF) data from the cashflow statement
# We use 'Free Cash Flow' from the rows; if not found, we use 'Operating Cash Flow' - 'Capital Expenditures'
# Modify this according to the available columns if necessary
try:
    # Access Free Cash Flow row
    free_cash_flow = cashflow.loc["Free Cash Flow"]
except KeyError:
    print("'Free Cash Flow' not found, using alternative method.")
    # Alternative method: Estimate Free Cash Flow = Operating Cash Flow - Capital Expenditures
    free_cash_flow = cashflow.loc["Operating Cash Flow"] - cashflow.loc["Capital Expenditures"]

# Estimate future Free Cash Flows (simplified)
last_fcf = free_cash_flow.iloc[0]  # Taking the latest Free Cash Flow
long_term_growth_rate = 0.03  # 3% growth rate
discount_rate = 0.1  # 10% discount rate
projected_cashflows = [last_fcf * (1 + long_term_growth_rate) ** i for i in range(1, 6)]  # Next 5 years

# Perform the DCF calculation using the projected cash flows
terminal_year = len(projected_cashflows)  # Terminal year for DCF
enterprise_value = discounted_cash_flow(projected_cashflows, discount_rate, long_term_growth_rate, terminal_year)

# Output the enterprise value based on DCF
print(f"The enterprise value based on DCF is: ${enterprise_value / 1e9:.2f} billion")

# Plot the projected discounted cash flows
dcf_values = [cf / (1 + discount_rate) ** i for i, cf in enumerate(projected_cashflows, 1)]
plt.bar(range(1, 6), dcf_values)
plt.xlabel("Year")
plt.ylabel("Discounted Cash Flow (in billions)")
plt.title(f"Projected Discounted Cash Flows for {ticker}")
plt.show()
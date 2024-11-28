import yfinance as yf
import matplotlib.pyplot as plt

# Function to calculate Discounted Cash Flow (DCF)
def discounted_cash_flow(free_cash_flows, discount_rate, terminal_growth_rate, terminal_year):
    """
    Calculates the Discounted Cash Flow (DCF) for a given set of free cash flows.
    
    Args:
        free_cash_flows (list): List of future free cash flows.
        discount_rate (float): The rate used to discount the future cash flows.
        terminal_growth_rate (float): The growth rate for terminal value calculation.
        terminal_year (int): The year at which the terminal value is estimated.

    Returns:
        float: The calculated enterprise value based on the DCF.
    """
    # Calculate the present value of future cash flows
    present_value_cash_flows = sum(
        [cf / (1 + discount_rate) ** (i + 1) for i, cf in enumerate(free_cash_flows)]
        )

    # Calculate terminal value
    terminal_value = free_cash_flows[-1] * \
        (1 + terminal_growth_rate) / (discount_rate - terminal_growth_rate)
    terminal_value_discounted = terminal_value / (1 + discount_rate) ** terminal_year

    # Calculate the enterprise value (DCF value)
    enterprise_value = present_value_cash_flows + terminal_value_discounted
    return enterprise_value


# Download Nvidia financial data from Yahoo Finance
TICKER = "NVDA"
nvda = yf.Ticker(TICKER)

# Get Nvidia's Cash Flow statement
cashflow = nvda.cashflow

# Check the available data and inspect the first few rows to find Free Cash Flow
print(cashflow.head())  # Shows a preview of the data
print(cashflow.columns)  # Shows the column names

# Retrieve the Free Cash Flow (FCF) data from the cashflow statement
try:
    # Access Free Cash Flow row
    free_cash_flow = cashflow.loc["Free Cash Flow"]
except KeyError:
    print("'Free Cash Flow' not found, using alternative method.")
    # Alternative method: Estimate Free Cash Flow = Operating Cash Flow - Capital Expenditures
    free_cash_flow = cashflow.loc["Operating Cash Flow"] - cashflow.loc["Capital Expenditures"]

# Estimate future Free Cash Flows (simplified)
last_fcf = free_cash_flow.iloc[0]  # Taking the latest Free Cash Flow
LONG_TERM_GROWTH_RATE = 0.03  # 3% growth rate
DISCOUNT_RATE = 0.1  # 10% discount rate
projected_cashflows = [last_fcf * (1 + LONG_TERM_GROWTH_RATE) ** i for i in range(1, 6)]  # Next 5 years

# Perform the DCF calculation using the projected cash flows
terminal_year_value = len(projected_cashflows)  # Terminal year for DCF
enterprise_value_result = discounted_cash_flow(projected_cashflows, DISCOUNT_RATE, LONG_TERM_GROWTH_RATE, terminal_year_value)

# Output the enterprise value based on DCF
print(f"The enterprise value based on DCF is: ${enterprise_value_result / 1e9:.2f} billion")

# Plot the projected discounted cash flows
dcf_values = [cf / (1 + DISCOUNT_RATE) ** i for i, cf in enumerate(projected_cashflows, 1)]
plt.bar(range(1, 6), dcf_values)
plt.xlabel("Year")
plt.ylabel("Discounted Cash Flow (in billions)")
plt.title(f"Projected Discounted Cash Flows for {TICKER}")
plt.show()
import pandas as pd

def calculate_annual_returns(file_path):
    # Read the historical data
    df = pd.read_csv(file_path)

    # Parsing 'Date' column as datetime
    df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m')

    # Sorting data by Date
    df.sort_values('Date', inplace=True)

    # Calculate monthly returns first
    df['Monthly Return'] = df['MSCI World'].pct_change()

    # Resample to annual returns
    df['Year'] = df['Date'].dt.year
    annual_returns = df.groupby('Year')['Monthly Return'].apply(lambda x: (1 + x).prod() - 1)

    # Calculate mean and standard deviation of the annual returns
    mean_annual_return = annual_returns.mean()
    std_dev_annual_return = annual_returns.std()

    return mean_annual_return, std_dev_annual_return


### Step 2: Monte Carlo Simulation with Recurring Deposits and TWR Calculation


import numpy as np

def monte_carlo_simulation_with_twr(mean_return, std_dev, initial_investment, monthly_deposit, n_years, n_simulations):
    annual_returns = np.random.normal(mean_return, std_dev, size=(n_simulations, n_years))
    investment_values = np.zeros((n_simulations, n_years + 1))
    investment_values[:, 0] = initial_investment
    monthly_return = (1 + mean_return) ** (1 / 12) - 1

    individual_returns = []

    for sim in range(n_simulations):
        year_returns = []
        for year in range(1, n_years + 1):
            investment_values[sim, year] = (investment_values[sim, year - 1] * (1 + annual_returns[sim, year - 1]) +
                                            monthly_deposit * ((1 + monthly_return) ** 12 - 1) / monthly_return)
            year_return = (investment_values[sim, year] / (investment_values[sim, year - 1] + monthly_deposit * 12)) - 1
            year_returns.append(year_return)
        individual_returns.append(year_returns)

    twr = [(np.prod([(1 + r) for r in individual_returns[sim]]) ** (1/n_years)) - 1 for sim in range(n_simulations)]

    return investment_values, twr


### Step 3: Plotting Results


import matplotlib.pyplot as plt

def plot_simulation_results_with_twr(investment_values, twr_percentiles):
    # Calculate the percentiles
    investment_percentiles = np.percentile(investment_values, [10, 20, 50, 90], axis=0)
    twr_percentiles = np.percentile(twr_percentiles, [10, 20, 50, 90])

    # Calculate the final investment values at percentiles
    final_values = investment_percentiles[:, -1]

    # Plot the simulation and the percentiles
    plt.figure(figsize=(12, 8))
    plt.plot(investment_values.T, alpha=0.1, color='gray')
    plt.plot(investment_percentiles[0], label='10th percentile', color='red')
    plt.plot(investment_percentiles[1], label='20th percentile', color='blue')
    plt.plot(investment_percentiles[2], label='50th percentile', color='green')
    plt.plot(investment_percentiles[3], label='90th percentile', color='black')
    plt.xlabel('Year')
    plt.ylabel('Investment Value (€)')
    plt.legend()
    plt.title('Monte Carlo Simulation of Investment Growth with Recurring Deposits')

    # Annotate the final values and TWR, applying thousand separators
    for index, final_value in enumerate(final_values):
        plt.text(investment_values.shape[1] - 1, final_value,
                 f'{final_value:,.2f}€\n(TWR: {twr_percentiles[index]*100:.2f}%)',
                 horizontalalignment='left',
                 verticalalignment='center')

    # Display final values and TWR below the chart
    final_values_df = pd.DataFrame({
        'Percentile': ['10th', '20th', '50th', '90th'],
        'Final Value (€)': [f'{value:,.2f}' for value in final_values],
        'TWR (%)': [f'{twr*100:.2f}' for twr in twr_percentiles]
    })

    plt.figtext(0.5, -0.15, final_values_df.to_string(index=False),
                horizontalalignment='center', fontsize=12, bbox=dict(facecolor='white', alpha=0.5))
    plt.show()


### Main Function to Tie Everything Together:


def main():
    file_path = 'chartMSCIWORLD1978-2024.csv'
    initial_investment = 10000  # initial amount in EUR
    monthly_deposit = 100 # recurring monthly deposit
    n_years = 30  # projection period in years
    n_simulations = 1000  # number of simulations

    # Calculate annual returns
    mean_annual_return, std_dev_annual_return = calculate_annual_returns(file_path)

    # Perform Monte Carlo simulation with TWR calculation
    investment_values, twr = monte_carlo_simulation_with_twr(mean_annual_return, std_dev_annual_return,
                                                             initial_investment, monthly_deposit,
                                                             n_years, n_simulations)

    # Plot the results with TWR
    plot_simulation_results_with_twr(investment_values, twr)

# Execute the main function
main()

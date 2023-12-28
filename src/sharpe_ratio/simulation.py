import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class Simulation():
    def __init__(self, portfolio: pd.DataFrame, trials: int, risk_free_rate: float) -> None:
        self.portfolio = portfolio
        self.TRIALS = trials
        self.RISK_FREE_RATE = risk_free_rate
        self.TRADING_DAYS = 252

    def get_pct_returns(self):
        return self.portfolio.pct_change().dropna()

    def get_annualized_mean_returns(self):
        r = self.get_pct_returns() * self.TRADING_DAYS
        return r.mean()

    def get_covariance_matrix(self):
        r = self.get_pct_returns()
        return r.cov()

    def simulate(self):
        """
        Method that runs a monte carlo simulation with different weights of each investment in portfolio and monitoring how that effects returns

        :return: Dictionary with simulation results.
        """
        # Calculate average daily returns and the covariance matrix for the assets
        annualized_mean_returns = self.get_annualized_mean_returns()
        cov_matrix = self.get_covariance_matrix()

        portfolio_weights = []
        portfolio_returns = []
        portfolio_volatilities = []
        sharpe_ratios = []

        # Run simulations to generate random portfolios
        for _ in range(self.TRIALS):
            # Generate random weights for each stock in the portfolio and normalize them
            #! Consider the join_tickers() logic here below
            weights = np.random.random(len(self.portfolio.columns))
            weights /= np.sum(weights)

            # Calculate expected portfolio return
            portfolio_return = np.dot(weights, annualized_mean_returns)

            # Calculate portfolio variance
            portfolio_variance = np.dot(weights.T, np.dot(cov_matrix, weights))

            # Calculate annualized portfolio volatility (standard deviation)
            portfolio_volatility = np.sqrt(portfolio_variance) * np.sqrt(self.TRADING_DAYS)
             
            # Calculate the Sharpe ratio for this portfolio
            sharpe_ratio = (portfolio_return -
                            self.RISK_FREE_RATE) / portfolio_volatility

            # Store the results
            portfolio_weights.append(weights)
            portfolio_returns.append(portfolio_return)
            portfolio_volatilities.append(portfolio_volatility)
            sharpe_ratios.append(sharpe_ratio)

        return {
            "weights": portfolio_weights,
            "returns": portfolio_returns,
            "volatilities": portfolio_volatilities,
            "sharpe_ratios": sharpe_ratios
        }

    def visualize_efficient_frontier(self, simulation_results: dict, figsize_x=9, figsize_y=7):
        """
        Plots the results of the Monte Carlo simulation as an efficient frontier and calculates simulation statistics.

        :param simulation_results: Dict, the results returned from simulate().
        :param figsize_x: Int, the size of x axis of figure output.
        :param figsize_y: Int, the size of y axis of figure output.
        :return: Matplotlib graph of efficient frontier and displays simulation statistics.
        """
        weights = simulation_results["weights"]
        returns = simulation_results["returns"]
        vols = simulation_results["volatilities"]
        sharpe_ratios = simulation_results["sharpe_ratios"]
        max_sharpe_index = sharpe_ratios.index(max(sharpe_ratios))
        max_sharpe_portfolio = weights[max_sharpe_index]

        # Creating a figure with two subplots
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=[figsize_x, figsize_y])

        # Plotting the Efficient Frontier on the first subplot
        sc = ax1.scatter(vols, returns, c=sharpe_ratios, cmap='RdYlGn')
        ax1.scatter(vols[max_sharpe_index], returns[max_sharpe_index],
                    c="black", marker='*', s=500)  # Highlight the max Sharpe ratio
        ax1.set_xlabel('Volatility')
        ax1.set_ylabel('Return')
        plt.colorbar(sc, ax=ax1, label='Sharpe Ratio')
        ax1.set_title('Efficient Frontier')

        # Adding text to the second subplot
        ax2.axis('off')  # Turn off the axis for the text subplot
        max_sharpe_ratio = max(sharpe_ratios)
        s = f'Max Sharpe Ratio: {max_sharpe_ratio:.2f}\n\n'
        s += f'Portfolio Weights:\n{pd.Series(max_sharpe_portfolio * 100, index=self.portfolio.columns).to_string()}'
        ax2.text(0.5, 0.5, s, fontsize=12,
                 ha='center', va='center', wrap=True)

        plt.tight_layout()
        plt.show()

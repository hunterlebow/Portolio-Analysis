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
        

    def visualize_simulation_results(self, simulation_results):
        # Unpack simulation results
        weights = simulation_results["weights"]
        returns = simulation_results["returns"]
        vols = simulation_results["volatilities"]
        sharpe_ratios = simulation_results["sharpe_ratios"]
        max_sharpe_index = sharpe_ratios.index(max(sharpe_ratios))
        max_sharpe_weights = weights[max_sharpe_index]

        # Calculate cumulative returns
        daily_returns = self.get_pct_returns()
        weighted_returns = daily_returns * max_sharpe_weights
        portfolio_returns = weighted_returns.sum(axis=1)
        cumulative_returns = (1 + portfolio_returns).cumprod()

        # Creating a figure with a 2x2 grid layout
        fig, axs = plt.subplots(2, 2, figsize=[16, 16])

        # Plotting the Efficient Frontier on the first subplot (top left)
        sc = axs[0, 0].scatter(vols, returns, c=sharpe_ratios, cmap='RdYlGn')
        axs[0, 0].scatter(vols[max_sharpe_index], returns[max_sharpe_index],
                          c="black", marker='*', s=500)  # Highlight the max Sharpe ratio
        axs[0, 0].set_xlabel('Volatility')
        axs[0, 0].set_ylabel('Return')
        fig.colorbar(sc, ax=axs[0, 0], label='Sharpe Ratio')
        axs[0, 0].set_title('Efficient Frontier')

        # Adding text for the simulation statistics in the second subplot (top right)
        axs[0, 1].axis('off')  # Turn off the axis for the text subplot
        max_sharpe_ratio = max(sharpe_ratios)
        text_str = f'Max Sharpe Ratio: {max_sharpe_ratio:.2f}\n\n'
        text_str += f'Portfolio Weights:\n{pd.Series(max_sharpe_weights * 100, index=self.portfolio.columns).to_string()}'
        axs[0, 1].text(0.5, 0.5, text_str, fontsize=12, ha='center', va='center', wrap=True)

        # Plotting cumulative returns on the third subplot (bottom left)
        axs[1, 0].plot(cumulative_returns)
        axs[1, 0].set_title(f"Cumulative Returns of the Portfolio")
        axs[1, 0].set_xlabel("Date")
        axs[1, 0].set_ylabel("Cumulative Returns")
        axs[1, 0].grid(True)

        # Placeholder for additional plot (bottom right)
        axs[1, 1].axis('off')  # Currently turned off; replace with another plot as needed

        plt.tight_layout()
        plt.show()
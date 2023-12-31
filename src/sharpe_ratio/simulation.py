import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from .portfolio import Portfolio


class Simulation():
    def __init__(self, portfolio: Portfolio, trials: int, risk_free_rate: float) -> None:
        self.portfolio = portfolio.portfolio
        self.index_fund_portfolio = portfolio.index_fund_portfolio
        self.TRIALS = trials
        self.RISK_FREE_RATE = risk_free_rate
        self.TRADING_DAYS = 252


    def _get_pct_returns(self):
        return self.portfolio.pct_change().dropna()

    def _get_annualized_mean_returns(self):
        r = self._get_pct_returns() * self.TRADING_DAYS
        return r.mean()

    def _get_covariance_matrix(self):
        r = self._get_pct_returns()
        return r.cov()
    
    # Additional method to calculate portfolio volatility for given weights
    def _portfolio_volatility(self, weights, mean_returns, cov_matrix):
        return np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights))) * np.sqrt(self.TRADING_DAYS)

    # Additional method to minimize volatility for a given target return
    def _minimize_volatility(self, target_return, mean_returns, cov_matrix):
        num_assets = len(mean_returns)
        args = (mean_returns, cov_matrix)
        constraints = (
            {'type': 'eq', 'fun': lambda x: np.sum(x) - 1},  # Weights must sum to 1
            {'type': 'eq', 'fun': lambda x: np.dot(x, mean_returns) - target_return}  # Targeted return
        )
        bounds = tuple((0, 1) for asset in range(num_assets))
        result = minimize(self._portfolio_volatility, num_assets * [1. / num_assets], args=args,
                          method='SLSQP', bounds=bounds, constraints=constraints)
        return result

    # Method to calculate the efficient frontier
    def _efficient_frontier(self, mean_returns, cov_matrix, return_range):
        efficient_portfolios = []
        for ret in return_range:
            efficient_portfolio = self._minimize_volatility(ret, mean_returns, cov_matrix)
            if efficient_portfolio.success:
                efficient_portfolios.append(efficient_portfolio)
        return efficient_portfolios


    def simulate(self, random_seed: int = None):
        """
        Method that runs a monte carlo simulation with different weights of each investment in portfolio and monitoring how that effects returns

        :return: Dictionary with simulation results.
        """
        
        if random_seed is not None:
            if not isinstance(random_seed, int):
                raise TypeError("random_seed parameter only accepts integer arguments, you provided the argument \"{}\" which is type {}, not integer".format(random_seed, type(random_seed)))
            np.random.seed = random_seed
        # Calculate average daily returns and the covariance matrix for the assets
        annualized_mean_returns = self._get_annualized_mean_returns()
        cov_matrix = self._get_covariance_matrix()

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
            "sharpe_ratios": sharpe_ratios,
            "random_seed": random_seed
        }
        

    def visualize_simulation_results(self, simulation_results):
        # Unpack simulation results
        weights = simulation_results["weights"]
        returns = simulation_results["returns"]
        vols = simulation_results["volatilities"]
        sharpe_ratios = simulation_results["sharpe_ratios"]
        max_sharpe_index = sharpe_ratios.index(max(sharpe_ratios))
        max_sharpe_weights = weights[max_sharpe_index]

        # Creating a figure with a 2x2 grid layout
        fig, axs = plt.subplots(2, 2, figsize=[16, 10], facecolor="white")

        # Plotting the Efficient Frontier on the first subplot (top left)
        sc = axs[0, 0].scatter(vols, returns, c=sharpe_ratios, cmap='RdYlGn')
        axs[0, 0].scatter(vols[max_sharpe_index], returns[max_sharpe_index],
                          c="#FF7FFF", marker='*', s=500, label="Max Sharpe Ratio")  # Highlight the max Sharpe ratio
        axs[0, 0].set_xlabel('Volatility')
        axs[0, 0].set_ylabel('Return')
        fig.colorbar(sc, ax=axs[0, 0], label='Sharpe Ratio')
        axs[0, 0].set_title('Monte Carlo Portfolio Weight Simulation')
        # Add Sharpe Ratio text to the star marker in axs[0,0]
        max_sharpe_ratio = max(sharpe_ratios)
        
        max_sharpe_point = (vols[max_sharpe_index], returns[max_sharpe_index])
        axs[0, 0].annotate(f'{max_sharpe_ratio:.2f}', 
                        xy=max_sharpe_point, 
                        xytext=(15,15), 
                        textcoords='offset points', 
                        arrowprops=dict(arrowstyle='->', color='black'),
                        fontsize=12,
                        color='black')

        axs[0,0].grid(True)
        axs[0,0].legend()

        # Monte Carlo Simulation Statistics
        # Plot cumulative returns in axs[0,1]
        # Identify the maximum Sharpe ratio portfolio
        max_sharpe_portfolio_weights = weights[max_sharpe_index]

        # Compute the weighted returns for the max Sharpe ratio portfolio
        max_sharpe_weighted_returns = (self.portfolio.pct_change() * max_sharpe_portfolio_weights).sum(axis=1)
        
        # Compute the cumulative returns for the max Sharpe ratio portfolio
        max_sharpe_cumulative_returns = (1 + max_sharpe_weighted_returns).cumprod()


        # Plot the cumulative returns on axs[0, 1]
            # Plot cumulative returns for the max Sharpe ratio portfolio
        axs[0, 1].plot(max_sharpe_cumulative_returns, label='Max Sharpe Portfolio')

        # Iterate over each index fund and plot its cumulative returns
        for fund in self.index_fund_portfolio.columns:
            fund_cumulative_returns = (1 + self.index_fund_portfolio[fund].pct_change()).cumprod()
            axs[0, 1].plot(fund_cumulative_returns, label=f'{fund} Index Fund')
        axs[0, 1].set_title('Cumulative Returns Comparison')
        axs[0, 1].legend()
        # axs[0, 1].axis('off')  # Turn off the axis for the text subplot

        # # Format portfolio weights as strings with two decimal points and a percentage sign
        # formatted_weights = pd.Series(max_sharpe_weights * 100, index=self.portfolio.columns).sort_values(ascending=False).map('{:.2f}%'.format)

        #         # Text for the Simulation Statistics Header
        # header_text = "Simulation Statistics"
        # axs[0, 1].text(0.5, 0.97, header_text, fontsize=20, ha='center', va='center', fontweight='bold')

        
        # axs[0, 1].text(0.02, 0.85, "Top Simulated Portfolio", fontsize=16, ha='left', va='center', fontweight='bold')

        # # Text for the Highest Sharpe Ratio
        # sharpe_text = f"Sharpe Ratio: {max_sharpe_ratio:.2f}"
        # axs[0, 1].text(0.06, 0.79, sharpe_text, fontsize=12, ha='left', va='center')
        # axs[0, 1].text(0.06, 0.73, f"This portfolio returned {max_sharpe_ratio:.2f} units of risk-adjusted returns per 1 unit of risk.", fontsize=10, ha='left', va='center')


        # # Text for Portfolio Asset Composition Header
        # composition_header = "Asset Composition:"
        # axs[0, 1].text(0.02, 0.63, composition_header, fontsize=16, ha='left', va='center', fontweight='bold')

        # # Asset Weights List
        # asset_list_start = 0.57  # Starting vertical position for the list
        # for stock, weight in formatted_weights.items():
        #     axs[0, 1].text(0.06, asset_list_start, f'{stock}: {weight}', fontsize=12, ha='left', va='center')
        #     asset_list_start -= 0.06  # Adjust for spacing between lines

        # # Simulation Parameters in smaller text at the bottom

        
       # Calculate annualized mean returns and covariance matrix
        annualized_mean_returns = self._get_annualized_mean_returns()
        cov_matrix = self._get_covariance_matrix()

        # Determine the range of return values for the efficient frontier
        min_return = min(simulation_results['returns'])
        max_return = max(simulation_results['returns'])
        return_range = np.linspace(min_return, max_return, 100)

        # Calculate the Efficient Frontier
        efficient_portfolios = self._efficient_frontier(annualized_mean_returns, cov_matrix, return_range)
        efficient_returns = [np.dot(portfolio.x, annualized_mean_returns) for portfolio in efficient_portfolios]
        efficient_volatilities = [portfolio.fun for portfolio in efficient_portfolios]

        # Plot the Efficient Frontier on the bottom right subplot (axs[1, 1])
        axs[1, 0].plot(efficient_volatilities, efficient_returns, 'b--', linewidth=2, label='Efficient Frontier')
        axs[1, 0].set_title('Markowitz Efficient Frontier')
        axs[1, 0].set_xlabel('Volatility (Standard Deviation)')
        axs[1, 0].set_ylabel('Expected Return')
        axs[1, 0].grid(True)
        axs[1, 0].legend()
        
        # Plot the Monte Carlo simulation results
        sc = axs[1, 1].scatter(simulation_results['volatilities'], simulation_results['returns'], c=simulation_results['sharpe_ratios'], cmap='RdYlGn', label='Monte Carlo')
        # Highlight the maximum Sharpe ratio from the simulation
        axs[1, 1].scatter(simulation_results['volatilities'][max_sharpe_index], simulation_results['returns'][max_sharpe_index], c='#FF7FFF', marker='*', s=500, label='Max Sharpe Ratio')
        # Plot the Markowitz Efficient Frontier curve
        axs[1, 1].plot(efficient_volatilities, efficient_returns, 'b--', linewidth=2, label='Efficient Frontier')

        axs[1, 1].set_title('Efficient Frontier with Monte Carlo Simulation')
        axs[1, 1].set_xlabel('Volatility (Standard Deviation)')
        axs[1, 1].set_ylabel('Expected Annual Return')
        axs[1, 1].legend()
        axs[1, 1].grid(True)
        
        params_text = f"Simulation Arguments: Start Date: {self.portfolio.index[0]} | Trials: {self.TRIALS} | Risk-Free Rate: {self.RISK_FREE_RATE:.2%} | Random Seed: {simulation_results['random_seed']}"

        # x and y are the coordinates in figure space, where (0, 0) is the bottom left and (1, 1) is the top right
        fig.text(0.05, 0.02, params_text, fontsize=10, ha='left', va='bottom')


        # Show the plot
        plt.tight_layout()
        plt.show()
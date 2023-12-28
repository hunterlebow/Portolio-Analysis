from data_processing.investments import read_tickers
from sharpe_ratio.portfolio import Portfolio
from sharpe_ratio.simulation import Simulation


def main():

    portfolio = Portfolio(start_date="2023-01-01", investments=read_tickers())
    portfolio.build_portfolio()

    simulator = Simulation(portfolio=portfolio.portfolio,
                           trials=10000, risk_free_rate=0.03)
    simulation_results = simulator.simulate()
    simulator.visualize_simulation_results(
        simulation_results=simulation_results)

if __name__ == "__main__":
    main()

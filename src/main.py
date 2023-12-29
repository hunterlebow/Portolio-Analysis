from sharpe_ratio.portfolio import Portfolio
from sharpe_ratio.simulation import Simulation
import os


def main():
    data = Portfolio(start_date="2022-01-01")
    data.build_portfolio(ticker_updates={"FB":"META"})

    simulator = Simulation(portfolio=data,
                           trials=10000, 
                           risk_free_rate=0.03)
    
    simulation_results = simulator.simulate()
    
    simulator.visualize_simulation_results(
        simulation_results=simulation_results)

if __name__ == "__main__":
    main()

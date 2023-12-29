# Stock Portfolio Analysis Project

## Overview
The Stock Portfolio Analysis Project is a comprehensive tool designed to offer insightful analysis and visualization of stock portfolios. Leveraging historical stock price data, this project empowers investors to make informed decisions by simulating various portfolio combinations and evaluating their performance against key financial metrics.

## Features
- **Monte Carlo Simulation**: Runs extensive simulations to generate a range of possible portfolios, providing a broad view of potential outcomes based on historical data.
- **Sharpe Ratio Calculation**: Computes the Sharpe Ratio for each simulated portfolio, allowing investors to understand the risk-adjusted return and make comparisons between different investment strategies.
- **Markowitz Efficient Frontier**: Implements Markowitz Portfolio Theory to identify the set of optimal portfolios that offer the highest expected return for a given level of risk. This feature visualizes the trade-off between risk and return, aiding in the selection of the most efficient portfolio.

- **Interactive Visualization**: Offers detailed visual representations including:
    - A scatter plot of the Monte Carlo simulation results, colored by Sharpe Ratio.
    - Monte Carlo simulation statistics, displaying the optimal weights of each asset comprising the portfolio that yielded the highest Sharpe Ratio.
    - The Markowitz Efficient Frontier curve, highlighting the optimal risk-return balance.
    - An overlay of the Efficient Frontier over the Monte Carlo simulation results for comparative analysis.

## Technologies Used
- **Python**: Primary programming language for data analysis and visualization.
- **Polygon API**: Used to programatically retrieve historical data. Visit Polygon at https://polygon.io/
- **Pandas**: Used for efficient data manipulation and analysis.
- **NumPy**: Fundamental package for numerical computation in Python.
- **Matplotlib**: Python plotting library for creating static, interactive, and animated visualizations.
- **SciPy**: Used for scientific and technical computing, particularly the optimization functions to compute the Efficient Frontier.

## Getting Started
To use this project, clone the repository and install the required Python packages listed in `requirements.txt`. Ensure you have access to your own Polygon API key.  

Set self.API_KEY equal to your own Polygon API secret key in src/data_procesing/polygon_api.py

```python
class Polygon():
    def __init__(self):
        load_dotenv()
        self.API_KEY = os.getenv("POLYGON_API_KEY")
```

Or create a .env file in root directory and add the following code:


	POLYGON_API_KEY=add your own secret key here

## Usage
The project is structured into classes and functions that can be easily integrated into your investment analysis workflow. Customize the parameters such as portfolio composition, number of trials for Monte Carlo simulation, and risk-free rate as per your requirement. Run the simulation and visualize the results to gain insights into the potential performance and risk of your stock portfolio.

## License
This project is open source and available under the [MIT License](LICENSE.md).

## Disclaimer
This tool is for informational purposes only and does not constitute financial advice. Always conduct your own research and consult with a financial advisor before making investment decisions.

---

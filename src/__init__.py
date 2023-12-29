"""This is the docstring for the src package."""

# Importing classes from submodules for easy access
from .sharpe_ratio.portfolio import Portfolio
from .sharpe_ratio.simulation import Simulation
from .data_processing.polygon_api import Polygon

# Defining what gets imported with "from data_processing import *"
__all__ = ['Portfolio', 'Simulation', 'Polygon', 'read_tickers']


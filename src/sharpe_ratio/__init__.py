"""This is the docstring for the sharpe_ratio package."""

# Importing classes from submodules for easy access
from .portfolio import Portfolio
from .simulation import Simulation

# Defining what gets imported with "from data_processing import *"
__all__ = ['Portfolio', 'Simulation']

# Package initialization code
print("Initializing sharpe_ratio package")

"""This is the docstring for the data_processing package."""

# Importing classes from submodules for easy access
from .polygon_api import Polygon
from .investments import read_tickers

# Defining what gets imported with "from data_processing import *"
__all__ = ['Polygon', 'read_tickers']

# Package initialization code
print("Initializing data_processing package")

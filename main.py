# Install Pandas, Numpy, Matplotlib, seaborn and pyjstat, DID NOT INSTALL REQUESTS FOR API
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pyjstat import pyjstat
import matplotlib as mpl

# Create a function to read the car sales csv's
carsales_all=pd.read_csv("TEA18.20210615T100603.csv",delimiter=',', quotechar='"', index_col=0)
# Check the csv files are consistent in format
print(carsales_all.head())
print(carsales_all.info())
print(carsales_all.shape)
missing_values_count = carsales_all.isnull().sum()
print(missing_values_count[0:7])
carsales_all.to_csv("carsales_all.csv")
# Delete for blank value
carsales_all= carsales_all.dropna()
print(carsales_all.shape)

# From column Statistics Delete Rows all private Cars
# from column Engine Capacity cc delete rows All engine capacities with respect to private cars (cc
# From column car make delete rows all makes
# From column emission band delete column all bands
# From column Licensing Authority delete columns All licensing Authorities
# Delete column number
# Set index to county


# Add a line graph by year and sales


# Add a stacked bar chart per year imports and new registrations

# Add a diagram by county

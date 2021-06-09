# Install Pandas, Numpy, Matplotlib, seaborn and pyjstat, DID NOT INSTALL REQUESTS FOR API
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pyjstat import pyjstat
import matplotlib as mpl

# Create a function to read the car sales csv's
carsales2015=pd.read_csv("passenger cars 2015.csv",delimiter=',', quotechar='"', index_col=0)
carsales2016=pd.read_csv("passenger cars 2016.csv",delimiter=',', quotechar='"', index_col=0)
carsales2017=pd.read_csv("passenger cars 2017.csv",delimiter=',', quotechar='"', index_col=0)
carsales2018=pd.read_csv("passenger cars 2018.csv",delimiter=',', quotechar='"', index_col=0)
carsales2019=pd.read_csv("passenger cars 2019.csv",delimiter=',', quotechar='"', index_col=0)
# Check the csv files are consistent in format
print(carsales2015.head())
print(carsales2016.head())
print(carsales2017.head())
print(carsales2018.head())
print(carsales2019.head())
# Join the car sales csv's into one dataframe using concat
carsales_all= pd.concat([carsales2015, carsales2016, carsales2017, carsales2018, carsales2019])
# Check for missing values and remove
print(carsales_all.info())
print(carsales_all.shape)
missing_values_count = carsales_all.isnull().sum()
print(missing_values_count[0:5])
carsales_all.to_csv("carsales_all.csv")
# Delete for kissing values
carsales_all= carsales_all.dropna()
print(carsales_all.shape)
carsales_all=carsales_all.reset_index()
print(carsales_all.head())
print(carsales_all.dtypes)
# Change Year column datatype to a string.
carsales_all["Year"]=carsales_all["Year"].astype(np.int64)
carsales_all["Year"]=carsales_all["Year"].astype(str)
# carsales_all["Car registration count"]=carsales_all["Car registration count"].astype(int)
print(carsales_all.dtypes)
# Create a column called period for the month and the year.
carsales_all["Period"]=carsales_all['Month'].astype(str) +" "+ carsales_all['Year']
print(carsales_all.dtypes)
print(carsales_all.head())
carsales_all_year_by_type=carsales_all.groupby("Year")["Car registration count"].sum()

print(carsales_all_year_by_type.head())

# Add a line graph


# Add a stacked bar chart per year.

# carsales_all["Car registration count"]=carsales_all["Car registration count"].astype(int(float("car registration count")))


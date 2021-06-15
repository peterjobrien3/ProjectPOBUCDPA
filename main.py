# Install Pandas, Numpy, Matplotlib, seaborn and pyjstat, DID NOT INSTALL REQUESTS FOR API
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pyjstat import pyjstat




# Create a function to read the car sales csv's
carsales_all=pd.read_csv("TEA18.20210615T100603.csv",delimiter=',', quotechar='"')
# Check the csv file
print(carsales_all.head())
print(carsales_all.info())
print(carsales_all.shape)
# Rename column 'Licensing Authority' to 'county' and 'VALUE' to 'car_count'
carsales_all.rename(columns={'VALUE':'car_count'}, inplace=True)
carsales_all.rename(columns={'Licensing Authority':'county'}, inplace=True)
# Check for missing values and delete rows
missing_values_count = carsales_all.isnull().sum()
print(missing_values_count[0:8])
carsales_all= carsales_all.dropna()
print(carsales_all.shape)
# Drop columns 'Car Make' and 'UNIT' NOTE: inplace=True
carsales_all.drop(['Car Make','UNIT'], axis=1, inplace=True)
# From column 'Statistic' exclude rows 'All Private Cars'
carsales_all_rev1=carsales_all.loc[carsales_all["Statistic"]!="All Private Cars"]
# from column 'Engine Capacity cc' exclude rows 'All engine capacities with respect to private cars (cc)'
carsales_all_rev2=carsales_all_rev1.loc[carsales_all_rev1["Engine Capacity cc"]!="All engine capacities with respect to private cars (cc)"]
# From column 'Emission Band' exclude rows all bands
carsales_all_rev3=carsales_all_rev2.loc[carsales_all_rev2["Emission Band"]!="All bands"]
# From column 'county' exclude rows 'All licensing authorities'
carsales_all_clean=carsales_all_rev3.loc[carsales_all_rev3["county"]!="All licensing authorities"]
# Check the database including Export to csv
print(carsales_all_clean.head())
print(carsales_all_clean.info())
print(carsales_all_clean.shape)
carsales_all_clean.to_csv("carsales_all_clean.csv")
# Pivot the car sales data by year and car type
carsales_pivot=carsales_all_clean.pivot_table(values="car_count",index="Year",columns="Statistic",aggfunc=np.sum)
print(carsales_pivot)
# Plot the pivot table into a stacked bar chart.
carsales_pivot.plot.bar(stacked=True).legend(loc='best', title="Car Type")
plt.xticks(rotation=30, horizontalalignment="center")
plt.title("Private Car Sales per Year")
plt.xlabel("Year")
plt.ylabel("car_count")
plt.show()
# Set the index of carsales_all_clean to county, subset for "new private cars only"
carsales_all_county=carsales_all_clean.set_index("county")
carsales_new_county=carsales_all_county.loc[carsales_all_county["Statistic"]=="New Private Cars"]
print(carsales_new_county.head())
print(carsales_new_county.info())
# New private cars grouped by county and the mean calculated per county over the 5 years 2015 to 2019.
carsales_new_county_avg= carsales_new_county.groupby("county")[["car_count"]].mean()
carsales_new_county_avg.sort_values('county', ascending=False)
print(carsales_new_county_avg)
# Add a horizontal bar chart with avg new private cars per county over the 5 years
carsales_new_county_avg['car_count'].plot(kind="barh")
plt.xticks(rotation=30, horizontalalignment="center")
plt.title("Average Private Car Sales per County 2015 to 2019")
plt.xlabel("Average Private Car Sales Per Annum")
plt.ylabel("County")
plt.show()
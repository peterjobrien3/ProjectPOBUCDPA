# Install Pandas, Numpy, Matplotlib, seaborn and pyjstat, DID NOT INSTALL REQUESTS FOR API
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pyjstat import pyjstat
# POPULATION ANALYSIS
# Assign URL to variable: url
url = 'https://ws.cso.ie/public/api.restful/PxStat.Data.Cube_API.ReadDataset/E2049/JSON-stat/2.0/en'
# Get the dataset using pyjstat
census_dataset = pyjstat.Dataset.read(url)
# Write the dataset to a dataframe.
census_df=census_dataset.write('dataframe')
# Review the dataframe using print, head, shape & info
print(census_df)
print(census_df.head())
print(census_df.shape)
print(census_df.info())
# Check the columns for any missing data
print(census_df.isna().any())
# Subset for 2016 census data only
census_2016=census_df[census_df["CensusYear"].isin(["2016"])]
print(census_2016)
# Set the index of census_2016 to County & print head
census_2016_co=census_2016.set_index("County")
print(census_2016_co.head())
# Save as a csv and check for non applicable rows.
census_2016_co.to_csv("census2016_co.csv")
# Delete "State" in column "County" (index Column use .drop)
census_2016_co=census_2016_co.drop(labels="State", axis=0)
# Exclude "Both sexes" in column "Sex".
census_2016_co=census_2016_co.loc[census_2016_co["Sex"]!="Both sexes"]
# Exclude "All ages" column in "Age Group".
census_2016_co_clean=census_2016_co.loc[census_2016_co["Age Group"]!="All ages"]
# Check the dataframe using shape and info
print(census_2016_co_clean.shape)
print(census_2016_co_clean.head())
# Population Statistics, population by County, population by Age Group & Total Population, Group population by County
population_stats_county=census_2016_co_clean.groupby("County")["value"].agg([np.min, np.max, np.mean, np.median])
print(population_stats_county)
population_stats_age_group=census_2016_co_clean.groupby("Age Group")["value"].agg([np.min, np.max, np.mean, np.median])
print(population_stats_age_group)
population_total=census_2016_co_clean["value"].sum()
print("Total Population Census 2016 ="+str(population_total))
population_by_county=census_2016_co_clean.groupby("County")["value"].sum()
# Create a dataframe of population by county insert the column of the percentage of the total and sort descending.
population_by_county_df=pd.DataFrame(population_by_county)
population_by_county_df['%'] = ((population_by_county_df['value'] / population_by_county_df['value'].sum())*100).round(2).astype(str) + '%'
population_by_county_df=population_by_county_df.sort_values("value",ascending=False)
print(population_by_county_df)
# Create a dataframe of population by county, define the index order when creating the dataframe, insert a column of the percentage of the total.
population_by_agegroup=census_2016_co_clean.groupby("Age Group")["value"].sum()
population_by_agegroup_df=pd.DataFrame(population_by_agegroup,index=['0 - 4 years','5 - 9 years','10 - 14 years','15 - 19 years','20 - 24 years','25 - 29 years','30 - 34 years','35 - 39 years','40 - 44 years','45 - 49 years','50 - 54 years','55 - 59 years','60 - 64 years','65 - 69 years','70 - 74 years','75 - 79 years','80 - 84 years','85 years and over'
])
print(population_by_agegroup_df)
population_by_agegroup=census_2016_co_clean.groupby("Age Group")["value"].sum()
# Population by age group as a bar chart
population_by_county.plot(x="County", y="Population in Millions", kind="bar",rot=45, title="Population by County - Cenusus 2016")
plt.show()
# Plot Age group as a percentage of population as a Pie chart
population_by_agegroup_df.plot(kind="pie", subplots=True, legend=False, title="Population by Age Group - 2016 Census")
plt.show()
# Remove the index and Pivot the dataset
census_2016_co_clean=census_2016_co_clean.reset_index()
census_2016_pivot=census_2016_co_clean.pivot_table(values="value",index="County",columns="Age Group",aggfunc=np.sum,margins=False)
# Show census 2016 as a percentage of total population by age group by county in a 100% stacked  bar chart.
census_2016_percentage = census_2016_pivot.apply(lambda x: x*100/sum(x), axis=1)
print(census_2016_percentage)
census_2016_percentage.plot(kind="bar", stacked=True)
plt.title("Percentage of Population by Age Group by County", weight="bold", size=14)
plt.legend(bbox_to_anchor=(1.0, 1.05))
plt.xlabel("County")
plt.ylabel("Age Group (%)")
plt.show()
# Remove non car buying age groups, defined as excluding ages 0 to 19 and 80 & Over.
census_2016_carbuyers_percentage=census_2016_percentage.drop(['0 - 4 years','5 - 9 years','10 - 14 years','15 - 19 years','80 - 84 years','85 years and over'],axis=1)
print(census_2016_carbuyers_percentage.info())
# Re-plot the Data on the stacked bar chart showing the car buying Age Groups Only
census_2016_carbuyers_percentage.plot(kind="bar", stacked=True)
plt.title("Percentage of Population by Car Buying Age Group by County",weight="bold", size=14)
plt.legend(bbox_to_anchor=(1.0, 1.05))
plt.xlabel("County")
plt.ylabel("Car Buying Age Group (%)")
plt.show()
# CAR SALES ANALYSIS
# Create a function to read the car sales csv's
carsales_all=pd.read_csv("TEA18.20210616T120658.csv",delimiter=',', quotechar='"')
# Check the csv file
print(carsales_all.head())
print(carsales_all.info())
print(carsales_all.shape)
# Rename column 'Licensing Authority' to 'county' and 'VALUE' to 'car_count'
carsales_all.rename(columns={'VALUE':'car_count'}, inplace=True)
carsales_all.rename(columns={'Licensing Authority':'County'}, inplace=True)
# Check for missing values and delete rows
missing_values_count = carsales_all.isnull().sum()
print(missing_values_count[0:8])
carsales_all= carsales_all.dropna()
print(carsales_all.shape)
# Drop column 'UNIT' NOTE: inplace=True
carsales_all.drop(['UNIT'], axis=1, inplace=True)
# From column 'Statistic' exclude rows 'All Private Cars'
carsales_all_rev1=carsales_all.loc[carsales_all["Statistic"]!="All Private Cars"]
# from column 'Car Make' exclude rows 'All Makes'
carsales_all_rev2=carsales_all_rev1.loc[carsales_all_rev1["Car Make"]!="All makes"]
# From column 'county' exclude rows 'All licensing authorities'
carsales_all_clean_rev3=carsales_all_rev2.loc[carsales_all_rev2["County"]!="All licensing authorities"]
carsales_all_clean=carsales_all_clean_rev3.set_index('Year')
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
plt.title("Private Car Sales per Year", weight="bold", size=14)
plt.ylabel("Car Count")
plt.xlabel('')
plt.show()
# Plot the pivot table into a line graph using seaborn
# sns.relplot(x="Year", y="car_count", data=carsales_pivot.plot, kind="line", style="Statistic")
# Itterate for rows using pivot for car sales
# for index, row in carsales_pivot.iterrows():

# Plot a line graph by Car Type and Year.
carsales_pivot.plot.line(marker='o', linewidth=4)
plt.title("Private Car Sales per Year", weight="bold", size=14)
plt.grid(True)
plt.ylabel("Car Count")
plt.xlabel('')
plt.show()
# Set the index of carsales_all_clean to county, subset for "new private cars only"
carsales_all_county=carsales_all_clean.set_index("County")
carsales_new_county=carsales_all_county.loc[carsales_all_county["Statistic"]=="New Private Cars"]
print(carsales_new_county.head())
print(carsales_new_county.info())
# New private cars grouped by county and the mean calculated per county over the 5 years 2015 to 2019.
carsales_new_county_avg= carsales_new_county.groupby("County")[["car_count"]].mean()
carsales_new_county_avg.sort_values('County', ascending=False)
print(carsales_new_county_avg)
# Add a horizontal bar chart with avg new private cars per county over the 5 years
carsales_new_county_avg['car_count'].plot(kind="barh")
plt.xticks(rotation=30, horizontalalignment="center")
plt.title("Average Private Car Sales per County 2015 to 2019", weight="bold", size=14)
plt.xlabel("Average Private Car Sales Per Annum")
plt.ylabel("County")
plt.show()
# MERGE DATA ANALYSE & VISUALISE
# Group Car sales by County & type for 2019 only
print(carsales_all_clean.info())
carsales_all_2019=carsales_all_clean.loc[2019,['Statistic','County','car_count']]
carsales_all_2019.to_csv('carsales_2019_only.csv')
carsales_type_county_2019=carsales_all_2019.pivot_table(values="car_count",index="County",columns="Statistic",aggfunc=np.sum)
# Get the total population by county
population_by_county_carbuyers=census_2016_pivot.drop(['0 - 4 years','5 - 9 years','10 - 14 years','15 - 19 years','80 - 84 years','85 years and over'],axis=1)
print(population_by_county_carbuyers.info())
# Add a column 'Total_Pop_CarBuying_Age' and sum all age groups.
cols_to_sum = population_by_county_carbuyers.columns[ : population_by_county_carbuyers.shape[1]]
population_by_county_carbuyers['Total_Pop-CarBuying_Age'] = population_by_county_carbuyers[cols_to_sum].sum(axis=1)
# Remove individual Age Groups columns
population_by_county_carbuyers_totals= population_by_county_carbuyers.drop(population_by_county_carbuyers.columns[0:12], axis=1)
# Check the data and see how we can merge
print(carsales_type_county_2019.info())
print(population_by_county_carbuyers_totals.info())
# Merge the data using pd.merge
pop_carsales2019_merged= pd.merge(population_by_county_carbuyers_totals,carsales_type_county_2019,on='County')
# Check the data post merge
print(pop_carsales2019_merged.head())
print(pop_carsales2019_merged.info())
pop_carsales2019_merged.to_csv('pop_carsales2019_merged.csv')
# Add 1 columns Total Private cars and 3 columns of new cars, second hand cars and total cars bought per capita
pop_carsales2019_merged['Total Private Cars']=pop_carsales2019_merged['New Private Cars']+pop_carsales2019_merged['Second Hand Private Cars']

print(pop_carsales2019_merged.head())
print(pop_carsales2019_merged.info())

# Graph the data gep graph using seaborn
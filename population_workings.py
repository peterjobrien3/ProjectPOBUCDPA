# Install Pandas, Numpy and Matplotlib and pyjstat, DID NOT INSTALL REQUESTS FOR API
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pyjstat import pyjstat

# Assign URL to variable: url
url = 'https://ws.cso.ie/public/api.restful/PxStat.Data.Cube_API.ReadDataset/E2049/JSON-stat/2.0/en'
# Get the dataset using pyjstat
census_dataset=pyjstat.Dataset.read(url)
# Write the dataset to a dataframe and print it.
census_df=census_dataset.write('dataframe')
print(census_df)
# print the head of the dataframe
print(census_df.head())
# View the shape of the dataframe
print(census_df.shape)
# View the information on the dataframe
print(census_df.info())
# Check the columns for any missing data
print(census_df.isna().any())
# Subset for 2016 census data only
census_2016=census_df[census_df["CensusYear"].isin(["2016"])]
print(census_2016)
# Set the index of census_2016 to County
census_2016_co=census_2016.set_index("County")
print(census_2016_co.head())
# Save as a csv and check for non applicable rows.
census_2016_co.to_csv("census2016_co.csv")
print(census_2016_co.shape)
# Delete "State" in column "County" (index Column use .drop)
census_2016_co=census_2016_co.drop(labels="State", axis=0)
print(census_2016_co.shape)
# Exclude "Both sexes" in column "Sex".
census_2016_co=census_2016_co.loc[census_2016_co["Sex"]!="Both sexes"]
print(census_2016_co.shape)
# Exclude "All ages" column in "Age Group".
census_2016_co_clean=census_2016_co.loc[census_2016_co["Age Group"]!="All ages"]
print(census_2016_co_clean.shape)
# Population Statistics
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
# Create a dataframe of population by county, define the index order when creating the dataframe, insert a column of the percentage of the total
population_by_agegroup=census_2016_co_clean.groupby("Age Group")["value"].sum()
population_by_agegroup_df=pd.DataFrame(population_by_agegroup,index=['0 - 4 years','5 - 9 years','10 - 14 years','15 - 19 years','20 - 24 years','25 - 29 years','30 - 34 years','35 - 39 years','40 - 44 years','45 - 49 years','50 - 54 years','55 - 59 years','60 - 64 years','65 - 69 years','70 - 74 years','75 - 79 years','80 - 84 years','85 years and over'
])
population_by_agegroup_df['%'] = ((population_by_agegroup_df['value'] / population_by_agegroup_df['value'].sum())*100).round(2).astype(str) + '%'
print(population_by_agegroup_df)
# Population by age group as a bar chart
population_by_county.plot(x="County", y="Population in Millions", kind="bar",rot=45, title="Population by County - Cenusus 2016")
plt.show()
# Age group as a percentage of population bar chart Pie chart
population_by_agegroup.plot(kind="pie", subplots=True, title="Population by Age Group - 2016 Census")
plt.show()
# Remove the index and Pivot the dataset
census_2016_co_clean=census_2016_co_clean.reset_index()
census_2016_pivot=census_2016_co_clean.pivot_table(values="value",index="County",columns="Age Group",aggfunc=np.sum,margins=True)
# Add percentage columns to the datset for each age group
census_2016_pivot['0 - 4 years %'] = ((census_2016_pivot['0 - 4 years'] / census_2016_pivot['All'])*100).round(2).astype(str) + '%'
census_2016_pivot['5 - 9 years %'] = ((census_2016_pivot['5 - 9 years'] / census_2016_pivot['All'])*100).round(2).astype(str) + '%'
census_2016_pivot['10 - 14 years %'] = ((census_2016_pivot['10 - 14 years'] / census_2016_pivot['All'])*100).round(2).astype(str) + '%'
census_2016_pivot['15 - 19 years %'] = ((census_2016_pivot['15 - 19 years'] / census_2016_pivot['All'])*100).round(2).astype(str) + '%'
census_2016_pivot['20 - 24 years %'] = ((census_2016_pivot['20 - 24 years'] / census_2016_pivot['All'])*100).round(2).astype(str) + '%'
census_2016_pivot['25 - 29 years %'] = ((census_2016_pivot['25 - 29 years'] / census_2016_pivot['All'])*100).round(2).astype(str) + '%'
census_2016_pivot['30 - 34 years %'] = ((census_2016_pivot['30 - 34 years'] / census_2016_pivot['All'])*100).round(2).astype(str) + '%'
census_2016_pivot['35 - 39 years %'] = ((census_2016_pivot['35 - 39 years'] / census_2016_pivot['All'])*100).round(2).astype(str) + '%'
census_2016_pivot['40 - 44 years %'] = ((census_2016_pivot['40 - 44 years'] / census_2016_pivot['All'])*100).round(2).astype(str) + '%'
census_2016_pivot['45 - 49 years %'] = ((census_2016_pivot['45 - 49 years'] / census_2016_pivot['All'])*100).round(2).astype(str) + '%'
census_2016_pivot['50 - 54 years %'] = ((census_2016_pivot['50 - 54 years'] / census_2016_pivot['All'])*100).round(2).astype(str) + '%'
census_2016_pivot['55 - 59 years %'] = ((census_2016_pivot['55 - 59 years'] / census_2016_pivot['All'])*100).round(2).astype(str) + '%'
census_2016_pivot['60 - 64 years %'] = ((census_2016_pivot['60 - 64 years'] / census_2016_pivot['All'])*100).round(2).astype(str) + '%'
census_2016_pivot['65 - 69 years %'] = ((census_2016_pivot['65 - 69 years'] / census_2016_pivot['All'])*100).round(2).astype(str) + '%'
census_2016_pivot['75 - 79 years %'] = ((census_2016_pivot['75 - 79 years'] / census_2016_pivot['All'])*100).round(2).astype(str) + '%'
census_2016_pivot['80 - 84 years %'] = ((census_2016_pivot['80 - 84 years'] / census_2016_pivot['All'])*100).round(2).astype(str) + '%'
census_2016_pivot['85 years and over %'] = ((census_2016_pivot['85 years and over'] / census_2016_pivot['All'])*100).round(2).astype(str) + '%'
census_2016_pivot=census_2016_pivot.reset_index()
print(census_2016_pivot.info())
# Delete columns 1-19 from the pivot table
census_2016_pivot.drop(census_2016_pivot.columns[1:20], axis=1, inplace=True)
print(census_2016_pivot.info())
census_2016_pivot.to_csv("census2016_pivot.csv")
census_2016_pivot_dist=census_2016_pivot.loc[census_2016_pivot["County"]!="All"]
print(census_2016_pivot_dist)
# Show the profile of age by county Horizontal bar chart stacked.
# sns.set_theme(style="whitegrid")
# sns.set_color_codes("pastel")
# sns.barplot(x="0 - 4 years %", y="County", data=census_2016_pivot_dist)
# plt.show()


# population_distribution = sns.load_dataset("census_2016_pivot_dist").sort_values("County", ascending=False)
# Check for loop for adding a column.

# What is the county with the highest % of young people, what is the county with the highest percentage of old people.
# Extract non car buying age groups.
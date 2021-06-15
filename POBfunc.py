


import csv

answer = 0
with open('filename&path') as infile:
    for line in csv.reader(infile, delimiter=','):
        nums = (int(i) for i in line[5:])
        answer += sum(nums)
print(answer)

# carsales2015=pd.read_csv("passenger cars 2015.csv",delimiter=',', quotechar='"', index_col=0)

# print(df[df.Price.str.replace('$','').astype(float)

# Another option
# df["Price"].str.replace("$", "")

# Another option
for i, row in df.iterrows():
    rating = float(row.Rating)
    price = float(row.Price.str.replace('$', ''))

# Another Option
# print(carsales_all[carsales_all.str.replace(',','').astype(int)
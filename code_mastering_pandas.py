import pandas as pd
import os
import matplotlib.pyplot as plt

# First, randomly read individual datasets to get an idea of columns and types of datasets to be merged
#df_jan = pd.read_csv("Sales_Data/Sales_January_2019.csv")
#df_jan.head()

# Task 1: Merge 12 datafiles into a single dataframe
files = [file for file in os.listdir("C:/Users/my-g-/Desktop/Python/mastering_Pandas/SalesAnalysis/Sales_Data")]

all_months_data = pd.DataFrame()

for file in files:
    # print(file) # To print file names
    df = pd.read_csv("C:/Users/my-g-/Desktop/Python/mastering_Pandas/SalesAnalysis/Sales_Data/" + file)
    all_months_data = pd.concat([all_months_data, df])

all_months_data.to_csv("all_months_data.csv", index=False)

# Read the data
df = pd.read_csv("all_months_data.csv")
# Read and rename the dataframe to an easy to write title


# Get the list of columns - check whether unnecessary columns are added in the final dataset.
df
# Or alternatively, use this command
print(df.columns)



# Task 2: (Q) What was the best month for sales? And how much was earned that month?

# First, lets create a column "month". To do that, lets apply datetime to Order Date
df["Order Date"] =  pd.to_datetime(df["Order Date"], infer_datetime_format=True, errors='coerce')
df['month'] = pd.DatetimeIndex(df['Order Date']).month
df['year'] = pd.DatetimeIndex(df['Order Date']).year

# Finding how many missing values are there for each column
df.isnull().sum()
pd.isna(df).sum()
# df = df[pd.notnull(df["Order ID"])]

# Drop NANs
df=df.dropna()
df.shape

df["Order Date2"]=df["Order Date"]
# # Alternatively
# df['month2'] = df['Order Date2'].str[0:2]
# df['month2']=df['month2'].astype("int32")
# # Gives error as Order Date has meaningless value "Order Date" in many places and returns "Or" in place of NaNs

# temp_df = df[df["Order Date2"].str[0:2]=="Or"]
# temp_df.head()
# # Drop the "Or" rows
# df = df[df["Order Date2"].str[0:2]!="Or"]
# df.head()

# # Now run the
# df=df.dropna(how="all")
# df['month2'] = df['Order Date2'].str[0:2]
# df['month2']=df['month2'].astype("int32")
# df.head()


# Second, see whether all columns have appropriate data types.
# Especially important when we need to multiply columns to answer the above question
print(df.dtypes)
# We observe that all columns are of object dtype.
# We need to convert the following columns to numeric dtypes: 'Order ID', 'Quantity Ordered', 'Price Each'
df["Order ID"] = pd.to_numeric(df["Order ID"], errors='coerce')
df["Price Each"] = pd.to_numeric(df["Price Each"], errors='coerce')
df["Quantity Ordered"] = pd.to_numeric(df["Quantity Ordered"], errors='coerce')
df.dtypes


# Construct a new column indicating sales revenue
df["Sales_Revenue"]=df["Price Each"]*df["Quantity Ordered"]
print(df["Sales_Revenue"].describe())

# Finally, lets answer the question
df_max_sales = df.groupby(pd.PeriodIndex(df['Order Date'], freq="M"))['Sales_Revenue'].sum()
df_max_avg_sales = df.groupby(pd.PeriodIndex(df['Order Date'], freq="M"))['Sales_Revenue'].mean()

print(f"The month of December reported the highest total sales {df_max_sales.max()} and average sales per order {df_max_avg_sales.max()}.")


# Data exploration
months = range(1,13)
print(months)

print("Total Sales=", df.groupby(['month']).sum()['Sales_Revenue'])

plt.bar(months,df.groupby(['month']).sum()['Sales_Revenue'])
plt.xticks(months)
plt.ylabel('Sales in USD ($)')
plt.xlabel('Month number')
plt.show()



# Task 3: (Q) Which US city had the largest sales?

# Get city and state
def get_city_state(address):
    asplit = address.split(",")
    ssplit = address.split(" ")
    city = asplit[1].split()[-1]
    state = asplit[2].split()[0]
    return city, state
df[['City', 'State']] = df['Purchase Address'].apply(get_city_state).to_list()

print(df.groupby(['City']).sum()['Sales_Revenue'])
df.groupby('City')['Sales_Revenue'].sum().plot.bar()
print("Francisco has the highest sales of $8262203.91")


# Alternatively,
# def get_city(address):
#     return address.split(",")[1].strip(" ")
# def get_state(address):
#     return address.split(",")[2].split(" ")[1]
# df['City'] = df['Purchase Address'].apply(lambda x: f"{get_city(x)}  ({get_state(x)})")
# df.head()
#
# df.groupby(['City']).sum()
#
# import matplotlib.pyplot as plt
#
# keys = [city for city, df in df.groupby(['City'])]
#
# plt.bar(keys,df.groupby(['City']).sum()['Sales'])
# plt.ylabel('Sales in USD ($)')
# plt.xlabel('Month number')
# plt.xticks(keys, rotation='vertical', size=8)
# plt.show()



# Task 4: (Q) What time should we display advertisements to maximize sales?

# First we should get hour from Order Date to capture the exact time customers create orders
df['hour'] = pd.DatetimeIndex(df['Order Date']).hour
pd.isna(df['hour']).sum() # Check if there are NAs. Nope!

df.groupby('hour')['Sales_Revenue'].sum().plot.bar()
print("At 7PM")

# Alternatively,
# # Add hour column
# df['Hour'] = pd.to_datetime(df['Order Date']).dt.hour
# df['Minute'] = pd.to_datetime(df['Order Date']).dt.minute
# df['Count'] = 1
# df.head()
#
# keys = [pair for pair, df in df.groupby(['Hour'])]
#
# plt.plot(keys, df.groupby(['Hour']).count()['Count'])
# plt.xticks(keys)
# plt.grid()
# plt.show()



# Task 5: (Q) What product sold the most? Why do you think it sold the most?
df2 = df.groupby('Product')['Quantity Ordered'].sum().sort_values(ascending=False)
print(f"The customers bought total {df2.max()} AAA Batteries (4-pack), the most of any other products")

# Alternatively,
# product_group = df.groupby('Product')
# quantity_ordered = product_group.sum()['Quantity Ordered']
#
# keys = [pair for pair, df in product_group]
# plt.bar(keys, quantity_ordered)
# plt.xticks(keys, rotation='vertical', size=8)
# plt.show()


prices = df.groupby('Product').mean()['Price Each']

fig, ax1 = plt.subplots()

ax2 = ax1.twinx()
ax1.bar(keys, quantity_ordered, color='g')
ax2.plot(keys, prices, color='b')
ax1.set_xlabel('Product Name')
ax1.set_ylabel('Quantity Ordered', color='g')
ax2.set_ylabel('Price ($)', color='b')
ax1.set_xticklabels(keys, rotation='vertical', size=8)
fig.show()




# Task 6: (Q) Which products are most often sold together?
# First, lets create a new df and keep Order IDs with multiple values
new_df = df[df["Order ID"].duplicated(keep = False)]
# Create a "product_basket" joiing products within an Order ID together
new_df["product_basket"] = new_df.groupby("Order ID")["Product"].transform(lambda x: ",".join(x))
# Drop the duplicates
new_df = new_df[["Order ID", "product_basket"]].drop_duplicates()

new_df.head()

count = Counter()
for row in new_df["product_basket"]:
    row_list = row.split(",")
    count.update(Counter(combinations(row_list,2)))
print(count)

count.most_common(5)# if too many combinations
#%%
import pandas as pd
import plotly.express as px
## readthe html data
df = pd.read_html("https://www.moneycontrol.com/stocks/marketstats/blockdeals/")
# %%
## get the data frame
df1 = df[0]
### to drop multiple column names to the results you want repeat the process as many times as requried
df1.columns = df1.columns.droplevel(0)
#%%
df1.columns = df1.columns.droplevel(0)
# %%
## rename the columns
dict = {
    "Time":"Quntity",
    'Unnamed: 4_level_2':"price",
    'Unnamed: 5_level_2':"Value",
    'Unnamed: 6_level_2':"Time"
}
df2 = df1.rename(columns=dict , inplace=True)
# %%
df1 = df1.sort_values(by=['Quntity'] , ascending=False)
sort = df1[df1['Quntity'] > 500000]
# %%
name = df1['Company Name'].str.split("Add" , n=1 , expand=True)
df1['company name'] =  name[0]
df_final = df1[[ 'Exchange', 'Sector', 'Quntity', 'price', 'Value','Time', 'company name']]
# %%
top_sec = df_final.groupby(by=['Sector']).sum().sort_values(by=['Value'])
# %%
fig = px.bar(top_sec, x='Value', y=top_sec.index)
fig.show()
# %%
top_stock = df_final.groupby(by=['company name']).sum().sort_values(by=['Value'])
top_stock = top_stock.tail(20)
fig1 = px.bar(top_stock, x='Value', y=top_stock.index)
fig1.show()
# %%
import seaborn as sn
# %%
sn.set_style("darkgrid")
sn.color_palette("rocket", as_cmap=True)
fig2 = sn.barplot(data=top_stock , x='Value' , y=top_stock.index)
# %%

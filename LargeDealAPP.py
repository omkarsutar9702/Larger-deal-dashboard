#import libraries
import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title = "Large Deals In Stocks",layout="wide" , page_icon="chart_with_upwards_trend")
## build app
## load data
df = pd.read_html("https://www.moneycontrol.com/stocks/marketstats/blockdeals/")
## get derised data from web
df1 = df[0]
## remove extra column names from datafreame
df1.columns = df1.columns.droplevel(0)
df1.columns = df1.columns.droplevel(0)
## rename columns
dict = {"Time" : "Quntity", 'Unnamed: 4_level_2' : "price" , 'Unnamed: 5_level_2' : "Value (Cr)" , 'Unnamed: 6_level_2' : "Time"}
df2 = df1.rename(columns=dict , inplace=True)
## remove extra string from company name
name = df1['Company Name'].str.split("Add" , n=1 , expand=True)
## selelct only company name
df1['company name'] =  name[0]
## remove original company name
df_final = df1[[ 'Exchange', 'Sector', 'Quntity', 'price', 'Value (Cr)','Time', 'company name']]
## sort values by Quntity
top10 = df_final.sort_values(by=['Value (Cr)'] , ascending=False)
## create table
st.markdown("<h3 style='text-align: center;'>Today's top 20 Deals</h3>", unsafe_allow_html=True)
st.table(top10.head(20) )
##get filterd data
options = df_final['Sector'].unique().tolist()
selected_options = st.multiselect('Select the Scetor you want to see',options)
filtered_df = df_final[df_final["Sector"].isin(selected_options)]
filtered_df = filtered_df.sort_values(by=['Value (Cr)'] , ascending=False)
st.markdown("<h3 style='text-align: center;'>Sector Wise Deals</h3>", unsafe_allow_html=True)
## show data on dashboard
st.dataframe(filtered_df , use_container_width=True)
## plot of top 20 sectors
st.markdown("<h3 style='text-align: center;'>Today's top Scetors</h3>", unsafe_allow_html=True)
top_sec = df_final.groupby(by=['Sector']).sum().sort_values(by=['Value (Cr)'])
top_sec = top_sec.tail(20)
fig = px.bar(top_sec, x='Value (Cr)', y=top_sec.index)
st.plotly_chart(fig , use_container_width=True)
## plot top Stocks 
st.markdown("<h3 style='text-align: center;'>Today's top Stock</h3>", unsafe_allow_html=True)
top_stock = df_final.groupby(by=['company name']).sum().sort_values(by=['Value (Cr)'])
top_stock = top_stock.tail(20)
fig1 = px.bar(top_stock, x='Value (Cr)', y=top_stock.index)
st.plotly_chart(fig1 , use_container_width=True)






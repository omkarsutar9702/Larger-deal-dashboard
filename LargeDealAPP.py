import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Large Deals In Stocks", layout="wide", page_icon="📈")

@st.cache(ttl=600)  # Cache data for 10 minutes to avoid redundant requests
def load_data():
    url = "https://www.moneycontrol.com/stocks/marketstats/blockdeals/"
    df_list = pd.read_html(url)
    df = df_list[0]
    return df

# Load data
df = load_data()

# Clean and prepare data
df.columns = df.columns.droplevel([0, 1])
df.rename(columns={"Time": "Quantity", 'Unnamed: 4_level_2': "Price", 'Unnamed: 5_level_2': "Value (Cr)", 'Unnamed: 6_level_2': "Time"}, inplace=True)

# Ensure relevant columns are strings
df['Company Name'] = df['Company Name'].astype(str)
df['Quantity'] = df['Quantity'].astype(str)
df['Price'] = df['Price'].astype(str)
df['Value (Cr)'] = df['Value (Cr)'].astype(str)

# Extract company names
df['Company Name'] = df['Company Name'].str.split("Add", n=1, expand=True)[0]

# Select relevant columns
df = df[['Sector', 'Quantity', 'Price', 'Value (Cr)', 'Time', 'Company Name']]

# Convert relevant columns to numeric
df['Quantity'] = pd.to_numeric(df['Quantity'].str.replace(',', ''), errors='coerce')
df['Price'] = pd.to_numeric(df['Price'].str.replace(',', ''), errors='coerce')
df['Value (Cr)'] = pd.to_numeric(df['Value (Cr)'].str.replace(',', ''), errors='coerce')


# Display top 20 deals
st.markdown("<h3 style='text-align: center;'>Today's Top 20 Deals</h3>", unsafe_allow_html=True)
top_20_deals = df.nlargest(10, 'Value (Cr)')
st.table(top_20_deals)

# Filter data by sector
try:
    sectors = df['Sector'].unique().tolist()
    selected_sectors = st.multiselect('Select the Sectors you want to see', sectors)
    filtered_df = df[df['Sector'].isin(selected_sectors)].sort_values(by='Value (Cr)', ascending=False)
    st.markdown("<h3 style='text-align: center;'>Sector Wise Deals</h3>", unsafe_allow_html=True)
    st.dataframe(filtered_df, use_container_width=True)
except Exception as e:
    st.error(f"Error filtering data by sector: {e}")


# Plot top 20 sectors
st.markdown("<h3 style='text-align: center;'>Today's Top Sectors</h3>", unsafe_allow_html=True)
top_sectors = df.groupby('Sector')['Value (Cr)'].sum().nlargest(20)
fig_sectors = px.bar(top_sectors, x=top_sectors.values, y=top_sectors.index, orientation='h', labels={'x': 'Value (Cr)', 'y': 'Sector'})
st.plotly_chart(fig_sectors, use_container_width=True)

# Plot top 20 stocks
st.markdown("<h3 style='text-align: center;'>Today's Top Stocks</h3>", unsafe_allow_html=True)
top_stocks = df.groupby('Company Name')['Value (Cr)'].sum().nlargest(20)
fig_stocks = px.bar(top_stocks, x=top_stocks.values, y=top_stocks.index, orientation='h', labels={'x': 'Value (Cr)', 'y': 'Company Name'})
st.plotly_chart(fig_stocks, use_container_width=True)




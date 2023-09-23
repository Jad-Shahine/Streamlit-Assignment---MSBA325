#!/usr/bin/env python
# coding: utf-8

# In[7]:


# !pip install -q pandas
# !pip install -q streamlit
# !pip install -q matplotlib
# !pip install -q seaborn
# !pip install -q plotly
# !pip install -q geopandas

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
import locale
import geopandas as gpd
import numpy as np
import altair as alt
import plotly.graph_objects as go


df = pd.read_csv('global-data-on-sustainable-energy (1).csv')
df.rename(columns={"Value_co2_emissions_kt_by_country":"CO2 Emissions"}, inplace=True)
df2 = df.dropna(subset=['Land Area(Km2)'])


# In[9]:


# Streamlit WebApp

# Set the theme settings
st.set_page_config(
    page_title="Sustainable Energy",
    page_icon="🌍♻",
    layout="wide",  # You can set the layout as per your preference
)

# Define your theme
st.markdown(
    f"""
    <style>
    .reportview-container {{
        background-color: #FFFFFF;
    }}
    .sidebar .sidebar-content {{
        background-color: #F0F2F6;
    }}
    .Widget {{
        color: #262730;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# # Set page config to wide layout
# st.set_page_config(layout="wide")

# Set the title of your Streamlit app
st.markdown("<h1 style='text-align: Left; font-size: 100; color: #F63366;'>Sustainable Energy</h1>", unsafe_allow_html=True)

st.markdown(" ")
st.markdown(" ")
st.markdown(" ")
st.markdown(" ")
st.markdown(" ")
st.markdown(" ")
st.markdown(" ")


# Add a title to the sidebar
st.sidebar.markdown("<h1 style='text-align: center; font-size: 50px; color: #F63366;'>2022 Stats</h1>", unsafe_allow_html=True)
st.sidebar.markdown(" ")
st.sidebar.markdown(" ")
st.sidebar.markdown(" ")
st.sidebar.markdown(" ")

# CO₂ Emissions Metric
st.sidebar.metric(label="Gloabl CO₂ Emissions", value="36.8 gigatons", delta="+0.9%")

st.sidebar.markdown(" ")
st.sidebar.markdown(" ")
st.sidebar.markdown(" ")

# Largest CO₂ Emissions Metric
st.sidebar.metric(label="Top Contributar to CO₂ Emissions", value="China")

st.sidebar.markdown(" ")
st.sidebar.markdown(" ")
st.sidebar.markdown(" ")

# Renewable Energy Electricity Generation Metric
st.sidebar.metric(label="Renewable Energy Electricity Generation", value="90%")

st.sidebar.markdown(" ")
st.sidebar.markdown(" ")
st.sidebar.markdown(" ")

# Visualization 1: Scatter Plot
st.markdown("<h1 style='text-align: Left; font-size: 50; color: #F63366;'>Renewable Energy Share in Consumption vs GDP</h1>", unsafe_allow_html=True)

# Define the scatter plot
fig1 = px.scatter(
    df2, 
    x='gdp_per_capita',
    y='Renewable energy share in the total final energy consumption (%)',
    size='Land Area(Km2)',
    size_max=50,
    hover_name='Entity',
    color='Continent',
    animation_frame='Year',
    animation_group='Entity',
    log_x=True,
    range_y=[0, 100],
    range_x=[100, 120000]
)

# Customize the layout
fig1.update_layout(
    width=1700,
    height=750,
)

# Display the scatter plot
st.plotly_chart(fig1)


st.markdown(" ")
st.markdown(" ")
st.markdown(" ")
st.markdown(" ")

# Visualization: Choropleth Map
st.markdown("<h1 style='text-align: Left; font-size: 50; color: #F63366;'>CO₂ Emissions per Capita</h1>", unsafe_allow_html=True)

# Define custom colorscale
custom_colorscale = [
    [0.0, 'blue'],
    [0.0005, 'lightblue'],
    [0.001, 'lightcyan'],
    [0.08, 'lightgray'],
    [0.15, 'lightpink'],
    [0.3, 'lightcoral'],
    [0.5, 'salmon'],
    [0.75, 'orangered'],
    [0.9, 'red'],
    [1.0, 'darkred']
]

# Create the choropleth map
fig = px.choropleth(
    df,
    locations="Entity",
    locationmode="country names",
    color="CO2 Emissions",
    hover_name="Entity",
    animation_frame='Year',
    color_continuous_scale=custom_colorscale,
    projection='natural earth',
)

# Customize the color axis
fig.update_coloraxes(colorbar_title="CO₂ Emissions", cmin=0, cmax=10_000_000)

# Customize the layout
fig.update_layout(
    width=1700,
    height=750,
)

# Display the choropleth map
st.plotly_chart(fig)


st.markdown(" ")
st.markdown(" ")
st.markdown(" ")
st.markdown(" ")

# Visualization: Electricity Generation Over Time
st.markdown("<h1 style='text-align: Left; font-size: 50; color: #F63366;'>Global Electricity Generation Mix Over Time</h1>", unsafe_allow_html=True)

# Group the data by year and aggregate the columns
grouped_df = df.groupby('Year').agg({
    'Electricity from fossil fuels (TWh)': 'sum',
    'Electricity from nuclear (TWh)': 'sum',
    'Electricity from renewables (TWh)': 'sum'
}).reset_index()

# Create a Figure
fig = go.Figure()

# Define distinct colors for each energy source
colors = {
    'Fossil Fuels': 'green',
    'Nuclear': 'red',
    'Renewables': 'blue'
}

# Add traces for each energy source
fig.add_trace(go.Scatter(x=grouped_df['Year'], y=grouped_df['Electricity from fossil fuels (TWh)'], fill='tozeroy', mode='none', name='Fossil Fuels', fillcolor=colors['Fossil Fuels']))
fig.add_trace(go.Scatter(x=grouped_df['Year'], y=grouped_df['Electricity from nuclear (TWh)'], fill='tonexty', mode='none', name='Nuclear', fillcolor=colors['Nuclear']))
fig.add_trace(go.Scatter(x=grouped_df['Year'], y=grouped_df['Electricity from renewables (TWh)'], fill='tonexty', mode='none', name='Renewables', fillcolor=colors['Renewables']))

# Customize the layout of the chart
fig.update_layout(xaxis_title="Year",
                  yaxis_title="Electricity Generation (TWh)",
                  showlegend=True)

fig.update_layout(
    width=1700,  # Set the width of the figure in pixels
    height=750,  # Set the height of the figure in pixels
)

# Display the chart in the Streamlit app
st.plotly_chart(fig)


st.markdown(" ")
st.markdown(" ")
st.markdown(" ")
st.markdown(" ")


st.markdown("<h1 style='text-align: Left; font-size: 100; color: #F63366;'>Access to Electricity Over Time (% of population)</h1>", unsafe_allow_html=True)

# Create a filter for the continent
selected_continent = st.selectbox('Select Continent:', df['Continent'].unique())

# Filter the data based on the selected Continent
continent_filtered_df = df[df['Continent'] == selected_continent]

# Create a selectbox for filtering by Entity within the selected Continent
selected_entity = st.selectbox(f'Select Entity in {selected_continent}:', continent_filtered_df['Entity'].unique())

# Filter the data based on the selected Entity
filtered_df = continent_filtered_df[continent_filtered_df['Entity'] == selected_entity]

# Create the line chart
fig = px.line(filtered_df, x="Year", y="Access to electricity (% of population)", title=f"{selected_entity} ({selected_continent})")
fig.update_layout(xaxis_title="Year", yaxis_title="Access to Electricity (%)", width=1700, height=750)

# Display the line chart
st.plotly_chart(fig)


# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import folium
import geopandas as gpd
from folium.plugins import HeatMap
from streamlit_folium import st_folium
from streamlit_folium import folium_static
import streamlit.components.v1 as comp
import altair as alt   

gdf = gpd.read_file('https://raw.githubusercontent.com/python-visualization/folium/master/tests/us-states.json', driver='GeoJSON')

# Load data and remove NAs from Lon, Lat, and Mortality Rates
hd_mort_demo = pd.read_csv(r"Datasets//Heart_Disease_Mortality_Data_Among_us_Adults_35_by_State_Territory_and_County_2018_2020.csv")
hd_mort_demo = hd_mort_demo.dropna(subset=['X_lon'])
hd_mort_demo = hd_mort_demo.dropna(subset=['Y_lat'])
hd_mort_demo = hd_mort_demo.dropna(subset=['Data_Value'])

# Setup sidebar to filter data by different criterias
all_data = st.checkbox('Filter Data')
top_ten = "in the US"

# Create title and load map
st.subheader("Heart Diseases Mortality in US Adults per 100,000")
fol_test = folium.Map([hd_mort_demo['Y_lat'].mean(), hd_mort_demo['X_lon'].mean()], zoom_start=5, width=1250, height=1000)

# Add weights to the datapoints
points_weight = [[y,x,mort] for x,y,mort in zip(hd_mort_demo['X_lon'].astype(float), hd_mort_demo['Y_lat'].astype(float), hd_mort_demo['Data_Value'])]

hd_mort_demo_sort = hd_mort_demo[hd_mort_demo['GeographicLevel'] == "State"]
hd_mort_demo_sort = hd_mort_demo_sort.groupby('Data_Value')['LocationDesc'].sum().reset_index()
hd_mort_demo_sort = hd_mort_demo_sort.sort_values(by=['Data_Value'], ascending=False).reset_index(drop=True)
hd_mort_demo_sort = hd_mort_demo_sort.drop_duplicates(subset=['LocationDesc'], keep='first')

if all_data:
    st.sidebar.header('Filter Criteria')
    data_view = st.sidebar.selectbox('Select Data View', options=['County', 'State'])
    gender = st.sidebar.selectbox('Select Gender', options=hd_mort_demo['Stratification1'].unique().tolist())
    race = st.sidebar.selectbox('Select Race', options=hd_mort_demo['Stratification2'].unique().tolist())
    # create new dataframe with the filters applied to the columns
    hd_mort_demo_filter = hd_mort_demo[(hd_mort_demo['GeographicLevel']==data_view) & (hd_mort_demo['Stratification1']==gender)
                                        & (hd_mort_demo['Stratification2']==race)]
    view = st.sidebar.selectbox('Select View', options=hd_mort_demo_filter['LocationDesc'])

    fol_test = folium.Map([hd_mort_demo_filter['Y_lat'].mean(), hd_mort_demo_filter['X_lon'].mean()], zoom_start=5, width=1250, height=1000)
    points_weight = [[y,x,mort] for x,y,mort in zip(hd_mort_demo_filter['X_lon'].astype(float), hd_mort_demo_filter['Y_lat'].astype(float), hd_mort_demo_filter['Data_Value'])]
    top_ten = "by " + data_view
    
    ## Adding Summary Statistics to the Side
    ## Currently top 10 highest mortality rates
    hd_mort_demo_sort = hd_mort_demo_filter.sort_values(by='Data_Value', ascending=False)

# Add weights to the datapoints
HeatMap(points_weight, radius=5).add_to(fol_test)
folium_static(fol_test)

st.subheader(f"Top 10 Mortality Rates {top_ten}")
#st.bar_chart(hd_mort_demo_sort.head(10), x='LocationDesc', y='Data_Value')
#st.write(hd_mort_demo_sort.head(10))
st.altair_chart(alt.Chart(hd_mort_demo_sort.head(10)).mark_bar().encode(
    x=alt.X('LocationDesc', sort=None, title='Mortality Rate'),
    y=alt.Y('Data_Value', sort='-x', title='Location'),),
    use_container_width=True)

if all_data: 
    st.subheader("Click to View State and County Data")
    location = hd_mort_demo_sort.loc[hd_mort_demo_sort['LocationDesc'] == view, 'LocationAbbr'].iloc[0]
    st.write("The default is state unless you change the filter criteria")
    st.write(f"Now Viewing Data for {view},  {location}")
    hd_mort_pop_view = hd_mort_demo[hd_mort_demo['LocationDesc'] == view]
    hd_mort_pop_view['Sex/Ethnicity'] = hd_mort_pop_view['Stratification1'] + " " + hd_mort_pop_view['Stratification2']
    hd_mort_pop_view = hd_mort_pop_view.drop_duplicates(subset=['Sex/Ethnicity', 'LocationDesc'], keep='first')
    print(hd_mort_pop_view)
    fig = px.scatter(
        hd_mort_pop_view,
        x="Sex/Ethnicity",
        y="Data_Value",
        color='Sex/Ethnicity',
        size='Data_Value'   
        )
    st.plotly_chart(fig)
    





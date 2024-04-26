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
import geopandas
from folium.plugins import HeatMap
from streamlit_folium import st_folium
from streamlit_folium import folium_static
import streamlit.components.v1 as comp

# Load data and remove NAs from Lon, Lat, and Mortality Rates
hd_mort_demo = pd.read_csv(r"Datasets//Heart_Disease_Mortality_Data_Among_us_Adults_35_by_State_Territory_and_County_2018_2020.csv")
hd_mort_demo = hd_mort_demo.dropna(subset=['X_lon'])
hd_mort_demo = hd_mort_demo.dropna(subset=['Y_lat'])
hd_mort_demo = hd_mort_demo.dropna(subset=['Data_Value'])

# Setup sidebar to filter data by different criterias
st.sidebar.header('Filter Criteria')
data_view = st.sidebar.selectbox('Select Data View', options=['County', 'State'])
gender = st.sidebar.selectbox('Select Gender', options=hd_mort_demo['Stratification1'].unique().tolist())
race = st.sidebar.selectbox('Select Race', options=hd_mort_demo['Stratification2'].unique().tolist())

# Save for unfiltered dataset (in works)
all_data = False

# create new dataframe with the filters applied to the columns
hd_mort_demo_filter = hd_mort_demo[(hd_mort_demo['GeographicLevel']==data_view) & (hd_mort_demo['Stratification1']==gender)
                                     & (hd_mort_demo['Stratification2']==race)]

# Create title and load map
st.subheader("Heart Diseases Mortality in US Adults per 100,000")
fol_test = folium.Map([hd_mort_demo['Y_lat'].mean(), hd_mort_demo['X_lon'].mean()], zoom_start=5, width=2000, height=800) 

# Add weights to the datapoints
points_weight = [[y,x,mort] for x,y,mort in zip(hd_mort_demo_filter['X_lon'].astype(float), hd_mort_demo_filter['Y_lat'].astype(float), hd_mort_demo_filter['Data_Value'])]
HeatMap(points_weight, radius=5).add_to(fol_test)
st_folium(fol_test)

## Adding Summary Statistics to the Side
## Currently top 10 highest mortality rates
st.subheader("Top 10 Mortality Rates")
hd_mort_demo_filtered = hd_mort_demo_filter.sort_values(by='Data_Value', ascending=False)
st.bar_chart(hd_mort_demo_filtered.head(10), x='LocationDesc', y='Data_Value')



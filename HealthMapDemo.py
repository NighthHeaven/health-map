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

def run():
  
  import streamlit as st
  import pandas as pd
  import numpy as np
  import plotly.express as px
  #px.set_mapbox_access_token(open(".mapbox_token").read())
  
  #hd_500 = pd.read_csv(r"Datasets/(Heart Disease) 500_Cities__City-level_Data__GIS_Friendly_Format___2019_release.csv")
  hd_mort_demo = pd.read_csv(r"Datasets//Heart_Disease_Mortality_Data_Among_us_Adults_35_by_State_Territory_and_County_2018_2020.csv")
  #cd_indic = pd.read_excel(r"Datasets//US Chronic Disease Indicators Adjusted by Age.xlsx")
  
  #hd_mort_demo = hd_mort.loc[hd_mort['Data_Value_Type']=='Age-adjusted, 3-year Average Rate']
  
  # testing
  #st.subheader("Heart Diseases in 500 Cities")
  #st.write(hd_500)
  #mort_fig = px.scatter_geo(hd_mort_demo.dropna(), lat='Y_lat', lon='X_lon', 
  #                             hover_data=['Stratification1', 'Stratification2'], projection='albers usa')
  
  # Sidebar Data
  st.sidebar.header('Filter Criteria')
  data_view = st.sidebar.selectbox('Select Data View', options=['County', 'State'])
  gender = st.sidebar.selectbox('Select Gender', options=hd_mort_demo['Stratification1'].unique().tolist())
  race = st.sidebar.selectbox('Select Race', options=hd_mort_demo['Stratification2'].unique().tolist())
  state = st.sidebar.selectbox('Filter for State', options=hd_mort_demo['LocationAbbr'].unique().tolist())
  
  hd_mort_demo_filter = hd_mort_demo[(hd_mort_demo['GeographicLevel']==data_view) & (hd_mort_demo['Stratification1']==gender)
                                         & (hd_mort_demo['Stratification2']==race) & (hd_mort_demo['LocationAbbr']==state)]
  
  
  st.subheader("Heart Diseases Mortality in US Adults per 100,000")
  #st.plotly_chart(mort_fig)
  st.map(hd_mort_demo_filter.dropna(subset=['Y_lat', 'X_lon', 'Data_Value']), latitude='Y_lat', longitude='X_lon')
if __name__ == "main":
  run()

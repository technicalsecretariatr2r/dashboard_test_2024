import streamlit as st
import pandas as pd
import numpy as np
import os
from PIL import Image
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.ticker as ticker
from matplotlib.ticker import MaxNLocator
from matplotlib.ticker import ScalarFormatter
from matplotlib.ticker import FuncFormatter
from wordcloud import WordCloud, STOPWORDS
from streamlit_folium import st_folium
import folium
import plotly.graph_objects as go
# import squarify
import seaborn as sns
import plotly.express as px
import sys
import re
import openpyxl
from openpyxl.styles import Border, Side
from io import BytesIO
from numerize.numerize import numerize
import requests
#News
from datetime import datetime
import pydeck as pdk


def solution_stories_partner_finder(df_filtered,p_short_name):
    st.markdown(f"### {p_short_name} SOLUTION STORIES")
    st.markdown(f"""

    **Click on a pin for a popup with key details on {p_short_name} solution stories.**

    """, unsafe_allow_html=True)

    df_filtered['Onclick'] = df_filtered['Cities'].astype(str) + ", " + df_filtered['All_Countries'].astype(str)
    # df_solution_stories['Onclick']

    def convert_date(date_string):
        try:
            # Parse the date string in the given format
            date_obj = datetime.strptime(date_string, '%B %d, %Y')
            # Convert the date object to a standard format, e.g., "YYYY-MM-DD"
            return date_obj.strftime('%Y-%m-%d')
        except ValueError:
            # Return None or some default value if the parsing fails
            return None

    # Apply the conversion function to the 'Date' column
    df_filtered['Date'] = df_filtered['Date'].apply(convert_date)
    
    # df_filtered
    
    ## Chart
    df = df_filtered
    # df.columns

    # InitName
    # All_Countries
    # Cities 
    # Lat
    # Lon
    # SAA Priority Systems
    # Description
    # Title
    # Date
    # Implementers
    # Beneficiaries / Impact:
    # Official_Link
    # Video Description
    # Comments

    world_map_solution_stories = folium.Map(location=[0, 0], zoom_start=2, tiles="cartodbpositron")

    # Loop through the data and add markers.
    for index, row in df.iterrows():
        # Check and prepare 'Video Description' link if available
        video_description_link = f'<a href="{row["Video_Description"]}" target="_blank"><b>Video Description</b></a><br>' if row['Video_Description'] != "No Available" else ""

        # Check and prepare 'Beneficiaries / Impact:' if available
        beneficiaries_impact = f'<b>Beneficiaries / Impact:</b> {row["Beneficiaries / Impact:"]}<br>' if row['Beneficiaries / Impact:'] != "No Available" else ""

        # Create popup HTML including only available information
        popup_html = f"""
        <div>
            <b style="color:#FF37D5;">RtR SOLUTION STORY</b><br>
            <b>Title:</b> {row['Title']}<b>.</b><br>
            <b>Date:</b> {row['Date']}<br>
            <b>Partner:</b> {row['InitName']}<br>
            <b>Location:</b> {row['Onclick']}<br> 
            <b>Implementers:</b> {row['Implementers']}<br>
            <b>SAA Priority Systems:</b> {row['SAA Priority Systems']}<br>
            {beneficiaries_impact}
            <b>Description:</b> {row['Description']}<br>
            {video_description_link}
            <a href="{row['Official_Link']}" target="_blank"><b>Read full solution story here!</b></a>
        </div>
        """

        popup = folium.Popup(popup_html, max_width=300)
        folium.Marker(
            location=[row["lat"], row["lon"]],
            popup=popup,
            tooltip=row['Onclick'],
        ).add_to(world_map_solution_stories)

    # Display the map in Streamlit.
    st_folium(world_map_solution_stories, width=725, key="map_solution_stories", returned_objects=[])


    # solution_studies_table_public_list = ['InitName',
    # 'Title',
    # 'Description',
    # 'Date',
    # 'SAA Priority Systems',
    # 'Implementers',
    # 'Beneficiaries / Impact:',
    # 'Official_Link',
    # 'Video_Description',
    # 'Cities',
    # 'All_Countries',
    # 'country_continents_all',
    # 'country_region_all',
    # 'country_subregion_all',]


    # with st.expander("Solution Stories Data Set: Filtered Based on Selection Criteria"):
    #     st.dataframe(df_filtered[solution_studies_table_public_list])
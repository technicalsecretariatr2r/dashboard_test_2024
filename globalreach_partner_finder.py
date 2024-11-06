## LIBRARIES

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns
from streamlit_folium import st_folium
import folium
from PIL import Image
from numerize.numerize import numerize
from branca.element import Template, MacroElement

# Get unique sources from the DataFrame
def global_reach_partner_finder(df_partner_campaign,df_m_countries_vertical,political_countries_url):
    try:
        p_short_name = df_partner_campaign['short_name'].iloc[0]
        unique_sources = df_m_countries_vertical['source'].unique()
        # sorted_sources = sorted(unique_sources, key=custom_sort_key)

        # Define a custom sorting key function
        def custom_sort_key(source):
            order = {
                'All Tools Available': 1,
            }
            
            if source in order:
                return order[source]
            
            if source.startswith('Pledge'):
                return 2
            
            order2 = {
                'Plans (All Plans, in case there is more than one)': 3,
            }
            
            if source in order2:
                return order2[source]
            return 4

        # Sort the unique_sources list using the custom sorting key
        sorted_sources = sorted(unique_sources, key=custom_sort_key)

        # Create a selectbox widget for selecting one source
        st.markdown("##### GLOBAL OUTREACH")
        selected_source = st.selectbox("Select a source of information from "+p_short_name+" to explore", sorted_sources)

        # Display the selected source
        st.write("Selected Source:", selected_source)
        df_m_countries_vertical = df_m_countries_vertical.query('source == @selected_source')
        df_m_countries_vertical['number_country'] = 1
        
        # st.write(df_m_countries_vertical)


        # making the worlmap
        world_map_full = folium.Map(location=(0, 0), zoom_start=1, tiles="cartodb positron")

        folium.Choropleth(
            geo_data=political_countries_url,
            data=df_m_countries_vertical,
            columns=["country_to_plot", 'number_country'],
            key_on="feature.properties.name",
            fill_color="RdPu",
            fill_opacity=0.7,
            line_opacity=0.2,
            legend_name="Country " + p_short_name + " (" + selected_source + ")",
            highlight=True,
        ).add_to(world_map_full)

        folium.LayerControl().add_to(world_map_full)

        st_folium(world_map_full, width=725, key="map1", returned_objects=[])
        
        
        
        
        
        


        with st.expander("Explore Countries, Continents, Regions & Subregions:"):
            st.dataframe(df_m_countries_vertical)
    except Exception as e:
        st.markdown("#### GLOBAL OUTREACH")
        st.markdown("No Information Reported Yet")
        pass
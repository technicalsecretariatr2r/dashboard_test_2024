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



def headquarters(df_gi,df_country,political_countries_url):
    st.markdown("### PARTNERS' HEADQUARTERS")
    st.markdown("Location of RtR Partners' Headquarters")
    #Data set from here to frontend
    df2_gi = df_gi['country_hq'].value_counts().reset_index()
    df2_gi.columns = ['Country', 'Frequency']
    # df3_gi = df_gi[['InitName','q26','country_hq','short_name']]

    # Function to create the new DataFrame
    def create_country_initiatives_df(df_gi,df_country):
        # Ensure 'country_hq' is a string and split it into separate rows for each country
        df_gi['country_hq'] = df_gi['country_hq'].astype(str)
        countries_expanded = df_gi['country_hq'].str.split(';', expand=True).stack().reset_index(level=1, drop=True).rename('Country')

        # Join back to df_gi for the 'short_name' and 'q9'
        df_gi_expanded = df_gi.join(countries_expanded).reset_index()

        # Remove any empty or null country entries
        df_gi_expanded = df_gi_expanded[df_gi_expanded['Country'].str.strip().astype(bool)]

        # Group by the country and aggregate
        df_country_initiatives = df_gi_expanded.groupby('Country').agg(
            n_initiatives=pd.NamedAgg(column='Country', aggfunc='size'),
            org_short_names=pd.NamedAgg(column='short_name', aggfunc=lambda x: '; '.join(x.dropna().unique())),
            org_full_names=pd.NamedAgg(column='InitName', aggfunc=lambda x: '\n'.join(['- ' + name for name in x.dropna().unique()]))
        ).reset_index()
        
        df_country_initiatives = df_country_initiatives [df_country_initiatives ['Country'] != "nan"]
        df_country_lat_lon = df_country[['Country','lat','lon']]
        df_country_initiatives = df_country_initiatives.merge(df_country_lat_lon, on='Country', how='left')
        return df_country_initiatives

    df4_gi_hq_by_country = create_country_initiatives_df(df_gi, df_country)
    # df4_gi_hq_by_country




    #WORLDMAP HEADQUARTERS
    numbers_partners_hq = df4_gi_hq_by_country['n_initiatives'].sum()
    world_map_HQ = folium.Map(location=(0, 0), zoom_start=1, tiles="cartodb positron") 

    for index, row in df4_gi_hq_by_country.iterrows():
        lat = row["lat"]
        lon = row["lon"]
        if not pd.isna(lat) and not pd.isna(lon):  # skip rows with non-numerical lat/lon values
            folium.Marker(
                location=[lat, lon],
                # popup=row['q9'],
                # tooltip=f"<b>N° Headquarters:</b> {row['n_initiatives']}"
                tooltip=f"<b>Country:</b> {row['Country']}<br><b>N° Headquarters:</b> {row['n_initiatives']}<br><b>Partners:</b> {row['org_short_names']}"
                # tooltip=f"<b>Country:</b> {row['Country']}<b>N° Headquarters:</b> {row['n_initiatives']}<br><b>Number of partners per country:</b> {row['N Parters per country']}<br><b>Partners per country:</b> {row['Partners per country']}"
            ).add_to(world_map_HQ)
            
    folium.Choropleth(
        geo_data=political_countries_url,
        data=df2_gi,
        columns=['Country', 'Frequency'],
        key_on="feature.properties.sovereignt",
        fill_color="RdPu",
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name="Number of RtR Partners' Headquarters by Country",
        highlight=True,
    ).add_to(world_map_HQ)
    folium.LayerControl().add_to(world_map_HQ)

    st_folium(world_map_HQ,width=725, returned_objects=[])
    st.caption("Out of "+str(numbers_partners_hq)+" RtR Partners (Source: General Information Survey)")
    with st.expander("Check Table of Head Quarters Info"):
        st.write(df4_gi_hq_by_country)
    



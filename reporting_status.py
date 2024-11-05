# BLOCK REPORTING STATUS
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns
from streamlit_folium import st_folium
from wordcloud import WordCloud, STOPWORDS
import folium
from PIL import Image
from numerize.numerize import numerize


def reporting_status(df_m_countries_vertical, df_partner_campaign):
    tile_partner_reporting_status =f"""#### REPORTING STATUS"""
    st.markdown(tile_partner_reporting_status)
    try:
        n_countries_pledge = df_m_countries_vertical[df_m_countries_vertical['source'].isin(['Pledge (All Beneficiaries)'])]
        n_countries_pledge = len(n_countries_pledge['All_Countries'].unique())

        n_countries_plan = df_m_countries_vertical[df_m_countries_vertical['source'].isin(['Plans (All Plans, in case there is more than one)'])]
        n_countries_plan = len(n_countries_plan['All_Countries'].unique())

        n_countries_all_tools = df_m_countries_vertical[df_m_countries_vertical['source'].isin(['All Tools Available'])]
        n_countries_all_tools = len(n_countries_all_tools['All_Countries'].unique())

        gi_perc = df_partner_campaign['GI_all_index'].iloc[0]
        pledge_perc = df_partner_campaign['pledge_overall_index_percentaje'].iloc[0]
        n_plans = df_partner_campaign['N_Plans'].iloc[0]
        plan_perc = df_partner_campaign['OverallPlanConsolidated'].iloc[0]
        
        col1, col2, col3,col4,col5 = st.columns(5)
        col1.metric("General \nInformation", f"{gi_perc:.0f}%")
        col2.metric("Pledge", f"{pledge_perc:.0f}%")
        col3.metric("N Plans", numerize(n_plans))
        col4.metric("Plan(s)", f"{plan_perc:.0f}%")
        col5.metric("Countries (All Tools)",n_countries_all_tools)
        
    except Exception as e:
        st.markdown("No Reported Information Available")
        pass

# END BLOCK REPORTING STATUS

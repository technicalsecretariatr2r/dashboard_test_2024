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


def structure_and_format_partner_finder():
    
    #__________________________________________________________________________________________________________________________________________________________________
# Dashboard structure and format
#__________________________________________________________________________________________________________________________________________________________________
    im = Image.open("logo_web.png")
    st.set_page_config(page_title="RtR DATA EXPLORER", page_icon=im, layout="wide", initial_sidebar_state="expanded")

    # CURRENT_THEME = "light"
    # IS_DARK_THEME = False

    with open( "style.css" ) as css:
        st.markdown(f'<style>{css.read()}</style>' , unsafe_allow_html= True)
        st.sidebar.markdown(f'<style>{css.read()}</style>' , unsafe_allow_html= True)


    ##hidefooter streamlit
    hide_streamlit_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                </style>
                """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)


    # Hide index when showing a table. CSS to inject contained in a string
    hide_table_row_index = """
                <style>
                thead tr th:first-child {display:none}
                tbody th {display:none}
                </style>
                """
    # Inject CSS with Markdown
    st.markdown(hide_table_row_index, unsafe_allow_html=True)



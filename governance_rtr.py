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



def intro_summary():
   
    st.markdown("""
                ##### GOVERNANCE SETUP
                The governance setup of the Campaign seeks to ensure this goal. RtR has three advisory bodies: the Technical Secretariat (TS), the Expert Review Group (ERG), and the Methodological Advisory Group (MAG). The TS, hosted by the <a style="font-weight:bold" href="https://www.cr2.cl/">Center for Climate and Resilience Research (CR)2</a> of the University of Chile, is an academic entity that offers technical support to the Campaign and is responsible for upholding the credibility, transparency, and robustness of the RtR and oversees the MAG and ERG. The TS includes scientists who are leading academic authors and contribute to the Intergovernmental Panel on Climate Change (IPCC). The MAG (18 members) helps improve and validate the RtR framework and metrics. The ERG (14 members) is set up to peer-review applications of candidates applying to join the RtR.
                """,unsafe_allow_html=True)

    with st.expander("To get more information about the members of the RtR advisory bodies, click here"):
        st.write("Names:")
        col1, col2, col3 = st.columns(3)
        markdown_text_1 = """
        ###### Technical Secretariat (TS)

        - Marco Billi
        - Roxana Bórquez
        - Francis Mason
        - Paulina Aldunce
        - Nicolle Aspee
        - Priscilla Berríos
        - Marcela Cuevas
        - Juan Carlos Varela
        """

        markdown_text_2 = """
        ###### Methodological Advisory Group (MAG)

        - Emilie Beauchamp (MAG Co-Lead)
        - Ana María Loboguerrero (MAG Co-Lead)
        - Anand Patwardhan (MAG Co-Lead)
        - Md Nurul Alam
        - Tariq Al-Olaimy
        - Pilar Bueno
        - Ankan De
        - Portia Hunt
        - Jia Li
        - Jennifer Shaw
        - Shehnaaz Moosa
        - André Nahur
        - Marta Olazabal
        - Revathi Sharma
        - Karl Schultz
        - Chiara Trabacchi
        - Kay Tuschen
        - Patricia Villarroel
        """

        markdown_text_3 = """
        ###### Experts Review Group (ERG)

        - Ellen Acioli
        - Ibidun Adelekan
        - Ambe Emmanuel Cheo
        - Alex Godoy-Faúndez
        - Narayan Gyawali
        - George Haddow
        - Marina Hermosilla
        - Runa Khan
        - Paul O´Hare
        - Ignacio Robles
        - Annette Salkeld
        - Thomas Tanner
        - Sebastián Vicuña
        - Terry-Rene Wiesner
        """
        col1.markdown(markdown_text_1)
        col2.markdown(markdown_text_2)
        col3.markdown(markdown_text_3)


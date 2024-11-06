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
    st.markdown("#### INTRODUCTION")
    st.markdown("""
                **Welcome to the RtR Data Explorer**. A powerful web application designed to support the <a style="font-weight:bold" href="https://racetozero.unfccc.int/system/racetoresilience/">Race to Resilience Campaign (RtR)</a>. 
                
                RtR was launched at the Climate Adaptation Summit in 2021 by the <a style="font-weight:bold" href="https://climatechampions.unfccc.int/">UN Climate Change High-Level Champions (HLCs)</a> for COP25 and COP26, with the purpose to serve as a global platform that brings together Non-Party Stakeholders (NPS), investors, businesses, cities, regions, and civil society to increase the resilience of 4 billion people by 2030, those most vulnerable to the climate crisis.
                
                <blockquote style="background-color: #f9f9f9; border-left: 10px solid #ccc; margin: 1.5em 10px; padding: 0.5em 10px;">
                    The RtR Data Explorer offers an informative and interactive experience with data visualization, providing updates on the resilience-building metrics of RtR Partners' Pledges and Plans. This application offers a comprehensive view of the RtR Metrics Framework, showcasing the global efforts of the campaign. It includes a Multicriteria-Based Partner Selection Tool, which allows access to Partners' Profiles and enables in-depth exploration of their contributions to the campaign. Additionally, it showcases various solution stories from RtR Partners, members, and implementers in different countries and regions, all racing towards a better world.
                </blockquote>
                """,unsafe_allow_html=True)

    st.markdown("""
    ##### HOW TO USE 

    Begin by accessing the sidebar to choose from the RtR Data Explorer Features. The main page will then refresh to display content tailored to your settings, including interactive charts and maps. Delve into datasets, gain insights from the 'Metrics Framework', and read 'Solution Stories' for an overview of partners' experiences within the Race to Resilience Campaign.
                """)
    with st.expander("Read detailed instructions here"):
        st.markdown("""
            ###### HOW TO USE THE RtR DATA EXPLORER

            **1. Navigation:**
            - Begin by utilizing the sidebar to navigate the app. This sidebar is your primary tool for setting your exploration parameters.
            - If the sidebar is not visible, click the arrow or the icon at the top-left corner to expand it.

            **2. Selecting Options:**
            - Within the sidebar, you'll find various selection tools to tailor the data displayed on the main page. Adjust these to filter the view to your interests.
            - As you make selections, the main content will update to reflect these choices.

            **3. Interacting with Main Page Content:**
            - The main page will display content such as text, charts, and maps according to your selections. 
            - Engage with the charts and maps for detailed information by hovering, clicking, and exploring the visualizations presented.

            **4. Exploring Datasets:**
            - Some elements of the main page may offer interactive capabilities, allowing you to explore the data in depth.

            **5. Understanding Key Concepts:**
            - The 'Metrics Framework' section provides insights and explanations about the key concepts, terms, and methodologies used within the explorer.
            
            **6. Read RtR Partners' experiencies and solution stories:**
            - Utilize features such as 'Solution Stories' to gain insights into case studies of partners across various Sharm-El-Sheikh Adaptation Agenda Priority Systems, countries and regions.
            
            The RtR Data Explorer is a dynamic tool that offers a window into the Race to Resilience Campaign's efforts to fortify the resilience of populations most vulnerable to climate change by 2030. Engage with this platform to explore the multifaceted actions and partnerships that are part of this global movement.
            """)

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


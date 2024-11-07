
import streamlit as st
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
# from wordcloud import WordCloud, STOPWORDS
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
import fitz  # PyMuPDF



def structure_and_format():
    im = Image.open("R2R_RGB_PINK_BLUE.png")
    st.set_page_config(page_title="RtR DATA EXPLORER", layout="wide", initial_sidebar_state="expanded")
    st.logo(im, size="large")
    
    css_path = "style.css"

    with open(css_path) as css:
        st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)
    
    ##
    ##Hide footer streamlit
    ##
    hide_streamlit_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                </style>
                """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
    
    ## Hide index when showing a table. CSS to inject contained in a string
    hide_table_row_index = """
                <style>
                thead tr th:first-child {display:none}
                tbody th {display:none}
                </style>
                """
    ##
    ## Inject CSS with Markdown
    ##
    st.markdown(hide_table_row_index, unsafe_allow_html=True)

structure_and_format()



st.markdown('# RtR METRICS FRAMEWORK')


image_path = 'images/metric_framework_foto.png'

# Display the image in Streamlit

col1, col2 = st.columns([1.5,0.5])
col1.markdown("""
            The **Race to Resilience Metrics Framework** represents a groundbreaking approach in the assessment of climate resilience initiatives. At its core, the integration of qualitative **Depth Metrics** and quantitative **Magnitude Metrics** offers a holistic view of the impact of resilience actions. This dual metric system not only measures the scale of interventions but also delves into their substantive changes and long-term impacts, providing a more nuanced understanding of resilience enhancement.

A key innovation of this framework is the incorporation of these metrics into the **Monitoring, Evaluation, and Learning (MEL) cycle**, transforming them from static measurements to dynamic elements that adapt and evolve over time. This integration is crucial for the continuous refinement and adaptation of resilience strategies, ensuring that they remain effective and responsive to the changing nature of climate challenges.
""")

st.markdown("""
Furthermore, the framework addresses critical challenges in resilience measurement, such as reducing double counting and fostering more integrated intervention strategies. By providing a structured and comprehensive methodology for data collection and analysis, it enhances the credibility and robustness of the data. This rigorous approach ensures that reported outcomes are trustworthy and reliable, paving the way for more effective and sustainable global resilience-building efforts.""")


file_path_full_doc = "rtrmetricsframework2023_full.pdf"


with col2:
    col2.image(image_path)

    # Adding a download button for the PDF in the second column
    with open(file_path_full_doc, "rb") as file:
        col2.download_button(
            label="Download in PDF",
            data=file,
            file_name=os.path.basename(file_path_full_doc),
            mime="application/octet-stream",
            key='download_pdf_col2'  # Unique key for this button
        )

# If you want to add another download button in the sidebar, ensure it has a different key
with open(file_path_full_doc, "rb") as file:
    st.sidebar.download_button(
        label="Download RtR Metrics Framework",
        data=file,
        file_name=os.path.basename(file_path_full_doc),
        mime="application/octet-stream",
        key='download_pdf_sidebar'  # Unique key for this button
    )
 


### SLIDES
file_path_slides = "rtrframework2023_slides.pdf"

def get_pdf_images(file_path):
    doc = fitz.open(file_path)
    all_images = []
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        zoom = 2
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat)
        image = pix.tobytes("png")
        all_images.append(image)
    return all_images

def display_pdf_horizontal(all_images):
    # Initialize counter if not in session state
    if 'counter' not in st.session_state:
        st.session_state.counter = 0

    # Slider for fast navigation
    page_slider = st.slider('Go to Page', 1, len(all_images), st.session_state.counter + 1, key='page_slider')
    if page_slider - 1 != st.session_state.counter:
        st.session_state.counter = page_slider - 1

    # Display images in a carousel-like format using columns
    col1, col2, col3 = st.columns([1, 10, 1])
    with col1:
        if st.session_state.counter > 0 and st.button('Prev', key='prev_button'):
            st.session_state.counter -= 1
    with col2:
        st.image(all_images[st.session_state.counter], use_column_width=True)
    with col3:
        if st.session_state.counter < len(all_images) - 1 and st.button('Next', key='next_button'):
            st.session_state.counter += 1
        
            
def metric_framework_key_highlights():
    st.write("### KEY HIGHLIGHTS")
    st.markdown("The following presentation provides a comprehensive overview of the RtR Metrics Framework. It is designed to guide you through the critical components and methodologies that underpin this framework. Each slide is meticulously crafted to illustrate the various dimensions and applications of these metrics, ensuring a deeper understanding of their role in effective decision-making. Whether you are a novice or an expert in this field, these slides will offer valuable insights and a structured approach to the RtR Metrics Framework.")

    # Mapping of sections to page numbers
    sections_to_pages = {
        "Introduction": 0,
        "RtR Campaign Context": 2,
        "RtR Work Focus":5,
        "RtR Technical Bodies":6,
        "Campaign's Metrics Framework": 8,
        "RtR Theory of Change":12,
        "Resilience Increase Index": 13,
        "Magnitud Metrics":14,
        "Depth Metrics":15,
        "MEL Cicle":16,
        "The Pathway Throught the Race": 17,
        "RtR Reporting Tools":19,
        "Data Explorer and General Results": 23,
        "The Progress of RtR":28,
        "Final Remarks": 22
    }
    
    # Selector for sections
    section = st.selectbox('Go to Section', list(sections_to_pages.keys()), key='section_selector')
    
    # Update counter to the section's start page
    if 'prev_section' not in st.session_state or st.session_state.prev_section != section:
        st.session_state.counter = sections_to_pages[section]
        st.session_state.prev_section = section

    all_images = get_pdf_images(file_path_slides)
    display_pdf_horizontal(all_images)

# metric_framework_key_highlights()







### FULL DOC
# file_path_full_doc = "rtrmetricsframework2023_full.pdf"


def get_pdf_images(file_path):
    doc = fitz.open(file_path)
    all_images = []
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        zoom = 2
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat)
        image = pix.tobytes("png")
        all_images.append(image)
    return all_images

def display_pdf_vertical(all_images):
    # Initialize counter if not in session state
    if 'counter' not in st.session_state:
        st.session_state.counter = 0

    # Slider for fast navigation
    page_slider = st.slider('Go to Page', 1, len(all_images), st.session_state.counter + 1, key='page_slider')
    if page_slider - 1 != st.session_state.counter:
        st.session_state.counter = page_slider - 1

    # Display images in a carousel-like format using columns
    col1, col2, col3 = st.columns([1, 10, 1])
    with col1:
        if st.session_state.counter > 0 and st.button('Prev', key='prev_button'):
            st.session_state.counter -= 1
    with col2:
        st.image(all_images[st.session_state.counter], use_column_width=True)
    with col3:
        if st.session_state.counter < len(all_images) - 1 and st.button('Next', key='next_button'):
            st.session_state.counter += 1
        
            
def metric_framework_full():
    st.markdown("### FULL DOCUMENT: Enhanced Edition (2023)")
    st.markdown("The enhanced 2023 edition of the Race to Resilience White Paper builds on the previous 2022 framework, introducing improved metrics for resilience, a denser theoretical understanding of resilience attributes, and delivering confidence for the robustness of the data, showing the continued evolution of the framework.")
    
    # Mapping of sections to page numbers
    sections_to_pages = {
        "Content": 3,
        "Executive Summary":5,
        "Introduction":7,
        "RtR Campaign Context": 8,
        "Presentation of Race to Resilience":11,
        "RtR Technical Bodies":11,
        "Campaign's Metrics Framework": 14,
        "Framework objetives":15,
        "Resilience Increase Index": 18,
        "Magnitud Metrics":19,
        "Depth Metrics":21,
        "MEL Cicle":22,
        "The Pathway Throught the Race": 24,
        "RtR Reporting Tools":28,
        "Final Remarks": 32,
    }
    
    # Selector for sections
    section = st.selectbox('Go to Section', list(sections_to_pages.keys()), key='section_selector')
    
    # Update counter to the section's start page
    if 'prev_section' not in st.session_state or st.session_state.prev_section != section:
        st.session_state.counter = sections_to_pages[section]
        st.session_state.prev_section = section

    all_images = get_pdf_images(file_path_full_doc)
    display_pdf_vertical(all_images)
    
    with open(file_path_full_doc, "rb") as file:
        btn = st.download_button(
            label="Download RtR Metric Framework",
            data=file,
            file_name=os.path.basename(file_path_full_doc),
            mime="application/octet-stream"
        )

# metric_framework_full()




from glossary_rtr import glossary_rtr
from ra_glossary import ra_glossary
from action_cluster_glossary import action_clusters_glossary


def main():
    # Add a radio button in the sidebar to select the mode
    option = st.sidebar.radio(
        'Select the Metrics Framework Mode',
        ('Glossary','Full Document', 'Key Highlights','Resilience Attributes','Resilience Action Clusters')
    )

    # Display the appropriate content based on the selection
    if option == 'Full Document':
        metric_framework_full()
    elif option == 'Key Highlights':
        metric_framework_key_highlights()
    elif option == 'Glossary':
        glossary_rtr()
    elif option == 'Resilience Attributes':
        ra_glossary()
    elif option == 'Resilience Action Clusters':
        action_clusters_glossary()

main()





st.write("___")
st.markdown("👈 Explore More: Navigate through different sections using the sidebar to discover in-depth insights and information.")


st.markdown("""
<style>
    a {
        text-decoration: none; /* Remove underline */
        color: #000000; /* Set link color */
    }
    a:hover {
        color: #FF37D5; /* Set hover color */
        text-decoration: underline; /* Underline on hover for better UX */
    }
    .link-list {
        line-height: 1.6; /* Adjust line spacing */
    }
</style>
<div class="link-list">
    <ul>
        <li>To get an overview of the campaign as a whole, <a href="/HOME" target="_self"><strong>click here</strong></a></li>
        <li>To search for partners solution stories, <a href="/SOLUTION_STORIES" target="_self"><strong>click here</strong></a></li>
        <li>To search for the contribution of specific partners, <a href="/PARTNER_FINDER" target="_self"><strong>click here</strong></a></li>
        <li>To get more information on this data explorer, <a href="/ABOUT_THE_DATA_EXPLORER" target="_self"><strong>click here</strong></a></li>
    </ul>
</div>
""", unsafe_allow_html=True)
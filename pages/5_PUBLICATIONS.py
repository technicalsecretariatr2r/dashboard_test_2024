import streamlit as st
import pandas as pd
import numpy as np
import os
import io
from PIL import Image




def structure_and_format():
    im = Image.open("images/R2R_RGB_PINK_BLUE.png")
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


## Welcome Partner finder
def render_main_page_metrics_framewortk(): 
    logo_path = "images/rtr_publication_banner.png"  

    col1, col2, col3 = st.columns([2,0.5,0.5])
    with col1: 
        st.image(logo_path) 

render_main_page_metrics_framewortk()


import streamlit as st
import pandas as pd
import os

# Function to load the CSV file
@st.cache_data
def load_publication_data():
    df_publication_path = "df_publications.csv"  
    df_publication = pd.read_csv(df_publication_path, sep=';')
    return df_publication

# Load the DataFrame
df_publication = load_publication_data()

# Selection filter for publication type with an "All" option
types = ['All'] + list(df_publication['type'].unique())  # Add an "All" option
selected_type = st.selectbox("Select publication type to display:", types)

# Filter DataFrame based on the selected type, or display all if "All" is selected
if selected_type == 'All':
    filtered_df = df_publication  # Display all if "All" is selected
else:
    filtered_df = df_publication[df_publication['type'] == selected_type]

# Display each document's information in columns
for index, row in filtered_df.iterrows():
    # Create columns for layout
    col1, col2 = st.columns([0.5, 1.5])
    
    with col1:
        # Display the image if it exists
        image_path = f"images/{row['image']}.png"
        if os.path.exists(image_path):
            st.image(image_path, caption=row['name_doc'], use_column_width=True)
        else:
            st.write("Image not available")
    
    with col2:
        # Document information
        st.write("###", row['name_doc'])  # Document Title
        st.write("**Type:**", row['type'])  # Type
        st.write("**Description:**", row['description'])  # Description
        
        # Link to the document for download
        if pd.notna(row['link']):
            st.markdown(f"[Download Document]({row['link']})", unsafe_allow_html=True)

    # Divider line for visual separation
    st.write("---")
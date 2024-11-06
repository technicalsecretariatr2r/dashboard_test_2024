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




def selfdescription_partner(df_gi):
    # #___________________________________________
    # #___________________________________________
    # #___________________________________________
    # #___________________________________________
    # # SELF DESCRIPTION 
    # #___________________________________________
    # #___________________________________________
    # #___________________________________________
    # #___________________________________________

    st.markdown("### PARTNERS SELF DESCRIPTION")
    st.markdown("""Visual representation of the words used most frequently by RtR Partners to describe their initiative, goals, and strategies for building resilience.
        """)
    # ## WORDCLOUD
    # df_wordcloud = df_gi
    # df_wordcloud['description_general'] = df_wordcloud['description_general'].astype(str)
    # text = ' '.join(df_wordcloud['description_general'])
    # st.set_option('deprecation.showPyplotGlobalUse', False)
    # wordcloud = WordCloud(stopwords=STOPWORDS, background_color='white', width=800, height=640, colormap="RdPu").generate(text)

    # # Create a new figure and add a title
    # fig, ax = plt.subplots()
    # ax.set_title('RtR PARTNERS SELF-DESCRIPTION - WORDCLOUD', fontsize=11, fontweight='light',color="#112E4D")
    # ax.title.set_position([.5, 1.05]) # Adjust the position of the title

    # # Display the wordcloud on the new figure
    # ax.imshow(wordcloud)
    # ax.set_xticks([])
    # ax.set_yticks([])

    # col1, col2, col3 = st.columns((1.8,0.6,0.6))
    # df_gi['Self Description'] = df_gi['description_general']
    # col1.pyplot(fig)
    # with st.expander("Read the Self Descriptions here"):
    #     st.table(df_gi[['InitName','Self Description']])
        
    
    # st.markdown("### PARTNERS' UNDERSTANDING OF RESILIENCE")
    # st.markdown("""Visual representation of the words most frequently used by RtR Partners when explaining their understanding of resilience.
    # """)

    # ## WORDCLOUD
    # df_wordcloud = df_gi
    # df_wordcloud['resilience_definition'] = df_wordcloud['resilience_definition'].fillna("")
    # df_wordcloud['resilience_definition'] = df_wordcloud['resilience_definition'].astype(str)
    # text = ' '.join(df_wordcloud['resilience_definition'])
    # st.set_option('deprecation.showPyplotGlobalUse', False)
    # wordcloud = WordCloud(stopwords=STOPWORDS, background_color='white', width=800, height=640, colormap="RdPu").generate(text)

    # # Create a new figure and add a title
    # fig, ax = plt.subplots()
    # ax.set_title("RtR PARTNERS' UNDERSTANDING OF RESILIENCE - WORDCLOUD", fontsize=11, fontweight='light',color="#112E4D")
    # ax.title.set_position([.5, 1.05]) # Adjust the position of the title

    # # Display the wordcloud on the new figure
    # ax.imshow(wordcloud)
    # ax.set_xticks([])
    # ax.set_yticks([])

    # col1, col2, col3 = st.columns((1.8,0.6,0.6))
    # df_gi['resilience_definition'] = df_gi['resilience_definition']
    # col1.pyplot(fig)
    # with st.expander("Read the Self Descriptions here"):
    #     st.table(df_gi[['InitName','resilience_definition']])









    # #___________________________________________
    # #___________________________________________
    # #___________________________________________
    # #___________________________________________
    # # END SELF DESCRIPTION 
    # #___________________________________________
    # #___________________________________________
    # #___________________________________________
    # #___________________________________________



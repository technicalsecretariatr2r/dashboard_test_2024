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




def selfdescription_partner_finder(df_gi,p_short_name):
    # #___________________________________________
    # #___________________________________________
    # #___________________________________________
    # #___________________________________________
    # # SELF DESCRIPTION 
    # #___________________________________________
    # #___________________________________________
    # #___________________________________________
    # #___________________________________________

    st.markdown("##### WORDCLOUD")
    st.markdown(f"""Word cloud highlighting {p_short_name}'s key terms related to their resilience-building initiatives and goals.""")
    
    ## WORDCLOUD
    df_wordcloud = df_gi
    df_wordcloud['q21'] = df_wordcloud['q21'].astype(str)
    text = ' '.join(df_wordcloud['q21'])
    st.set_option('deprecation.showPyplotGlobalUse', False)
    wordcloud = WordCloud(stopwords=STOPWORDS, background_color='white', width=800, height=640, colormap="RdPu").generate(text)

    # Create a new figure and add a title
    fig, ax = plt.subplots()
    ax.set_title(p_short_name+' SELF-DESCRIPTION', fontsize=11, fontweight='light',color="#112E4D")
    ax.title.set_position([.5, 1.05]) # Adjust the position of the title

    # Display the wordcloud on the new figure
    ax.imshow(wordcloud)
    ax.set_xticks([])
    ax.set_yticks([])

    col1, col2, col3 = st.columns((1.8,0.6,0.6))
    df_gi['Self Description'] = df_gi['q21']
    col1.pyplot(fig)
    # with st.expander("Read the Self Descriptions here"):
    #     st.table(df_gi[['InitName','Self Description']])


    # #___________________________________________
    # #___________________________________________
    # #___________________________________________
    # #___________________________________________
    # # END SELF DESCRIPTION 
    # #___________________________________________
    # #___________________________________________
    # #___________________________________________
    # #___________________________________________



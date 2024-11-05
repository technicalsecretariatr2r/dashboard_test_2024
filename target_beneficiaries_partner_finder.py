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



# #____________________________________________
# #___________________________________________
#___________________________________________
#___________________________________________
# # BLOQUE PRIORITY GROUPS
# #___________________________________________
#___________________________________________
#___________________________________________

def priority_groups_partnerfinder(df_gi,p_short_name):
    # Chart #3 Priority Groups Action GI
    st.markdown(f"#### TARGET BENEFICIARIES")
    st.caption(f"Presentation of {p_short_name} targeted efforts aimed at priority groups and beneficiaries to combat climate change hazards.")
    st.markdown(f"{p_short_name} presents targeted initiatives, emphasizing a commitment to combating climate challenges faced by priority groups and beneficiaries, particularly those most vulnerable. Priority groups reflect specific populations that have a higher level of vulnerability, exposure or need in the context of a particular initiative's action, acknowledging human rights, social equity, and  well-being of future generations. This approach reflects a joint commitment to increase resilience to climate change through tailored interventions that prioritize those most susceptible to its impacts.")

    # Your existing data preparation code
    pp_list = ['q34', 'q35', 'q36', 'q37', 'q38', 'q39', 'q40', 'q41', 'q42', 'q43']
    df_gi2 = df_gi[pp_list]

    # Calculate the percentages
    percentages = df_gi2.count() / len(df_gi2)

    # Prepare data for the horizontal bar chart
    categories = ['Women and girls', 'LGBTQIA+', 'Elderly', 'Children and Youth', 'Disabled', 'Indigenous or traditional communities', 'Racial, ethnic and/or religious minorities', 'Refugees', 'Low income communities', 'Other']

    # Set the Seaborn palette
    sns.set_palette("RdPu")
    colors = sns.color_palette("RdPu", n_colors=len(categories))

    # Create the horizontal bar chart
    fig_pp = go.Figure(data=[
        go.Bar(
            y=categories,
            x=percentages,
            marker_color=colors.as_hex(),  # Apply RdPu colors
            orientation='h'  # Horizontal bars
        )
    ])

    # Update layout
    fig_pp.update_layout(
        title=f" {p_short_name} Targeted Priority Groups",
        title_x=0.5,
        yaxis_title="Priority Groups",
        xaxis_title=p_short_name,
        xaxis=dict(range=[0, 1], nticks=2)  # Adjust x-axis range and tick marks
    )

    # Display the plot in Streamlit
    st.markdown(f"The bar chart below displays whether priority groups are being taken into consideration by {p_short_name}.")
    st.write(fig_pp)
    # #___________________________________________
    # #___________________________________________
    # #___________________________________________
    # #___________________________________________
    # # END BLOCK PRIORITY GROUPS
    # #___________________________________________
    # #___________________________________________
    # #___________________________________________
    # #___________________________________________


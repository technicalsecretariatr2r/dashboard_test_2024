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


def campaign_overview_general_metrics(n_reporting_partners,n_all_rtrpartners_2023,n_newpartners2023,n_members2022,n_partnersreportinmembers2022,n_members2023,n_partnersreportinmembers2023):
#____________________________________________________________________________________________________________________________________________________________
##__________________________________________________________________________________________________________________________________________________________________
## SET 1 CAMPAIGN OVERVIEW	Insight into the campaign’s objectives and the global scale of its impact.
##__________________________________________________________________________________________________________________________________________________________________
#__________________________________________________________________________________________________________________________________________________________________

    ##___________________________________________
    ##___________________________________________
    ##___________________________________________
    ## CHARTS PARTNERS - ALL 
    ##___________________________________________
    ##___________________________________________
    ##___________________________________________

    # Calculate the percentages relative to the total number of partners
    percent_reporting = (n_reporting_partners / n_all_rtrpartners_2023) * 100
    percent_new = (n_newpartners2023 / n_all_rtrpartners_2023) * 100

    # Set colors from the RdPu palette
    colors = sns.color_palette("RdPu", n_colors=2)

    # Define the size of the figure
    fig_width = 8  # Width of the figure
    fig_height = 2  # Height of the figure

    # Create the figure and horizontal bar chart with defined size
    fig_all_partners, ax = plt.subplots(figsize=(fig_width, fig_height))

    # Plotting the horizontal bars for reporting and new partners on the same bar
    bars = ax.barh(['Partners'], [n_reporting_partners], color=colors[0], label='Reporting Partners')
    ax.barh(['Partners'], [n_newpartners2023], left=[n_reporting_partners], color=colors[1], label='New Partners')

    # Adding labels inside each section of the bar with absolute number and percentage
    # For Reporting Partners
    midpoint_reporting = n_reporting_partners / 2
    ax.text(midpoint_reporting, 0, f'{n_reporting_partners} Reporting Partners \n - Partners Participating in the 2023 Reporting Process -  \n({percent_reporting:.1f}%)',
            va='center', ha='center', color='black')

    # For New Partners
    midpoint_new = n_reporting_partners + (n_newpartners2023 / 2)
    ax.text(midpoint_new, 0, f'{n_newpartners2023} \nNo Reporting\nPartners\n({percent_new:.1f}%)',
            va='center', ha='center', color='black')

    # Set labels
    ax.set_xlabel('Number of Partners')
    ax.set_yticklabels([])  # Hide the y-axis labels
    ax.set_title('Total Number of RtR Partner by COP28', fontsize=11)


    # Remove top and right spines
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    # Add annotation text
    annotation_text = f"N = {n_all_rtrpartners_2023} Partners"
    fig_all_partners.text(0.95, 0.0, annotation_text, ha='right', va='bottom', fontsize=10, color='black')  # Adjust coordinates and alignment

    # Adjust layout to fit and show the bar chart properly
    plt.tight_layout()

    # Show the figure in the Streamlit app
    # st.write("Partners")


    long_description = f"""
    ## CURRENT PARTNERS
    As the first-ever Global Stocktake is set to conclude at the UN Climate Change Conference COP28 and the definition of a Global Goal on Adaptation makes significant advances, **the Race to Resilience Campaign presents here its contribution to the progress on adaptation delivered by the Non-Party Stakeholders**. **The overarching goal: putting people and nature first, making 4 billion people more resilient to climate change by 2030**.
    The strength of the Campaign lies on the joint ambition shared by {n_all_rtrpartners_2023} partners and its more than {n_members2023} members who implement locally-led adaptation actions for the benefit of the most vulnerable. This strength is underpinned by a credible, comprehensive, and transparent progress tracking framework that unites all partners and members in translating pledges into action. 
    """
    

    st.markdown(long_description)


    st.markdown("#### RtR CURRENTLY FEATURES:")
    col1, col2, col3,col4 = st.columns(4)
    col1.metric("All RtR Partners",n_all_rtrpartners_2023)
    col2.metric("Reporting Partners in 2023",n_reporting_partners)
    col3.metric("No Reporting Partners",n_newpartners2023)
    col4.metric("Members organizations (Updated 2023)",n_members2023,"(out of "+str(n_partnersreportinmembers2023)+" partners)")##
    st.markdown('''<a style="font-weight:bold" href="https://racetozero.unfccc.int/meet-the-partners/">Meet the Partners Here</a>
                ''', unsafe_allow_html=True)
    col1, col2, col3 = st.columns ([0.1,2.8,0.1])
    col2.pyplot(fig_all_partners)
    
    
    st.write("")
    
    disclaimer = (
    f"<strong>IMPORTANT:</strong> Out of the {n_all_rtrpartners_2023} RtR Partners, "
    f"{n_reporting_partners} participated in the reporting process 2023. Consequently, "
    "this Data Explorer provides an overview of the progress achieved so far by these reporting partners. ")
    
    st.markdown(f"""
    <style>
    .disclaimer {{
        color: #112E4D; /* Dark blue text color */
        background-color: rgba(255, 55, 213, 0.1); /* Light pink background */
        padding: 10px;
        border-radius: 5px;
        border: 2px solid #FF37D5; /* Pink border */
        font-size: 16px;
        margin-bottom: 10px; /* Adds space below the disclaimer */
    }}
    </style>
    <div class="disclaimer">
        {disclaimer}
    </div>
    """, 
    unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
#     col1.metric("Members organizations 2022",n_members2022,"(out of "+str(n_partnersreportinmembers2022)+" partners by 2022)")##
#     col1.metric("Members organizations (Updated 2023)",n_members2023,"(out of "+str(n_partnersreportinmembers2023)+" partners)")##
#     with st.expander("*Explore the differences between members here:"):
#         st.markdown("Differences in member counts are due to initiatives no longer being partners and thus not being included. In the 2023 reporting process, Partner Initiatives might have reported fewer members because they were required to explicitly identify organizations that align with the following definition: *In RtR, a member of an RtR Partner is defined as: an implementer, collaborator (partner organization), endorser, or donor - entities that directly contribute to the pledge, plan, and resilience actions reported by your initiative to the campaign, and have consented to be linked to the RtR through the partner initiative.* During the 2022 reporting process, they were not as strict with this definition and included all related organizations, regardless of their consent to be linked to RtR. Additionally, a significant number of RtR Initiatives have not yet reported their member counts for the 2023 process. As a result, this number is expected to increase in subsequent metric updates")


    ##___________________________________________
    ##___________________________________________
    ##___________________________________________
    ## END CHART PARTNERS - ALL 
    ##___________________________________________
    ##___________________________________________
    ##___________________________________________




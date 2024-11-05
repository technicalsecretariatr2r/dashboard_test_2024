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



# def priority_groups_campaign_overview(df_gi,n_reporting_partners):
#     # Chart #3 Priority Groups Action GI
#     st.markdown("### TARGET BENEFICIARIES")
#     st.caption("Presentation of partners' targeted efforts aimed at priority groups and beneficiaries to combat climate change hazards.")
#     st.markdown("Partners present targeted initiatives, emphasizing a commitment to combating climate challenges faced by priority groups and beneficiaries, particularly those most vulnerable. Priority groups reflect specific populations that have a higher level of vulnerability, exposure or need in the context of a particular initiative's action, acknowledging human rights, social equity, and  well-being of future generations. This approach reflects a joint commitment to increase resilience to climate change through tailored interventions that prioritize those most susceptible to its impacts.")

#     # list of columns with Priority Groups
#     pg_list = ['q35', 'q36', 'q37', 'q38', 'q39', 'q40', 'q41', 'q42','q43']

#     # Use .any() function to check if any value in the row is True (i.e., is not NaN), then sum up these True values
#     pg_all = df_gi[pg_list].notna().any(axis=1).sum()
#     pg_others = df_gi['q44'].count()
#     pg_noneofabove = df_gi['q34'].count()


#     ## CHART PRIORITY GROUP %

#     pp_list = ['q35', 'q36', 'q37', 'q38', 'q39', 'q40', 'q41', 'q42', 'q43','q44']
#     df_gi2 = df_gi[pp_list]
#     total = n_reporting_partners  # Total number

#     # Count the values and calculate percentages
#     pg0 = (df_gi2["q35"].count() / total) * 100  # Women and girls
#     pg1 = (df_gi2["q36"].count() / total) * 100  # LGBTQIA+
#     pg2 = (df_gi2["q37"].count() / total) * 100  # Elderly
#     pg3 = (df_gi2["q38"].count() / total) * 100  # Children and Youth
#     pg4 = (df_gi2["q39"].count() / total) * 100  # Disabled
#     pg5 = (df_gi2["q40"].count() / total) * 100  # Indigenous or traditional communities
#     pg6 = (df_gi2["q41"].count() / total) * 100  # Racial, ethnic and/or religious minorities
#     pg7 = (df_gi2["q42"].count() / total) * 100  # Refugees
#     pg8 = (df_gi2["q43"].count() / total) * 100  # Low income communities
#     pg9 = (df_gi2["q44"].count() / total) * 100  # Other


#     s_df_gi2 = pd.DataFrame(dict(
#         r_values=[pg0, pg1, pg2, pg3, pg4, pg5, pg6, pg7, pg8, pg9],
#         theta_values=['Women and girls','LGBTQIA+','Elderly','Children and Youth','Disabled','Indigenous or traditional communities','Racial, ethnic and/or religious minorities','Refugees','Low income communities','Other']))

#     # Data
#     r_values = [pg0, pg1, pg2, pg3, pg4, pg5, pg6, pg7, pg8,pg9]
#     theta_values = ['Women and girls','LGBTQIA+','Elderly','Children and Youth','Disabled','Indigenous or traditional communities','Racial, ethnic and/or religious minorities','Refugees','Low income communities','Other']

#     # Create the plot
#     fig_pp = go.Figure(data=go.Scatterpolar(
#         r=r_values,
#         theta=theta_values,
#         mode='lines',
#         fill='toself',
#         line=dict(color='#FF37D5', width=1)
#     ))

#     fig_pp.update_layout(
#         polar=dict(
#             radialaxis=dict(
#                 tickfont=dict(color='#112E4D'),
#                 title=dict(
#                     text="(%) Partners",
#                     font=dict(size=14, color='black')
#                 )
#             ),
#             angularaxis=dict(
#                 tickfont=dict(size=12, color='black')
#             ),
#         ),
#         title="RtR Partners' Targeted Priority Groups"
#     )
#     # Update layout
#     fig_pp.update_layout(
#     title="RtR Partners' Targeted Priority Groups",
#     # annotations=[
#     #     go.layout.Annotation(
#     #         x=1,
#     #         y=0,
#     #         text='Out of ' + str(n_reporting_partners) + ' RtR Partners reporting about the Priority Groups',
#     #         showarrow=False,
#     #         yshift=-60
#     #     )
#     # ]
# )
#     st.write("RtR Partners' Targeted Priority Groups (%) OFICIAL")
#     st.write(fig_pp)

#     # #___________________________________________
#     # #___________________________________________
#     # #___________________________________________
#     # #___________________________________________
#     # # END BLOCK PRIORITY GROUPS
#     # #___________________________________________
#     # #___________________________________________
#     # #___________________________________________
#     # #___________________________________________


def priority_groups_campaign_overview_bar_chart(df_gi, n_reporting_partners):
    st.markdown("### TARGET BENEFICIARIES")
    st.caption("Presentation of partners' targeted efforts aimed at priority groups and beneficiaries to combat climate change hazards.")
    st.markdown("Partners present targeted initiatives, emphasizing a commitment to combating climate challenges faced by priority groups and beneficiaries, particularly those most vulnerable. Priority groups reflect specific populations that have a higher level of vulnerability, exposure or need in the context of a particular initiative's action, acknowledging human rights, social equity, and  well-being of future generations. This approach reflects a joint commitment to increase resilience to climate change through tailored interventions that prioritize those most susceptible to its impacts.")

    # List of columns with Priority Groups
    pg_list = ['q35', 'q36', 'q37', 'q38', 'q39', 'q40', 'q41', 'q42', 'q43']
    
    # Count the values and calculate percentages
    total = n_reporting_partners  # Total number
    pg0 = (df_gi["q35"].count() / total) * 100  # Women and girls
    pg1 = (df_gi["q36"].count() / total) * 100  # LGBTQIA+
    pg2 = (df_gi["q37"].count() / total) * 100  # Elderly
    pg3 = (df_gi["q38"].count() / total) * 100  # Children and Youth
    pg4 = (df_gi["q39"].count() / total) * 100  # Disabled
    pg5 = (df_gi["q40"].count() / total) * 100  # Indigenous or traditional communities
    pg6 = (df_gi["q41"].count() / total) * 100  # Racial, ethnic and/or religious minorities
    pg7 = (df_gi["q42"].count() / total) * 100  # Refugees
    pg8 = (df_gi["q43"].count() / total) * 100  # Low income communities
    pg9 = (df_gi["q44"].count() / total) * 100  # Other
    
    # Counts for each group
    counts = [
        df_gi["q35"].count(), df_gi["q36"].count(), df_gi["q37"].count(), df_gi["q38"].count(), 
        df_gi["q39"].count(), df_gi["q40"].count(), df_gi["q41"].count(), df_gi["q42"].count(),
        df_gi["q43"].count(), df_gi["q44"].count()
    ]
    
    data = {
        'Priority Group': [
            'Women and girls', 'LGBTQIA+', 'Elderly', 'Children and Youth', 
            'Disabled', 'Indigenous or traditional communities', 
            'Racial, ethnic and/or religious minorities', 'Refugees', 
            'Low income communities', 'Other'
        ],
        'Percentage': [pg0, pg1, pg2, pg3, pg4, pg5, pg6, pg7, pg8, pg9],
        '2024': counts
    }

    data_priority_group_2024 = pd.DataFrame(data)
    
    data_priority_group_2024 = data_priority_group_2024.sort_values(by='2024', ascending=False)

    # Create the bar chart
    fig, ax = plt.subplots(figsize=(10, 4))

    bars = ax.barh(data_priority_group_2024['Priority Group'], data_priority_group_2024['Percentage'], color=['#FF37D5'])

    # Add the count labels next to each bar
    for bar, count, percentage in zip(bars, data_priority_group_2024['2024'], data_priority_group_2024['Percentage']):
        ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2,
                f'{percentage:.1f}% ({count} Partners)', va='center')
                # f'{percentage:.1f}%', va='center')
                # f'{count} Partners ({percentage:.1f}%)', va='center')

    # Set the x-axis limit to 100%
    ax.set_xlim(0, 100)

    # Set labels and title
    ax.set_xlabel('Percentage of Reporting Partners (%)')
    ax.set_title('RtR Partners\' Targeted Priority Groups')

    # Disable lines in the chart area
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    # ax.spines['left'].set_visible(False)
    # ax.spines['bottom'].set_visible(False)
    # ax.grid(False)

    plt.gca().invert_yaxis()  # Invert y-axis to have the largest bar on top
    plt.tight_layout()

    # # Add a text box below the chart
    # plt.figtext(0.99, 0.01, f'Out of {n_reporting_partners} RtR Partners reporting about the Priority Groups',
    #             horizontalalignment='right', fontsize=10, weight='bold')

     # Add a text box below the chart
    plt.figtext(0.99, 0.01, f'N = {n_reporting_partners}',
                horizontalalignment='right', fontsize=10, weight='normal')

    # Display the chart in Streamlit
    # st.pyplot(fig)
    
    

    
    ##Creating comparation table
    
    # Define the data
    data_priority_group_2022 = {
        'Priority Group': ['Women and girls', 'Children and Youth', 'Low income communities', 'Indigenous or traditional communities', 
                'Elderly', 'Disabled', 'Racial, ethnic and/or religious minorities', 'Refugees', 'LGBTQIA+'],
        '2022': [19, 16, 13, 12, 8, 7, 4, 3, 2]
    }

    # Create the DataFrame
    data_priority_group_2022 = pd.DataFrame(data_priority_group_2022)

    
    # Create a dictionary with the given data
    data_priority_group_2023 = {
        'Priority Group': [
            'Women and girls', 
            'Low income communities', 
            'Disabled', 
            'Children and Youth', 
            'Other', 
            'Elderly', 
            'Refugees', 
            'Indigenous or traditional communities', 
            'Racial, ethnic and/or religious minorities', 
            'LGBTQIA+'
        ],
        '2023': [18, 17, 15, 15, 14, 9, 8, 6, 5, 5]
    }

    # Convert the dictionary to a pandas DataFrame
    data_priority_group_2023 = pd.DataFrame(data_priority_group_2023)

    data_priority_group_2024 = data_priority_group_2024[['Priority Group','2024']]
    
    # df_priority_group_comparison = pd.merge(data_priority_group_2022, data_priority_group_2023, on='Priority Group', how='outer')
    df_priority_group_comparison_23_24 = pd.merge(data_priority_group_2023, data_priority_group_2024, on='Priority Group', how='outer')

    df_priority_group_comparison_23_24 = df_priority_group_comparison_23_24[df_priority_group_comparison_23_24['Priority Group'] != "Other"]

    # Display the comparison DataFrame in Streamlit
    # st.write(df_priority_group_comparison_23_24)

  
    # Chart comparation 2023-2024
    
    
    # Convert the 2023 and 2024 values into percentages
    df_priority_group_comparison_23_24['2023_percent'] = (df_priority_group_comparison_23_24['2023'] / n_reporting_partners) * 100
    df_priority_group_comparison_23_24['2024_percent'] = (df_priority_group_comparison_23_24['2024'] / n_reporting_partners) * 100
    
    df_priority_group_comparison_23_24 = df_priority_group_comparison_23_24.sort_values(by='2024', ascending=True)
    
    # Set the Seaborn palette
    sns.set_palette("RdPu")

    # Set up the plot
    fig, ax = plt.subplots(figsize=(10, 4))

    # Define the position of the bars
    bar_width = 0.35
    index = np.arange(len(df_priority_group_comparison_23_24))
    
    # Set the x-axis limits from 0 to 100%
    ax.set_xlim(0, 100)

    # Set the x-axis ticks at intervals of 10 points
    ax.set_xticks(np.arange(0, 101, 10))

    # Plot 2023 and 2024 bars side by side
    bars_2023 = ax.barh(index, df_priority_group_comparison_23_24['2023_percent'], bar_width, label='2023') #, color='lightblue')
    bars_2024 = ax.barh(index + bar_width, df_priority_group_comparison_23_24['2024_percent'], bar_width, label='2024') #, color='salmon')

    # Set labels
    ax.set_xlabel('Percentage (%)')
    ax.set_ylabel('Priority Groups')
    ax.set_yticks(index + bar_width / 2)
    ax.set_yticklabels(df_priority_group_comparison_23_24['Priority Group'])
    
    # Disable lines in the chart area
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    

    # Add a legend
    ax.legend()

    # Title
    ax.set_title("RtR Partner’s Targeted Priority Groups (2023 and 2024)")
    
     # Add a text box below the chart
    plt.figtext(0.99, 0.01, f'N = {n_reporting_partners}',
                horizontalalignment='right', fontsize=10, weight='normal')

    # Display the plot in Streamlit
    st.pyplot(fig)
    
    
    
    
    
    
    
    
    
    
    
    
    
    # Chart 2
    
    
    
    # def priority_groups_per_partner_bar_chart(df_gi):
    # List of columns representing priority groups
    pg_list = ['q35', 'q36', 'q37', 'q38', 'q39', 'q40', 'q41', 'q42', 'q43', 'q44']
    
    # Create a new column 'Total Priority Groups' by summing across the priority group columns
    df_gi['Total Priority Groups'] = df_gi[pg_list].notnull().sum(axis=1)

    # Extract Partner names and total priority groups reported by each partner
    partners_total = df_gi[['InitName', 'Total Priority Groups']].sort_values(by='Total Priority Groups', ascending=False)
    

    # Create the bar chart
    fig, ax = plt.subplots(figsize=(10, 6))
    
    bars = ax.barh(partners_total['InitName'], partners_total['Total Priority Groups'], color=['#FF37D5'])

    # Add the count labels next to each bar
    for bar, total_groups in zip(bars, partners_total['Total Priority Groups']):
        ax.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2, 
                f'{total_groups}', va='center')
        
    ax.tick_params(axis='y', labelsize=8) 

    # Set labels and title
    ax.set_xlabel('Total Number of Priority Groups')
    ax.set_title('Total Priority Groups Reported by RtR Partners')

    # Disable lines in the chart area
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.gca().invert_yaxis()  # Invert y-axis to have the largest bar on top
    plt.tight_layout()

    # Display the chart in Streamlit
    st.pyplot(fig)
    
    
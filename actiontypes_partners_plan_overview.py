
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


def action_types_consolidated(df_2023_plan, n_total_plans_consolidated, n_partners_plan,df_2023_plan_summary):
    ###__________________________________________________________________________________
    ## PLAN ACTION TYPES PLAN CONSOLIDADO
    ###__________________________________________________________________________________
    
    def intro_resilience_actions():
        st.markdown("### RESILIENCE ACTIONS")
        st.caption("Highlighting the diverse actions taken by partners to foster resilience, demonstrating their impact.")
        st.markdown("""When partners submit their plans, they are required to indicate the type of resilience action they are undertaking. Then, all these specific actions are grouped according to the action types categorization of the Marrakech Partnership for Global Climate Action.
        
The following bar chart presents the number of Partners' Plans dedicated to each action type.""")
    intro_resilience_actions()

    def makingdataset_rsilience_actions():
    
        list_action_areas = ['x14','x15','x16','x17','x18','x19','x20','x21','x22',]
        # df_2023_plan[list_action_areas] 

        update_action_types = {'x14':'Climate risk and vulnerability assessments, disclosure and monitoring actions',
        'x15':'Access to early warning systems and development of early actions.',
        'x16':'Preparedness with contingency plans and emergency response',
        'x17':'Establishment of effective governance to manage climate risks accompanied by human and institutional capacity-building',
        'x18':'Nature-based solutions used to reduce risks',
        'x19':'Climate-proofing of infrastructure and services',
        'x21':'Sharing of knowledge and best practices on climate risk management',
        'x20':'Risk transfer: insurance and social protection instruments',
        'x22':'Increase in the volume, quality and access of public and private finance to invest in resilience',
        }

        # Counting occurrences where each action area is not False
        ac_counts = {
            'x14': df_2023_plan[df_2023_plan['x14'] != False]['x14'].count(),
            'x15': df_2023_plan[df_2023_plan['x15'] != False]['x15'].count(),
            'x16': df_2023_plan[df_2023_plan['x16'] != False]['x16'].count(),
            'x17': df_2023_plan[df_2023_plan['x17'] != False]['x17'].count(),
            'x18': df_2023_plan[df_2023_plan['x18'] != False]['x18'].count(),
            'x19': df_2023_plan[df_2023_plan['x19'] != False]['x19'].count(),
            'x20': df_2023_plan[df_2023_plan['x20'] != False]['x20'].count(),
            'x21': df_2023_plan[df_2023_plan['x21'] != False]['x21'].count(),
            'x22': df_2023_plan[df_2023_plan['x22'] != False]['x22'].count()
        }
        # Creating a DataFrame from the counts
        action_types_df = pd.DataFrame(list(ac_counts.items()), columns=['Action Type', 'Count'])
        # Mapping action areas to descriptive text
        action_types_df['Action Type'] = action_types_df['Action Type'].map(update_action_types)
        action_types_df = action_types_df.sort_values(by='Count', ascending=True)


        # Define a function to split long labels into multiple lines
        def split_label(label, max_chars=60):
            words = label.split()
            split_labels = ['']
            current_line = 0

            for word in words:
                # Check if adding the next word would exceed the max_chars limit
                if len(split_labels[current_line]) + len(word) > max_chars:
                    # Check if we are already at 2 lines, if so, append the rest to the last line
                    if current_line == 1:
                        split_labels[current_line] += ' ' + word
                    else:
                        # Move to the next line if not
                        current_line += 1
                        split_labels.append(word)
                else:
                    # Add the word with a space if the line is not empty
                    if split_labels[current_line]:
                        split_labels[current_line] += ' ' + word
                    else:
                        split_labels[current_line] += word

            return '\n'.join(split_labels)

        # Apply the function to the labels
        action_types_df['Action Type Three Lines'] = action_types_df['Action Type'].apply(split_label)
        
        return action_types_df
    action_types_df = makingdataset_rsilience_actions()

    def chart_resilience_actions():
        # Creating the horizontal bar chart
        fig_height = len(action_types_df) * 0.6  # Adjust the figure height as needed
        fig, ax = plt.subplots(figsize=(10, fig_height))

        n_colors = 9
        # Start from a higher value than 0 to avoid the lightest colors
        start = 0.2  # Adjust this value as needed
        end = 1
        colors = cm.RdPu(np.linspace(start, end, n_colors))

        # Set the color of the bars using the 'color' parameter
        # bars = ax.barh(action_types_df['Action Type'], action_types_df['Count'], color='#FF37D5')
        bars = ax.barh(action_types_df['Action Type'], action_types_df['Count'], color=colors)
        ax.set_xlabel('Number of Plans')
        ax.set_ylabel('Marrakech Partnership Action Types')
        ax.set_title('Number of Plans by Marrakech Partnership Action Types')

        # Set the labels for y-axis with split text
        # Make sure 'Action Type Three Lines' is created in your DataFrame, similar to the split_label function you mentioned
        ax.set_yticks(action_types_df.index)
        ax.set_yticklabels(action_types_df['Action Type Three Lines'], fontsize=10)

        # Adjust the layout to prevent overlapping labels
        plt.tight_layout()

        annotation_text = f"Out of {n_total_plans_consolidated} plans from {n_partners_plan} Partners"
        fig.text(0.95, 0.00, annotation_text, ha='right', va='bottom', fontsize=8, color='black', transform=fig.transFigure)

        # Add values on each bar
        for bar in bars:
            label_x_pos = bar.get_width()
            label_y_pos = bar.get_y() + bar.get_height() / 2
            ax.text(label_x_pos, label_y_pos, s=f'  {int(bar.get_width())}', va='center', ha='left', fontsize=8)
        
        return fig
    fig = chart_resilience_actions()
    
    col1, col2, col3 = st.columns([2,0.5,0.5])
    with col1: 
        st.pyplot(fig)
    
    climate_actions = {
    "Climate risk and vulnerability assessments, disclosure and monitoring actions": "This category focuses on conducting thorough assessments of climate risks and vulnerabilities. It involves the disclosure of these assessments and continuous monitoring to inform and guide climate resilience strategies. The goal is to understand and communicate the extent of climate risks to better prepare and adapt to climatic changes.",
    "Access to early warning systems and development of early actions": "Establishes advanced warning systems to foresee and act before extreme or slow-evolving climatic events occur, developing rapid and efficient response capabilities at various levels.",
    "Preparedness with contingency plans and emergency response": "Integrates climate risk and vulnerability analysis into national emergency preparedness and response strategies, aiming to equip nations for handling and mitigating climatic disasters.",
    "Establishment of effective governance to manage climate risks accompanied by human and institutional capacity-building": "Encourages inclusive climate risk management in policy and action planning at all levels, with a focus on the most vulnerable and marginalized groups.",
    "Nature-based solutions used to reduce risks": "Promotes ecological and sustainable solutions in planning policies and practices, like ecosystem conservation and natural habitat restoration, to mitigate climate impacts.",
    "Climate-proofing of infrastructure and services": "Adapts and strengthens infrastructures and services to be resilient to climate risks, including updating building codes and engineering practices.",
    "Risk transfer: insurance and social protection instruments": "Develops insurance and social protection mechanisms responsive to climate risks to protect vulnerable and poor populations from extreme climatic events.",
    "Sharing of knowledge and best practices on climate risk management": "Promotes the exchange of strategies for effective and sustainable climate risk management, focusing on increasing climate resilience.",
    "Increase in the volume, quality and access of public and private finance to invest in resilience": "Boosts financial resources for climate adaptation and resilience projects, focusing on mobilizing public and private investments."}
    
    action_types = list(climate_actions.keys())

    selected_action = st.selectbox("Select an Action Type from the Marrakech Partnership for Global Climate Action to read its definition", action_types)

    if selected_action:
        st.markdown(f"#### {selected_action}:")
        st.markdown(f"*Definition:* {climate_actions[selected_action]}")
        # st.write("___")
    
    # st.write(df_2023_plan_summary.columns)
    
    list_variales_plan = [
            "InitName",
            "Org_Type",
            "plan_name",
            "plan_description",
            "action_clusters_plan_concat",
            "action_clusters_plan_counts",]
    

    df_action_types_plans = df_2023_plan_summary[list_variales_plan]
    
    # df_action_types_plans = df_action_types_plans[df_action_types_plans["action_clusters_plan_concat"].str.contains(selected_action, na=False)]

    st.write("##### Partners Plans: Action Clusters Details")
    st.caption("Figure under development")
    st.write(df_action_types_plans)

# action_types_consolidated(df_2023_plan, n_total_plans_consolidated, n_partners_plan,df_2023_plan_summary)





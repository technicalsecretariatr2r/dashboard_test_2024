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


def action_cluster_to_partner_finder(df_gi,ac_atypes,p_short_name):
    st.markdown("#### IDENTIFICATION OF RESILIENCE ACTION CLUSTERS")
    st.caption("In this section, RtR Partners are asked to identify and elaborate on the resilience actions taken by their initiative, which are categorized into Action Clusters.")
    st.markdown("""Resilience Action Clusters serve to identify and categorise actions focused on building climate resilience. These emerged from a collaboration between different actors, originating in the collection of resilience actions from the Marrakech Partnership (Global Climate Action, 2021), the consulting firm Carbon Disclosure Project (CDP, 2022), and the IPCC Action List (IPCC, 2021). These actions were classified into 29 categories, the “Resilience Action Clusters”, which were validated by the campaign's Methodology Advisory Group (MAG). 
                
Resilience actions clusters usually include a combination of adaptation and response measures, as well as capacity building and awareness raising actions. Partner are asked to specify which action clusters align with their actions on the first step of the reporting tool: The General Information Survey. """)
    
    
        # Define the categories and descriptions as a dictionary
    action_clusters = {
        "Climate risk and vulnerability assessments, disclosure and monitoring actions": {
            "Monitoring and mapping of hazards and vulnerabilities": "Collection and analysis of geospatial and socioeconomic information to identify and assess areas and populations vulnerable to climate risks.",
            "Climate services and modelling": "Development of climate models to generate future climate projections and inform decision-making and planning.",
            "Generation and processing of data": "Collection and analysis of data relevant to climate resilience, and distribution of the findings through various information channels."
        },
        "Access to early warning systems and development of early actions": {
            "Early warning systems": "These systems issue alerts in case of detected extreme events, such as storms, floods or droughts, allowing for preventive measures and reducing damage."
        },
        "Preparedness with contingency plans and emergency response": {
            "Emergency preparedness": "Development of contingency plans, allocation of roles and resources, and training in response and recovery techniques to minimize impacts of climate disasters and ensure an effective response."
        },
        "Establishment of effective governance to manage climate risks accompanied by human and institutional capacity-building": {
            "Environmental governance and resource management systems": "Implementation of sustainable policies and natural resource management systems, promoting collaboration in decision-making and resource management.",
            "Environmental laws and regulatory framework": "Creation and enforcement of laws and regulations that protect the environment, promote climate change adaptation, and encourage sustainable practices.",
            "Protected areas and property rights definitions": "Establishment of protected areas and clarification of property and resource use rights, including the rights of indigenous and local communities.",
            "Institutional-led climate adaptation planning processes": "Design and implementation of climate adaptation strategies and plans at different levels of government, including identification of vulnerabilities, climate risks, and priority actions.",
            "Building regulations and standards for climate resilience": "Development and implementation of regulations and standards that ensure buildings are climate resilient, promoting the adoption of sustainable construction practices."
        },
        "Nature-based solutions used to reduce risks": {
            "Measures to improve air quality and reduce pollution": "Implementation of policies, technologies and practices to improve air quality.",
            "Green infrastructure and other engineered nature-based solutions": "Design and implementation of infrastructures that use natural systems to improve climate resilience and provide additional environmental benefits.",
            "Conservation and restoration of terrestrial and aquatic ecosystems": "Protection and recovery of terrestrial and aquatic ecosystems to ensure their capacity to provide ecosystem services and contribute to climate resilience."
        },
        "Climate-proofing of infrastructure and services": {
            "Critical Infrastructure and Protective Systems": "Design, construction, and maintenance of critical infrastructure resilient to climate, incorporating climate considerations in planning and strengthening protective systems.",
            "Coastal Infrastructure Protection": "Implementation of measures to protect coastal infrastructure from extreme climate events and sea level rise, including coastal land use planning.",
            "Energy efficiency and renewable energy technologies": "Promotion and implementation of technologies and practices that reduce energy consumption and increase the use of renewable energy sources.",
            "Water security and quality": "Implementation of measures to ensure the availability, quality, and access to water in the context of climate change.",
            "Health services": "Strengthening and adapting health systems to face the challenges and risks associated with climate change.",
            "Food safety and sustainable services": "Implementation of practices and technologies to ensure the availability, access, and stability of food, promoting sustainability in the production, distribution, and consumption of food."
        },
        "Risk transfer: insurance and social protection instruments": {
            "Climate insurance and risk transfer": "Development and implementation of insurance and risk transfer products that help vulnerable communities and sectors to face and recover from the economic impacts of climate change.",
            "Social protection actions": "Implementation of social protection programs and policies that help vulnerable communities to face and adapt to the impacts of climate change, such as cash transfers, training, and technical assistance."
        },
        "Sharing of knowledge and best practices on climate risk management": {
            "Agricultural, livestock, forestry and aquacultural practices actions": "Promotion and implementation of sustainable and resilient practices in these sectors, such as crop diversification, agroforestry systems, and sustainable management of fishery resources.",
            "Community-based inclusive and participatory risk reduction": "Strengthening the capacity of local communities to identify, assess, and address climate risks in an inclusive and participatory manner.",
            "Climate hazard communication, information, and technology awareness": "Development and implementation of communication and education strategies and tools that help communities understand and address climate risks.",
            "Knowledge building for resilience": "Promotion and implementation of training and skill-building activities that strengthen the capacity of communities to cope with and adapt to climate change.",
            "Research and collaboration actions": "Fostering cooperation and knowledge exchange among institutions, sectors, and countries on climate resilience, including the development of joint projects and collaboration networks."
        },
        "Increase in the volume, quality and access of public and private finance to invest in resilience": {
            "Livelihood diversification and social economy": "Support for income source diversification and the promotion of sustainable and climate-resilient economic activities, including the creation and strengthening of cooperatives, micro-enterprises, and other forms of community economic organization.",
            "Financial and investment tools in case of climate disasters": "Development and implementation of financial instruments and investment strategies that help communities, businesses, and governments to mobilize resources for recovery and reconstruction after climate disasters.",
            "Economic incentives": "Establishment of economic incentives that promote the adoption of climate-resilient practices and technologies and the conservation of natural resources, including subsidies, tax credits, and ecosystem service payment systems."
        }
    }

    # Define selection options for action types
    action_type_names = ["Select Action Type"] + list(action_clusters.keys())

    # Create a selectbox for Action Types
    selected_action_type = st.selectbox('Select an Action Type:', action_type_names)

    # Initialize an empty list for cluster names
    cluster_names = ["Select Cluster"]

    # Update cluster_names based on the selected action type
    if selected_action_type != "Select a Marrakech Partnership Action Type":
        cluster_names += list(action_clusters[selected_action_type].keys())

    # Create a selectbox for Clusters that updates based on the selected action type
    selected_cluster = st.selectbox('Select a RtR Action Cluster:', cluster_names)

    # Function to display the selected Action Type and Cluster
    def display_selected_action_type_and_cluster(action_type, cluster):
        st.markdown("*Marrakech Partnership for Global Climate Action - Action Type:*")
        st.markdown(f"**{action_type}**")
        st.markdown("### RtR Action Cluster:")
        if cluster != "Select Cluster":
            st.markdown(f"- **{cluster}:** {action_clusters[action_type][cluster]}")
        else:
            for cluster_action, description in action_clusters[action_type].items():
                st.markdown(f"- **{cluster_action}:** {description}")
        st.markdown("---")  # Adds a horizontal line for better separation

    # Display based on selections
    if selected_action_type != "Select Action Type" and selected_cluster != "Select Cluster":
        display_selected_action_type_and_cluster(selected_action_type, selected_cluster)
    elif selected_action_type != "Select Action Type":
        # Display all clusters under the selected action type
        display_selected_action_type_and_cluster(selected_action_type, "Select Cluster")


    
    

    st.markdown(f"##### {p_short_name} RESILIENCE ACTION CLUSTERS")
    # st.caption("**Q54. Please review the descriptions of each Action Cluster. Choose the ones that correspond closely to your organization work related to RtR, considering that a separate plan may be needed for each cluster in future reports. In cases where a particular action of your organization could be associated with multiple clusters, please assign it to the one that represents it best. Don't hesitate to select as many Action Clusters as required to adequately represent the wide range of activities conducted by your organization.**")

    #Creating the FULL Action CLuster Data Set
    actioncluster_list = ['q157','q158','q159','q160','q161','q162','q163','q164','q165',
    'q166','q167','q168','q169','q170','q171','q172','q173','q174','q175',
    'q176','q177','q178','q179','q180','q181','q182','q183','q184','q185',]

    actioncluster_how_list = ['q186','q187','q188','q189','q190','q191','q192','q193','q194','q195','q196','q197',
                                'q198','q199','q200','q201','q202','q203','q204','q205','q206','q207','q208','q209','q210',
                                'q211','q212','q213','q214',]

    # cleaning dataset of how
    df_gi[actioncluster_how_list] = df_gi[actioncluster_how_list].replace('x', np.nan)

    # st.caption("dataframehow")
    # df_gi_how = df_gi[actioncluster_how_list]
    # st.write(df_gi_how)

    action_cluster_to_explanation = {
        'q157' : 'q186','q158' : 'q187','q159' : 'q188','q160' : 'q189',
        'q161' : 'q190','q162' : 'q191','q163' : 'q192','q164' : 'q193',
        'q165' : 'q194','q166' : 'q195','q167' : 'q196','q168' : 'q197',
        'q169' : 'q198','q170' : 'q199','q171' : 'q200','q172' : 'q201',
        'q173' : 'q202','q174' : 'q203','q175' : 'q204','q176' : 'q205',
        'q177' : 'q206','q178' : 'q207','q179' : 'q208','q180' : 'q209',
        'q181' : 'q210','q182' : 'q211','q183' : 'q212','q184' : 'q213','q185' : 'q214',
    }
    partner_names = ['InitName']

    # Combine the lists
    selected_columns = partner_names + actioncluster_list + actioncluster_how_list

    # Select the specific columns from the DataFrame
    df_gi_partners_actioncluster = df_gi[selected_columns]
    # st.caption("all variables needeed")
    # st.write(df_gi_partners_actioncluster)

    # Melt the actioncluster_list columns into individual rows
    df_gi_partners_actioncluster = df_gi.melt(id_vars=partner_names, value_vars=actioncluster_list, value_name='Action Clusters')

    # Rename the 'InitName' column to 'Partner'
    df_gi_partners_actioncluster.rename(columns={'InitName': 'Partner'}, inplace=True)

    # st.caption("Melt Action Cluster")
    # st.write(df_gi_partners_actioncluster.count())

    # Remove rows where either "Partner" or "Action Clusters" is NaN or empty
    df_gi_partners_actioncluster.dropna(subset=['Partner', 'Action Clusters'], inplace=True)

    # st.caption('Melt where either "Partner" or "Action Clusters" is NaN or empty')
    # st.write(df_gi_partners_actioncluster.count())

    # Remove rows where either "Partner" or "Action Clusters" is an empty string
    df_gi_partners_actioncluster = df_gi_partners_actioncluster[df_gi_partners_actioncluster['Partner'].str.strip() != '']
    df_gi_partners_actioncluster = df_gi_partners_actioncluster[df_gi_partners_actioncluster['Action Clusters'].str.strip() != '']

    # st.caption('Remove rows where either "Partner" or "Action Clusters" is an empty string')
    # st.write(df_gi_partners_actioncluster.count())
    # st.write(df_gi_partners_actioncluster)

    #Making Status Info Data Set
    df_gi_status_unique = df_gi[['Org_Type','InitName',]]
    df_gi_status_unique = df_gi_status_unique.rename(columns={'InitName': 'Partner', 
                                                        'Org_Type':'Relation to RtR',})
    #Merging Data with Status Info
    df_gi_partners_actioncluster = pd.merge(df_gi_partners_actioncluster, df_gi_status_unique, on='Partner', how='outer')
    #Merging Data with Action_Types_Info
    df_gi_partners_actioncluster = pd.merge(df_gi_partners_actioncluster, ac_atypes, on='variable', how='outer')

    #Concat to create a key
    df_gi_partners_actioncluster["key"] = df_gi_partners_actioncluster['Partner'].astype(str) + df_gi_partners_actioncluster['variable_how'].astype(str)
    # st.caption('DataFrame x Action Cluster+otra info')
    # st.write(df_gi_partners_actioncluster)

    #HOW
    # Melt the actioncluster_list columns into individual rows
    df_gi_partners_actioncluster_how = df_gi.melt(id_vars=partner_names, value_vars=actioncluster_how_list, value_name='HOW Action Clusters')

    # Rename the 'InitName' column to 'Partner'
    df_gi_partners_actioncluster_how.rename(columns={'InitName': 'Partner'}, inplace=True)
    df_gi_partners_actioncluster_how.rename(columns={'variable': 'variable_how'}, inplace=True)

    #Concat to create a key
    df_gi_partners_actioncluster_how["key"] = df_gi_partners_actioncluster_how['Partner'].astype(str) + df_gi_partners_actioncluster_how['variable_how'].astype(str)

    # st.caption("Melt Action Cluster How")
    # st.write(df_gi_partners_actioncluster_how)
    # st.write(df_gi_partners_actioncluster_how.count())

    # Remove rows where either "Partner" or "Action Clusters" is NaN or empty
    df_gi_partners_actioncluster_how.dropna(subset=['Partner', 'HOW Action Clusters'], inplace=True)

    # st.caption('HOW Melt where either "Partner" or "Action Clusters" is NaN or empty')
    # st.write(df_gi_partners_actioncluster_how.count())

    # Remove rows where either "Partner" or "Action Clusters" is an empty string
    df_gi_partners_actioncluster_how = df_gi_partners_actioncluster_how[df_gi_partners_actioncluster_how['Partner'].str.strip() != '']
    df_gi_partners_actioncluster_how = df_gi_partners_actioncluster_how[df_gi_partners_actioncluster_how['HOW Action Clusters'].str.strip() != '']

    # st.caption('HOW Remove rows where either "Partner" or "Action Clusters" is an empty string')
    # st.write(df_gi_partners_actioncluster_how.count())

    # st.caption('HOW DataFrame x Action Cluster HOW')
    # st.write(df_gi_partners_actioncluster_how)

    # st.caption('HOW DataFrame x Action Cluster HOW_edited')
    df_gi_partners_actioncluster_how = df_gi_partners_actioncluster_how[['key','HOW Action Clusters']]
    # st.write(df_gi_partners_actioncluster_how)

    #Combining datas sets
    #Merging Data with Status Info
    df_gi_partners_actioncluster_total = pd.merge(df_gi_partners_actioncluster, df_gi_partners_actioncluster_how , on='key', how='outer')
    # st.write(df_gi_partners_actioncluster_total.columns)
    new_order = ['Relation to RtR','Partner','variable','variable_how','key','Action Cluster_code','Action Clusters','HOW Action Clusters','Action Type_code','Actions Type (Marrakech)']
    df_gi_partners_actioncluster_total = df_gi_partners_actioncluster_total[new_order]

    # st.subheader('Total')
    # st.write(df_gi_partners_actioncluster_total)


    ## Making the Chart#1: Number of RtR Partners per Action Cluster

        # Define the dictionary mapping for action clusters
    action_cluster_dict = {
        'q157': 'Monitoring and mapping of hazards and vulnerabilities',
        'q158': 'Climate services and modelling',
        'q159': 'Generation and processing of data',
        'q160': 'Early warning systems',
        'q161': 'Emergency preparedness',
        'q162': 'Environmental governance and resource management systems',
        'q163': 'Environmental laws and regulatory framework',
        'q164': 'Building regulations and standards for climate resilience',
        'q165': 'Protected areas and property rights definitions',
        'q166': 'Institutional-led climate adaptation planning processes',
        'q167': 'Measures to improve air quality and reduce pollution',
        'q168': 'Green infrastructure and other engineered nature-based solutions',
        'q169': 'Conservation and restoration of terrestrial and aquatic ecosystems',
        'q170': 'Critical Infrastructure and Protective Systems',
        'q171': 'Coastal Infrastructure Protection',
        'q172': 'Energy efficiency and renewable energy technologies',
        'q173': 'Water security and quality',
        'q174': 'Health services',
        'q175': 'Food safety and sustainable services',
        'q176': 'Agricultural, livestock, forestry and aquacultural practices actions',
        'q177': 'Social protection actions',
        'q178': 'Community-based inclusive and participatory risk reduction',
        'q179': 'Climate hazard communication, information, and technology awareness',
        'q180': 'Knowledge building for resilience',
        'q181': 'Research and collaboration actions',
        'q182': 'Livelihood diversification and social economy',
        'q183': 'Climate insurance and risk transfer',
        'q184': 'Financial and investment tools in case of climate disasters',
        'q185': 'Economic incentives'
    }
    # Calculate the count of identified action clusters
    actioncluster_all = df_gi[actioncluster_list].notna().any(axis=1).sum()

    # Create a list to store the counts of each action cluster
    actioncluster_counts = [df_gi[column].notna().sum() for column in actioncluster_list]

    # Create a list to store the action cluster names
    actioncluster_names = [action_cluster_dict[column].strip() for column in actioncluster_list]

    # Store the counts and the names in a DataFrame
    df_gi_actionclusters = pd.DataFrame({
        'names': actioncluster_names,
        'counts': actioncluster_counts
    })

    # Sort the DataFrame in descending order of 'counts'
    df_gi_actionclusters = df_gi_actionclusters.sort_values(by='counts', ascending=False)



    # CHART ACTION CLUSTER

    # Chart:
    # Set the desired height for the chart
    fig_height = len(actioncluster_names) * 0.17

    # Create the horizontal bar chart
    fig, ax = plt.subplots(figsize=(8, fig_height))
    bars = ax.barh(df_gi_actionclusters['names'], df_gi_actionclusters['counts'], height=0.6)

    # Set the plot title and axis labels
    ax.set_title("Number of RtR Partners per Action Cluster", fontsize=10)
    ax.set_xlabel('Number of Partners', fontsize=8)
    ax.set_ylabel('Action Cluster', fontsize=8)
    # Invert the y-axis to display action clusters from top to bottom
    ax.invert_yaxis()
    # Set the x-axis tick range to advance by 1 point
    ax.set_xticks(range(0, max(df_gi_actionclusters['counts']) + 2, 1))

    # Set the font size for x-axis labels
    plt.xticks(fontsize=6)
    # Set the font size for action cluster names
    plt.yticks(fontsize=8)
    # Adjust the layout to prevent overlapping labels
    plt.tight_layout()
    # Add annotation text at the bottom right of the figure
    annotation_text = f"Out of {actioncluster_all} partners (Source: General Information Survey 2023)"
    # Place the text at the bottom right of the figure
    fig.text(0.95, 0.00, annotation_text, ha='right', va='bottom', fontsize=8, color='black', transform=fig.transFigure)


    # Add values on each bar
    for bar in bars:
        width = bar.get_width()
        label_y_pos = bar.get_y() + bar.get_height() / 2
        ax.text(width + 0.1, label_y_pos, s=f'{width}', fontsize=6, va='center', ha='left')

    # Show the plot in Streamlit
    st.pyplot(fig)


    ###Chart #2: Number of Action Clusters per RtR Partner
    # Transpose the DataFrame and count non-null actions for each partner
    df_gi_transposed = df_gi.set_index('InitName')[actioncluster_list].T
    partner_action_counts = df_gi_transposed.notna().sum()

    # Convert the Series to a DataFrame and reset the index
    df_gi_partners = partner_action_counts.to_frame(name='counts').reset_index()
    # Sort the DataFrame in descending order of 'counts'
    df_gi_partners = df_gi_partners.sort_values(by='counts', ascending=False)
    # Set the desired height for the chart
    fig_height = len(df_gi_partners) * 0.2
    # Create the horizontal bar chart
    fig, ax = plt.subplots(figsize=(8, fig_height))
    bars = ax.barh(df_gi_partners['InitName'], df_gi_partners['counts'], height=0.6)
    # Set the plot title and axis labels
    ax.set_title("Number of Action Clusters per RtR Partner", fontsize=10)
    ax.set_xlabel('Number of Action Clusters', fontsize=8)
    ax.set_ylabel('RtR Partner', fontsize=8)
    # Invert the y-axis to display partners from top to bottom
    ax.invert_yaxis()
    # Set the x-axis tick range to advance by 1 point
    ax.set_xticks(range(0, max(df_gi_partners['counts']) + 2, 1))
    # Set the font size for x-axis labels
    plt.xticks(fontsize=6)
    # Set the font size for partner names
    plt.yticks(fontsize=8)
    # Adjust the layout to prevent overlapping labels
    plt.tight_layout()

    # # Add annotation text at the bottom right of the figure
    # annotation_text = f"Out of {actioncluster_all} partners (Source: General Information Survey 2023)"
    # # Place the text at the bottom right of the figure
    # fig.text(0.95, 0.00, annotation_text, ha='right', va='bottom', fontsize=8, color='black', transform=fig.transFigure)


    # Add values on each bar
    for bar in bars:
        width = bar.get_width()
        label_y_pos = bar.get_y() + bar.get_height() / 2
        ax.text(width + 0.1, label_y_pos, s=f'{width}', fontsize=6, va='center', ha='left')

    # Show the plot in Streamlit
    st.pyplot(fig)
    
    # Selecting specific columns and dropping NaN values
    df_gi_partners_actioncluster_total = df_gi_partners_actioncluster_total[['Partner', 'Action Clusters', 'HOW Action Clusters', 'Actions Type (Marrakech)']].dropna()

    with st.expander("Explore Data"):
        st.dataframe(df_gi_partners_actioncluster_total)
        

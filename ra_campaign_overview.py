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


def ra_campaign(df_2023_plan):
    st.markdown("### ASSESSING RESILIENCE ATTRIBUTES: AN OVERVIEW OF RtR PARTNERS' PLANS")
    # st.caption("An assessment of resilience attributes, evaluating how partners' actions are effectively enhancing individual resilience to climate change.")
    st.markdown("Resilience Attributes are critical qualities enabling systems to withstand, adapt, and recover from adverse conditions. The identification and definition of these attributes and corresponding sub-categories were the result of an exhaustive collaborative process involving a literature review and expert consultations including the Race to Resilience's Methodological Advisory Group and stakeholders from the Resilience Knowledge Coalition. They serve as a predictive measure of resilience, aiding in the design, supervision, and initial assessment of resilient action. In this sense, interventions that positively impact these attributes are seen to improve the capacity of climate-vulnerable beneficiaries to respond to and adapt to changes. Within the context of the RtR's Metrics Framework, Resilience Attributes constitute the depth metrics, representing the qualitative dimension of the index that measures the increased resilience resulting from our partner's efforts.")
    
    # Define the two-level nested dictionary for Resilience Attributes and their Sub-Categories
    resilience_attributes = {
        "Preparedness and planning": {
            "definition": "This skill refers to the ability to anticipate, prepare for and proactively manage change and uncertainty.",
            "sub_categories": {
                "Preparedness": "This skill focuses on the ability to anticipate and prepare for situations of change and uncertainty. It involves not only the implementation of responses, warning systems, and action protocols, but also the early identification of potential threats. It is the competence to recognize the hazard, interpret its imminent proximity, and know how to act appropriately and effectively in the face of it. This preparedness not only mitigates the impact of threats, but can also provide opportunities for adaptation and growth in times of challenge.",
                "Planning": "This skill emphasizes the ability to develop short, medium, and long-term strategies that manage change and uncertainty, promoting continuous adaptation to climate change. Planning is a critical process that facilitates the generation of a resilient vision for the future. This approach includes establishing long-term perspectives, taking into account both current and future trends, creating more adaptive and collaborative methods that encourage the participation and engagement of various stakeholders, as well as the clear definition of desirable conditions for conservation and sustainable use of natural resources. This forward planning process aids in anticipating and preparing effective responses to situations of change and challenge."
            }
        },
        "Learning": {
            "definition": "This capacity involves the generation, assimilation and processing of new information and knowledge specifically linked to climate change adaptation and uncertainty management.",
            "sub_categories": {
                "Experiential learning": "This capacity refers to the ability to learn from past experiences and failures, avoiding repeating mistakes and encouraging greater caution in future decisions. Transformative or experiential learning is a process in which problematic frames of reference are reconfigured to make them more inclusive, open and reflective with the intention of changing the scenario and thus building resilience. Therefore, this type of learning becomes a vital tool for the growth and development of stronger and more enduring resilience.",
                "Educational learning": "This type of learning involves the generation, absorption and processing of new information and knowledge focused on climate change adaptation and uncertainty management. This process is characterized by its dynamism and constant evolution, which allows for the continuous incorporation and application of new information. Educational learning is not limited to the classroom, but also occurs through interaction with the community, participation in research projects and field work. Environmental education can be a strategy for educational learning, involving the development of analytical and critical skills to understand the complexity of climate change and its consequences."
            }
        },
        "Agency": {
            "definition": "Agency refers to the ability of an individual, system or community to exercise free choice in response to environmental change or other challenges.",
            "sub_categories": {
                "Autonomy": "The ability of an individual, system or community to independently make decisions and take actions in response to challenges or changes. This ability promotes more personalized and effective adaptation to specific circumstances, resulting in greater resilience.",
                "Leadership": "This capacity involves the ability to influence, guide and motivate others to achieve common goals in times of adversity. This skill requires not only the ability to make strategic decisions at critical moments, but also the skill to inspire trust, cohesion and action in others. Effective leadership can mobilize resources, foster collaboration, and lead recovery efforts in ways that overcome adversity and promote resilience.",
                "Decision Making": "This capacity refers to the ability to choose among different options in response to changes or challenges. This skill involves evaluating possible actions and their consequences, as well as choosing and executing a course of action. Effective decision making is critical to a timely and effective response to challenges, and can make the difference between failure and overcoming adversity. Sound judgment, the ability to make decisions under pressure, and the ability to learn from mistakes are key aspects of this subcategory of agency. These skills promote successful adaptation and recovery from adversity, which increases resilience."
            }
        },
        "Social Collaboration": {
            "definition": "Social collaboration embodies the capacity for self-organization and coordinated collective action, fostering a cooperative approach and combined efforts that elevate resilience.",
            "sub_categories": {
                "Collective Participation": "Collective participation is a vital aspect of resilience, enabling the mobilization of individuals and groups towards common goals. It fosters social cohesion and drives collaborative action, particularly in response to challenges like climate change. By promoting collective participation, communities strengthen their bonds, foster shared ownership and solidarity, and empower individuals to work together for the greater good.",
                "Connectivity": "This refers to the quality, depth, and strength of social relationships within a system or community. Enhanced connectivity creates a responsive, well-informed network that can rapidly disseminate vital information and resources, facilitate mutual support, and collectively implement strategies to deal with crisis situations.",
                "Coordination": "This refers to the ability to organize and align various elements, be they leaders, departments, or organizations, towards achieving shared goals. Effective coordination enhances the efficiency of crisis response, promotes the spirit of unity, fosters effective cooperation, and thereby fortifies resilience."
            }
        },
        "Flexibility": {
            "definition": "Flexibility is a capacity that refers to the ability to switch between different coping and adaptive strategies, based on new information and ongoing assessments.",
            "sub_categories": {
                "Diversity": "Diversity refers to the ability to maintain multiple adaptive strategies, which ensures an effective response to a variety of climatic situations or adversities. It promotes resilience by providing a variety of tools and approaches to deal with challenges.",
                "Redundancy": "Redundancy involves maintaining copies of key strategies to ensure continuity of critical functions, even in cases of failures or outages. Although redundancy may seem inefficient in times of normalcy, it can be crucial for survival and recovery during and after adversity."
            }
        },
        "Equity": {
            "definition": "Capacity of ensuring fair and equitable access to resources, respecting fundamental equal rights in decision-making, and incorporating all affected stakeholders in decision-making processes.",
            "sub_categories": {
                "Distributive equity": "The ability to ensure fair and equitable distribution and access to resources. In the context of resilience, it is critical to ensure that the benefits and costs of adaptation and recovery strategies are shared fairly and that no one is excluded or left behind.",
                "Equity Access": "The capacity to incorporate and integrate all affected actors and discourses into decision-making processes. Inclusiveness is crucial to ensure that decisions made are representative of the needs and aspirations of all stakeholders."
            }
        },
        "Assets": {
            "definition": "Assets represent the ability to access natural, financial, infrastructure, technological and service resources in times of need.",
            "sub_categories": {
                "Finance": "Finance refers to the capacity to access, manage and effectively use financial resources. The robustness of internal funding, i.e., funds generated and managed within the community or system, is often more significant than external funding sources.",
                "Infrastructure": "Infrastructure encompasses the physical and systematic facilities that are essential to the functioning and well-being of a community or society. Ensuring the resilience of infrastructure is critical, as these facilities act as platforms that can absorb and withstand catastrophes.",
                "Natural Resources": "The effective management and use of natural resources is fundamental to the life and well-being of communities and ecosystems. Sustainable management of natural resources ensures their long-term availability and enables adaptation and recovery in the face of climate shocks.",
                "Technologies": "Access to and use of appropriate technologies can significantly facilitate adaptation to climate change. These tools can contribute to building more resilient and sustainable systems.",
                "Basic services": "Access to a wide range of services is a crucial component of supporting climate change adaptation. A resilient system ensures that these services remain accessible and functional during shocks, ensuring the well-being of the community."
            }
        }
    }
    
    # Define the selection options
    attribute_names = ["Select Attribute"] + list(resilience_attributes.keys())
    sub_category_options = ["All Sub-Categories"]

    # Create a selectbox for Resilience Attributes
    selected_attribute = st.selectbox('Select a Resilience Attribute:', attribute_names)

    # Initialize an empty list for sub-category names
    sub_category_names = []

    # Update sub_category_names based on the selected attribute
    if selected_attribute != "Select Attribute":
        sub_category_names = sub_category_options + list(resilience_attributes[selected_attribute]["sub_categories"].keys())

    # Create a selectbox for Sub-Categories that updates based on the selected attribute
    selected_sub_category = st.selectbox('Select a Sub-Category:', sub_category_names)

    # Function to display the selected Resilience Attribute or Sub-Category
    def display_selected_information(attribute, sub_category):
        # Display attribute definition
        st.markdown(f"### {attribute}")
        st.markdown(f"*Definition:* {resilience_attributes[attribute]['definition']}")

        # If "All Sub-Categories" is selected or the list of sub-categories is empty, display all sub-categories
        if sub_category == "All Sub-Categories" or not sub_category:
            for sub_cat, description in resilience_attributes[attribute]["sub_categories"].items():
                st.markdown(f"- **{sub_cat}:** {description}")
        else:
            # Display the selected sub-category description
            st.markdown(f"- **{sub_category}:** {resilience_attributes[attribute]['sub_categories'][sub_category]}")
        
        st.markdown("---")  # Adds a horizontal line for better separation

    # Display based on selections
    if selected_attribute != "Select Attribute":
        display_selected_information(selected_attribute, selected_sub_category)


    # ## CHART PLAN 2024
    
    ra_likert_var_list = ['Equity_Inclusivity_mean',
                          'Preparedness_and_planning_mean',
                          'Learning_mean',
                          'Agency_mean',
                          'Social_Collaboration_mean',
                          'Flexibility_mean',
                          'Assets_mean']


    # Resilience Attributes
    #Sample size RA
    df2_sz = df_2023_plan[ra_likert_var_list].dropna()
    sz = str(df2_sz.count().values[0])

    #dataframe to workwith (All data from the selection).
    df2 = df_2023_plan
    df2= df2[df2[ra_likert_var_list].notna()] #cleaning na

    Equity_y_Inclusivity        = df2['Equity_Inclusivity_mean'].mean()
    Preparedness_and_planning   = df2['Preparedness_and_planning_mean'].mean() 
    Learning                    = df2['Learning_mean'].mean()
    Agency                      = df2['Agency_mean'].mean()
    Social_Collaboration        = df2['Social_Collaboration_mean'].mean()
    Flexibility                 = df2['Flexibility_mean'].mean()
    Assets                      = df2['Assets_mean'].mean()

    s_df2 = pd.DataFrame(dict(
        r=[Equity_y_Inclusivity,Preparedness_and_planning,Learning,Agency,Social_Collaboration,Flexibility,Assets],
        theta=['Equity and Inclusivity','Preparedness and planning',
                            'Learning','Agency','Social Collaboration','Flexibility','Assets']))
    s_fig_ra_general = px.line_polar(s_df2, r='r', theta='theta', line_close=True, title="Resilient Attributes in Partners' Plans (2024)")
    s_fig_ra_general.update_traces(line_color='#FF37D5', line_width=1)
    s_fig_ra_general.update_traces(fill='toself')
    s_fig_ra_general.update_layout(
        polar=dict(
            radialaxis=dict(
                tickfont=dict(color='#112E4D'),
                range=[0, 4],
                ),
            angularaxis=dict(
                tickfont=dict(size=16, color='black')
            )
        )
    )
        # s_fig_ra_general.add_annotation(x=1, y=0,
        #             text='Out of '+ sz +' Plans',showarrow=False,
        #             yshift=-60)
        
    chart_ra_plan_current_year = s_fig_ra_general
    # st.write(chart_ra_plan_current_year)
        
    
    ## DATA 2023-2024
        # Create a dictionary with the data
    data_ra_23 = {
        'RA': [
            'Equity and Inclusivity', 
            'Preparedness and planning', 
            'Learning', 
            'Agency', 
            'Social Collaboration', 
            'Flexibility', 
            'Assets'
        ],
        'Score 2023': [
            2.5625, 
            2.645833333, 
            2.4375, 
            2.291666667, 
            2.125, 
            1.9375, 
            2.35
        ]
    }

    # Convert the dictionary to a pandas DataFrame
    data_ra_23 = pd.DataFrame(data_ra_23)

    data_ra_24 = s_df2
    data_ra_24 = data_ra_24.rename(columns={'theta': 'RA', 'r': 'Score 2024'})
    
    data_ra_23_24 = pd.merge(data_ra_23, data_ra_24, on='RA', how='inner')

        # Calculate means for both series
    series1 = data_ra_23_24['Score 2023']  
    series2 = data_ra_23_24['Score 2024']  

    # Create a dataframe with both series and 'RA' as theta
    polar_data = pd.DataFrame(dict(
        r1=series1,
        r2=series2,
        theta=data_ra_23_24['RA']  # Using 'RA' as the theta column
    ))

    # Create the polar line chart for Series 2023 and 2024
    fig_polar = go.Figure()

    # Add trace for Series 2023 with a lighter shade of blue
    fig_polar.add_trace(go.Scatterpolar(
        r=polar_data['r1'],
        theta=polar_data['theta'],
        mode='lines',
        name='Score 2023',
        line=dict(color='rgba(17, 46, 77, 0.5)', width=1),  # Lighter shade of blue for 2023
        fill='toself'
    ))

    # Add trace for Series 2024 with the darker blue color
    fig_polar.add_trace(go.Scatterpolar(
        r=polar_data['r2'],
        theta=polar_data['theta'],
        mode='lines',
        name='Score 2024',
        line=dict(color='#FF37D5', width=1),  
        fill='toself'
    ))

    # Customize layout
    fig_polar.update_layout(
        title="Resilient Attributes in Partners' Plans (2023-2024)",
        polar=dict(
            radialaxis=dict(
                tickfont=dict(color='#112E4D'),
                range=[0, 4],  # Adjust this range according to your data
            ),
            angularaxis=dict(
                tickfont=dict(size=16, color='black')
            )
        ),
        showlegend=True  # Ensure the legend is visible
    )
    
    #chart all years
    


    #Ranking

    #making a list of the three most important ra
    s_df2 = s_df2.sort_values(by=['r'],ascending=False)
    s_df2_best3 = s_df2.head(3)
    list_best3 = s_df2_best3.theta.unique()
    list_best3 =  ', '.join(list_best3)
    #making a function to change the last comma with "&"
    def replace_last(string, delimiter, replacement):
        start, _, end = string.rpartition(delimiter)
        return start + replacement + end
    #getting a string with the first three ra.
    list_best3 = replace_last(list_best3, ',', ' & ')
    #making a list of the three last important ra.
    s_df2_last3 = s_df2.tail(3)
    s_df2_last3 = s_df2_last3.sort_values(by=['r'])
    list_last3 = s_df2_last3.theta.unique()
    list_last3 =  ', '.join(list_last3)
    list_last3 = replace_last(list_last3, ',', ' & ')

    st.markdown("#### Resilience Attributes")
    
    tab1, tab2 = st.tabs(['2024-2023 Comparation', '2024 Details'])
    
    with tab1: 
        st.write(fig_polar)
        st.markdown("**Note:** "+list_best3 + " are top RtR Global Campaign Resilience Attributes. "+list_last3 + " represent Resilience Attributes for enhancement.")
    
    with tab2: 
        st.write(chart_ra_plan_current_year)
        st.markdown("**Note:** "+list_best3 + " are top RtR Global Campaign Resilience Attributes. "+list_last3 + " represent Resilience Attributes for enhancement.")
    

   
    #____
    ##SUB CATEGORIES - RESILIENCE ATTRIBUTES CHART
    #_____
    sub_ra_likert_var_list = ['Preparedness','Planning','Experiential_learning','Educational_learning','Autonomy','Leadership',
    'Decision_making','Collective_participation','Connectivity','Coordination','Diversity','Redundancy','Distributive_Equity','Equity_of_Access',
    'Finance','Infrastructure','Natural_resources','Technologies','Basic_services',]

    #Sample size SUB RA
    df2_sz = df_2023_plan[sub_ra_likert_var_list].dropna()
    sz = str(df2_sz.count().values[0])

    #dataframe to workwith (All data from the selection).
    df2 = df_2023_plan  ## AVOID DUPLICATING THE DATA SET
    df2= df2[df2[sub_ra_likert_var_list].notna()] #cleaning na


    Distributive_Equity= df2['Distributive_Equity'].mean() 
    Equity_of_Access = df2['Equity_of_Access'].mean() 
    Preparedness = df2['Preparedness'].mean() 
    Planning = df2['Planning'].mean() 
    Experiential_learning = df2['Experiential_learning'].mean() 
    Educational_learning = df2['Educational_learning'].mean() 
    Autonomy = df2['Autonomy'].mean() 
    Leadership = df2['Leadership'].mean() 
    Decision_making = df2['Decision_making'].mean() 
    Collective_participation = df2['Collective_participation'].mean() 
    Connectivity = df2['Connectivity'].mean() 
    Coordination = df2['Coordination'].mean() 
    Diversity = df2['Diversity'].mean() 
    Redundancy = df2['Redundancy'].mean() 
    Finance = df2['Finance'].mean() 
    Natural_resources = df2['Natural_resources'].mean() 
    Technologies = df2['Technologies'].mean() 
    Infrastructure = df2['Infrastructure'].mean() 
    Basic_services= df2['Basic_services'].mean() 


    s_df2 = pd.DataFrame(dict(
        r=[Distributive_Equity,Equity_of_Access,Preparedness,Planning,Experiential_learning,Educational_learning,Autonomy,
    Leadership,Decision_making,Collective_participation,Connectivity,Coordination,
    Diversity,Redundancy,Finance,Natural_resources,Technologies,Infrastructure,Basic_services],
        theta=['Distributive Equity','Equity of Access',	'Preparedness',
                                'Planning',	'Experiential Learning','Educational Learning',
                                'Autonomy',	'Leadership',	'Decision Making',	'Collective Participation',
                                'Connectivity',	'Coordination',	'Diversity',	'Redundancy',	'Finance',
                                'Natural Resources',	'Technologies',	'Infrastructure',	'Basic Services']))
    s_fig_sub_ra_general = px.line_polar(s_df2, r='r', theta='theta', line_close=True, title="Resilient Attributes Subcategories in Partners' Plans (2024)")
    # s_fig_sub_ra_general = px.line_polar(s_df2, r='r', theta='theta', line_close=True,)
    s_fig_sub_ra_general.update_traces(line_color='#FF37D5', line_width=1)
    s_fig_sub_ra_general.update_traces(fill='toself')
    s_fig_sub_ra_general.update_layout(
        polar=dict(
            radialaxis=dict(
                tickfont=dict(color='#112E4D'),
                range=[0, 4],
                ),
            angularaxis=dict(
                tickfont=dict(size=15, color='black')
            )
        )
    )

    # s_fig_sub_ra_general.add_annotation(x=1, y=0,
    #             text='Out of '+ sz +' Plans',showarrow=False,
    #             yshift=-60)
    # st.write(s_fig_sub_ra_general)

    #making a list of the three most important ra-subattribute
    s_df2 = s_df2.sort_values(by=['r'],ascending=False)
    s_df2_best3 = s_df2.head(3)
    list_best3 = s_df2_best3.theta.unique()
    list_best3 =  ', '.join(list_best3)
    #making a function to change the last comma with "&"
    def replace_last(string, delimiter, replacement):
        start, _, end = string.rpartition(delimiter)
        return start + replacement + end
    #getting a string with the first three ra-subattribute
    list_best3 = replace_last(list_best3, ',', ' & ')
    #making a list of the three last important ra-subattribute
    s_df2_last3 = s_df2.tail(3)
    s_df2_last3 = s_df2_last3.sort_values(by=['r'])
    list_last3 = s_df2_last3.theta.unique()
    list_last3 =  ', '.join(list_last3)
    list_last3 = replace_last(list_last3, ',', ' & ')

    st.write(s_fig_sub_ra_general)
    st.markdown("**Note:** "+list_best3 + " are top Resilience Attributes Sub Categories. "+list_last3 +" represent Resilience Attributes Sub Categoriess for enhancement in Partners' Plans.")
   

    list_variales_plan = [
            "InitName",
            "Org_Type",
            "plan_name",
            "plan_description",
            "Equity_Inclusivity_mean",
            "Social_Collaboration_mean",
            "Preparedness_and_planning_mean",
            "Learning_mean",
            "Agency_mean",
            "Flexibility_mean",
            "Assets_mean",
            "sub_ra_central_targeted_concat",
            "sub_ra_central_targeted_counts",
            "sub_ra_targeted_but_not_central_concat",
            "sub_ra_targeted_but_not_central_counts",
            "Tangible_ra_narrative",
            "Inclusive_ra_narrative",
            "Sustainable_ra_narrative",
            
            ]
    
    df_ra_plans = df_2023_plan[list_variales_plan]
    
    # df_action_types_plans = df_action_types_plans[df_action_types_plans["action_clusters_plan_concat"].str.contains(selected_action, na=False)]

    st.write("##### Partners Plans: RA Details")
    st.caption("Figure under development")
    st.write(df_ra_plans)

    # __________________________________________________________________________________________________________________________________________________________________
    # __________________________________________________________________________________________________________________________________________________________________
    # __________________________________________________________________________________________________________________________________________________________________
    # __________________________________________________________________________________________________________________________________________________________________
    # __________________________________________________________________________________________________________________________________________________________________
    # __________________________________________________________________________________________________________________________________________________________________
    # # END BLOCK RA CONSOLIDADO
    # __________________________________________________________________________________________________________________________________________________________________
    # __________________________________________________________________________________________________________________________________________________________________
    # __________________________________________________________________________________________________________________________________________________________________
    # __________________________________________________________________________________________________________________________________________________________________
    # __________________________________________________________________________________________________________________________________________________________________


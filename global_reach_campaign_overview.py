
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


def global_outreach_campaign_overview(df_pledge_unique_countries,n_countries_plan_consolidated,n_partners_reporting_countries,n_partners_reporting_countries_plan,political_countries_url,df2_all_countries):

    st.write("### GLOBAL OUTREACH")
    st.markdown("Showcasing the global footprint of RTR partners, with information on the number of countries where actions are being taken, as per their pledges and plans.")

    # num_countries_pledge = df_pledge_unique_countries.shape[0]  # The total goal
    # num_countries_plan = n_countries_plan_consolidated  # The current number

    # # Calculate the percentages relative to the total goal
    # total_percentage = 100  # The goal is 100%
    # current_percentage = (num_countries_plan / num_countries_pledge) * 100

    # # Create a gauge chart
    # fig = go.Figure(go.Indicator(
    #     mode="gauge+number",
    #     value=current_percentage,
    #     domain={'x': [0, 1], 'y': [0, 1]},
    #     gauge={
    #         'axis': {'range': [0, 100], 'tickcolor': "#112E4D"},
    #         'bar': {'color': "#FF37D5"},
    #         'bgcolor': "white",
    #         'borderwidth': 2,
    #         'bordercolor': "#112E4D",
    #         'steps': [
    #             {'range': [0, current_percentage], 'color': "#FF37D5"},
    #             {'range': [current_percentage, 100], 'color': "#112E4D"},
    #         ],
    #     }
    # ))

    # # Update the layout to add titles and colors
    # fig.update_layout(
    #     paper_bgcolor = "white",
    #     font = {'color': "#112E4D", 'family': "Arial"},
    # )

    # fig.update_layout(autosize=True, width=300, height=250) 

    # fig.update_layout(
    #     title={
    #         'text': "% Coverage Countries (Pledge - Plan)", 
    #         'y':0.9,
    #         'x':0.5,
    #         'xanchor': 'center',
    #         'yanchor': 'top'},
    #     title_font=dict(
    #         family="Montserrat",
    #         size=12,  # Adjust the size as needed
    #         color="black"
    #     )
    # )


    # st.markdown("##### NUMBER OF OPERATIONAL COUNTRIES BY RTR PARTNERS")

    ## NUMBER OF OPERATIONAL COUNTRIES BY RTR PARTNERS")
    # Creating columns within a container with equal width
    metrics_container = st.container()
    with metrics_container:
        col1, col2 = st.columns(2)  # This will create two columns of equal width

        with col1:
            col1.metric("Countries (Pledges 2023)*", df_pledge_unique_countries.shape[0],
                        f"Out of {n_partners_reporting_countries} partners")
        
        with col2:
            col2.metric("Countries (Plan 2023)", n_countries_plan_consolidated,
                        f"Out of {n_partners_reporting_countries_plan} partners")
            
    # Render the plot in Streamlit
    # st.plotly_chart(fig)
    # st.caption("*Differences in the number of countries arise because initiatives that are no longer partners are not counted. Additionally, during the 2023 reporting process, Partner Initiatives may have indicated fewer countries due to enhancements in their metrics systems over the past year.")




    ####______________________________________________________________________________________
    ####______________________________________________________________________________________
    ####______________________________________________________________________________________
    #### Mapping RtR Partners' Global Reach  # ALL DATA
    ####______________________________________________________________________________________
    ####______________________________________________________________________________________

    # <b>Country:</b> {row['Country']}<br>
    # <b>Country:</b> {row['ND_GAIN Index Country']}<br>
    # <b>Country:</b> {row['Total Population (2022)']}<br>
    # <b>Country:</b> {row['Ind_Pledge']}<br>
    # <b>Country:</b> {row['Ind_Plan']}<br>
    # <b>Country:</b> {row['Total Partners_Counts']}<br>
    # <b>Country:</b> {row['Partners_Pledge']}<br>
    # <b>Country:</b> {row['Partners_Pledge_Count']}<br>
    # <b>Country:</b> {row['Partners_Plans']}<br>
    # <b>Country:</b> {row['Partners_Plans_Count']}<br>

    # tooltip=f"<b>Country:</b> {row['Country']}<br>
    # <b>Total Population</b> {row['Total Population (2022)']}<br>
    # <b>Vulnerability Index (Notre Dame):</b> {row['ND_GAIN Index Country']}<br>
    # <b>N° Partners reporting a pledge</b> {row['Partners_Pledge_Count']}<br>
    # <b>N° Partners reporting a plan</b> {row['Partners_Plans_Count']}<br>
    # <b>Individuals Pledged</b> {row['Ind_Pledge']}<br>
    # <b>Individuals Plan</b> {row['Ind_Plan']}<br>
    # <b>% Total Population Pledged</b> {row['%TP Pledge']}<br>
    # <b>% Total Population Plan</b> {row['%TP Plan']}<br>
    # <b>dif</b> {row['dif']}<br>
    # <b>Total Partners</b> {row['Total Partners_Counts']}<br>
    # <b>Partners Name</b> {row['Total Partners']}",
    
    st.write(df2_all_countries.columns)


    world_map_full = folium.Map(location=(0, 0), zoom_start=1, tiles="cartodb positron") 

    for index, row in df2_all_countries.iterrows():
        lat = row["lat"]
        lon = row["lon"]
        if not pd.isna(lat) and not pd.isna(lon):  # skip rows with non-numerical lat/lon values
            folium.Marker(
                location=[lat, lon],
                popup=row['country_to_plot'],
                tooltip=f"<b>Country:</b> {row['Country']}<br><b>Total Population</b> {numerize(row['Total Population (2022)'])}<br><b>Vulnerability Index (Notre Dame):</b> {row['ND_GAIN Index Country']}<br><b>N° Partners reporting a pledge</b> {numerize(row['Partners_Pledge_Count'])}<br><b>N° Partners reporting plan(s)</b> {numerize(row['Partners_Plans_Count'])}<br><b>Individuals Pledged</b> {numerize(row['Ind_Pledge'])}<br><b>Individuals Plan</b> {numerize(row['Ind_Plan'])}<br><b>Total Population Pledged</b> {numerize(row['%TP Pledge'])}%<br><b>Total Population Plan</b> {numerize(row['%TP Plan'])}%<br><b>dif</b> {numerize(row['dif'])}%<br><b>Total Partners</b> {numerize(row['Total Partners_Counts'])}<br><b>Partners Name</b> {row['Total Partners']}",
            ).add_to(world_map_full)

    folium.Choropleth(
        geo_data=political_countries_url,
        data=df2_all_countries,
        columns=["country_to_plot",'Total Partners_Counts'],
        key_on="feature.properties.name",
        fill_color="RdPu",
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name="Number of Partners per Country",
        highlight=True,
        name="Number of Partners per Country",

    ).add_to(world_map_full)
    folium.LayerControl().add_to(world_map_full)

    st_folium(world_map_full,width=725, key="map1", returned_objects=[])
    # st.text('Out of '+ sz +' RtR Partners (Source: RtR Pledge Statement Survey 2023)')









    # ####______________________________________________________________________________________
    # ####______________________________________________________________________________________
    # ####______________________________________________________________________________________
    # #### Mapping RtR Partners' Global Reach  # only pledge (all data). It should work after updating all survyes
    # ####______________________________________________________________________________________
    # ####______________________________________________________________________________________
    # ####______________________________________________________________________________________

    # ## PART 2) PLEDGES DISTRIBUTION
    # tab1, tab2 = st.tabs(["World Map" ,"Tree Map" ])
    # #___________________________________________
    # # WORLD MAP    #https://github.com/jefftune/pycountry-convert/tree/master/pycountry_convert
    # ##https://realpython.com/python-folium-web-maps-from-data/
    # #___________________________________________

    # # _________________________________________
    # # FINAL GEO DATA FRAME
    # # _________________________________________

    # # new_order = ['Country','adm0_a3','N Pledges','% Pledges','N Parters per country','Partners per country','continent',
    # # '% Continent','region_wb','% Region','subregion','% Sub Region','country_to_plot','Frecuency','% country',
    # # 'Total population in millions','ND_GAIN Index Country','lat','lon','ND_GAIN Index Country','']

    # # df2 = df2.reindex(columns=new_order)


    # # df2.columns
    # # df2[['Country','country_to_plot','lat']]



    # df2_all_countries



    # world_map_full = folium.Map(location=(0, 0), zoom_start=1, tiles="cartodb positron") 

    # for index, row in df2.iterrows():
    #     lat = row["lat"]
    #     lon = row["lon"]
    #     if not pd.isna(lat) and not pd.isna(lon):  # skip rows with non-numerical lat/lon values
    #         folium.Marker(
    #             location=[lat, lon],
    #             popup=row['country_to_plot'],
    #             tooltip=f"<b>Country:</b> {row['Country']}<br><b>Vulnerability Index (Notre Dame):</b> {row['ND_GAIN Index Country']}<br><b>Number of Partners</b> {row['Total Partners_Counts']}<br><b>Names of Partners:</b> {row['Total Partners']}",
    #             # tooltip=f"<b>Country:</b> {row['Country']}<br><b>Pledges (All Beneficiaries):</b> {row['N Pledges']}<br><b>Number of Partners</b> {row['N Parters per country']}<br><b>Names of Partners:</b> {row['Partners per country']}"
    #         ).add_to(world_map_full)

    # folium.Choropleth(
    #     geo_data=political_countries_url,
    #     data=df2,
    #     columns=["country_to_plot", "N Pledges"],
    #     key_on="feature.properties.name",
    #     fill_color="RdPu",
    #     fill_opacity=0.7,
    #     line_opacity=0.2,
    #     legend_name="Partners' Pledges per Country",
    #     highlight=True,
    #     name="Frequency of pledges by country.",

    # ).add_to(world_map_full)
    # folium.LayerControl().add_to(world_map_full)


    # with tab1:
    #     st_folium(world_map_full,width=725, key="map1", returned_objects=[])
    #     # st.text('Out of '+ sz +' RtR Partners (Source: RtR Pledge Statement Survey 2023)')
    #     with st.expander("Navigating this worldmap: A User's Guide"):
    #         st.write("""
    # The world map displays the consolidated pledges dedicated to all beneficiaries: Individuals, Companies, Regions, Cities, and Natural Systems, as outlined in the RtR Pledge Statements. A unique RtR Partner can produce a single pledge statement, catering to one or multiple beneficiary categories. Thus, if a partner commits to all categories, the total pledge count represented here would tally to 5 — one for each beneficiary.

    # **To use the map:**

    # - Zoom in and out: Use the plus (+) and minus (-) buttons in the top left corner of the map, or scroll up and down on your mouse.

    # - Move the map: Click and drag on the map to move it in any direction.

    # - View country information: Click on any marker on the map to view a popup with information about that country, such as the country name, number of pledges, number of partners per country, and partners per country.

    # - View number of pledges: The countries are color-coded based on the number of pledges in each country. To view the legend, click on the button on the top right corner of the map that looks like layers stacked on top of each other.

    # - The grey color indicates that no information is yet available on a country.

    # """)
        
    #     st.markdown(
    #     """
    #     The countries topping the list with the highest number of pledged actions by RtR Partners, representing the uppermost 5%, include: """ + list_best_5_per + """.

    #     By continental distribution, the predominance of pledged actions by RtR Partners is noted in """ + list_best3_conti + """. Conversely, """ + list_less_2_conti + """ witness a reduced volume of pledges.
        
    #     From a regional perspective, """ + list_best3_region + """ emerge as leaders in the frequency of RtR Partners' pledges. Conversely, """ + list_less_2_region + """ exhibit a lower pledge activity by these partners.
        
    #     Zooming into subregional details, """ + list_best3_subregion + """ are the focal points for pledges by RtR Partners. In contrast, """ + list_less_2_subregion + """ experience fewer pledge commitments.
    #     """)


    # #___________________________________________
    # # TREEMAP CONTINENTS
    # #___________________________________________

    # df2.rename(columns={'continent': 'Continents'}, inplace=True)
    # df2.rename(columns={'% Continent': 'Relative presence by continent (%)'}, inplace=True)

    # fig_treemap = px.treemap(df2, path=[px.Constant("World"),'Continents','region_wb','subregion','adm0_a3'], values = '% Pledges', color='Relative presence by continent (%)', color_continuous_scale='RdPu')
    # fig_treemap.update_traces(root_color="#FF37D5")
    # fig_treemap.update_layout(title_text='Treemap - Resilience Action Pledges by Continent, Region, Sub Region and Country')
    # fig_treemap.update_layout(margin = dict(t=50, l=25, r=25, b=25), width=1000)
    # fig_treemap.add_annotation(x=1, y=0,
    #                 text='Out of '+ sz +' RtR Partners (Source: RtR Pledge Statement Survey).',showarrow=False,
    #                 yshift=-20)
    # fig_treemap.data[0].hovertemplate = '%{value:.1f}%'
    # fig_treemap.update_traces(marker_line_color='grey')

    # with tab2:
    #     st.plotly_chart(fig_treemap)
    #     with st.expander("Navigating this treemap: A User's Guide"):
    #         st.write("""
    #     The treemap provides a visual representation of the consolidated pledges dedicated to all primary beneficiaries: Individuals, Companies, Regions, Cities, and Natural Systems. These pledges are captured in the RtR Pledge Statements. Within the treemap, each rectangle corresponds to a specific geographical area, with the size denoting the percentage of associated pledges. Additionally, the color variations may represent different metrics or categories.

    #     Each RtR Partner can issue a single pledge statement, which may cater to one or several primary beneficiaries. For instance, if a partner commits to all of these beneficiaries, their contributions within the treemap would be represented as five distinct pledges — one for each beneficiary. It's from this distribution that the percentage of all pledges is calculated.

    #     At the highest level of the treemap, there is a rectangle representing the entire world, labeled as "World."
        
    #     This treemap *support interactivity* by allowing users to click on a rectangle and zoom in to see nested categories. For example, if you click on a rectangle representing a continent, you might see rectangles representing regions within that continent. By clicking on a rectangle representing a region, you might see rectangles representing subregions within that country.

    #     This interactivity makes it easier for users to explore and understand hierarchical relationships within the data. It allows users to zoom in and out of the treemap and view the data from different perspectives. Additionally, users can hover over each rectangle to see more detailed information about the category and its associated data value.
    # """)
        
    #     st.markdown(
    #     """
    #     On a continental scale, the predominance of pledged actions by RtR Partners is denoted by the larger rectangles for """ + list_best3_conti + """. In contrast, the smaller rectangles for """ + list_less_2_conti + """ signify a decreased volume of pledges.

    #     Examining the regions, those with substantial pledge activities by RtR Partners are represented by more expansive rectangles, namely """ + list_best3_region + """. Conversely, """ + list_less_2_region + """ are depicted by smaller rectangles, indicating lesser pledge activities.

    #     Delving into the subregional specifics, the treemap emphasizes """ + list_best3_subregion + """ with larger rectangles, signifying increased pledge commitments by RtR Partners. On the opposite spectrum, the more modest rectangles for """ + list_less_2_subregion + """ denote fewer pledge commitments.

    #     Nested within the subregional rectangles are the associated countries. Notably, the countries that emerge prominently, showcased by the largest rectangles and denoting the highest pledge counts by RtR Partners, include: """ + list_best_5_per + """.
    #     """
    # )


    # list_columns_to_show = ['Country',
    # 'adm0_a3',
    # 'N Pledges',
    # '% Pledges',
    # 'N Parters per country',
    # 'Partners per country',
    # 'Continents',
    # 'Relative presence by continent (%)',
    # 'region_wb',
    # '% Region',
    # 'subregion',
    # '% Sub Region',
    # ]

    # long_description = f"""
    # The adaptation solutions pledged by partners and members are located in {df_pledge_unique_countries.shape[0]} countries on every continent, across {Cities2023Num_pledge_adj} cities and {Regs2023Nums_pledge_adj} regions. In Partners’ plans, the {percentaje_countries_pledge_vs_plan}% of those countries are considered, gap that will be reduced as Partners increase the number of their plans in the future. 
    # """

    # with st.expander("Explore Summary and Geografical Data"): 
    #     # st.write("Table under construcct")
    #     st.markdown(long_description)
    #     st.write(df2[list_columns_to_show])
        





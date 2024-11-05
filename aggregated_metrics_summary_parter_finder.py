
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns
from streamlit_folium import st_folium
from wordcloud import WordCloud, STOPWORDS
import folium
from PIL import Image
from numerize.numerize import numerize

def aggregated_metrics_partner_finder(df_to_find_partner,df_pledge_summary,df_pledge,df_m_countries_vertical,df_partner_campaign,df_2022_2023_plan_consolidated_by_partner):
    tile_partner_metrics =f"""#### AGGREGATED METRICS"""
    st.markdown(tile_partner_metrics)
    try:
        n_countries_plan = df_m_countries_vertical[df_m_countries_vertical['source'].isin(['Plans (All Plans, in case there is more than one)'])]
        n_countries_plan = len(n_countries_plan['All_Countries'].unique())
        n_plans = df_partner_campaign['N_Plans'].iloc[0]
        p_short_name = df_partner_campaign['short_name'].iloc[0]
        n_countries_pledge = df_m_countries_vertical[df_m_countries_vertical['source'].isin(['Pledge (All Beneficiaries)'])]
        n_countries_pledge = len(n_countries_pledge['All_Countries'].unique())
        
        #PLEDGE
        tile_partner_pledge =f"""##### PLEDGE STATEMENT"""
        st.markdown(tile_partner_pledge)

        list_pledge_to_analisis = ['Comps2023Num','Regs2023Nums','Cities2023Num','NumHectNatSys2023','DirIndiv2023Num','CompsNumIndiv','NumIndivRegs','NumIndivCities','NumIndivNatSys',]

        Comps2023Num_pledge = df_pledge_summary['Comps2023Num'].iloc[0]
        Regs2023Nums_pledge = df_pledge_summary['Regs2023Nums'].iloc[0]
        Cities2023Num_pledge = df_pledge_summary['Cities2023Num'].iloc[0]
        NumHectNatSys2023_pledge = df_pledge_summary['NumHectNatSys2023'].iloc[0]

        DirIndiv2023Num_pledge = df_pledge_summary['DirIndiv2023Num'].iloc[0]
        CompsNumIndiv_pledge = df_pledge_summary['CompsNumIndiv'].iloc[0]
        NumIndivRegs_pledge = df_pledge_summary['NumIndivRegs'].iloc[0]
        NumIndivCities_pledge = df_pledge_summary['NumIndivCities'].iloc[0]
        NumIndivNatSys_pledge = df_pledge_summary['NumIndivNatSys'].iloc[0]
        n_indiv_total_pledge = np.nansum([DirIndiv2023Num_pledge,CompsNumIndiv_pledge,NumIndivRegs_pledge,NumIndivCities_pledge,NumIndivNatSys_pledge])

        us_dollar_pledge = df_pledge['s3107'].iloc[0]

        col1, col2, col3, col4, col5,col6 = st.columns(6)
        try:
            col1.metric("Individuals",numerize(n_indiv_total_pledge))
        except Exception as e:
            col1.markdown("Individuals Total: No available yet")

        try:
            col2.metric("Companies:",numerize(Comps2023Num_pledge))
        except Exception as e:
            col2.metric("Companies:",0)
            pass

        try:
            col3.metric("Regions",numerize(Regs2023Nums_pledge))
        except Exception as e:
            col3.metric("Regions",0)
            pass

        try:
            col4.metric("Cities",numerize(Cities2023Num_pledge))
        except Exception as e:
            col4.metric("Cities",0)
            pass

        try:
            col5.metric("Natural Systems",numerize(NumHectNatSys2023_pledge))
        except Exception as e:
            col5.metric("Natural Systems",0)
            pass

        try:
            col6.metric("Countries",n_countries_pledge)
        except Exception as e:
            pass

        with st.expander("Explore More of Metrics about Individuals in "+p_short_name+" Pledge"):
            col1, col2, col3, col4,  = st.columns(4)
            col1.markdown("AGGREGATED METRICS")
            col1, col2, col3, col4,col5  = st.columns(5)
            
            try:
                col1.metric("Individuals Total Pledge:",numerize(n_indiv_total_pledge))
            except Exception as e:
                col1.metric("Individuals Total Pledge:",0)
                
            col1, col2, col3, col4,  = st.columns(4)
            col1.markdown("DISAGGREGATED METRICS")
            col1, col2, col3, col4,col5  = st.columns(5)
            try:
                col1.metric("Individuals (Direct):",numerize(DirIndiv2023Num_pledge))
            except Exception as e:
                col1.metric("Individuals (Direct):",0)
                pass

            try:
                col2.metric("Individuals (Companies):",numerize(CompsNumIndiv_pledge))
            except Exception as e:
                col2.metric("Individuals (Companies):",0)
                pass
                
            try:
                col3.metric("Individuals (Regions):",numerize(NumIndivRegs_pledge))
            except Exception as e:
                col3.metric("Individuals (Regions):",0)
                pass
                
            try:
                col4.metric("Individuals (Cities):",numerize(NumIndivCities_pledge))
            except Exception as e:
                col4.metric("Individuals (Cities):",0)
                pass
            
            try:
                col5.metric("Individuals (Natural Systems):",numerize(NumIndivNatSys_pledge))
            except Exception as e:
                col5.metric("Individuals (Natural Systems):",0)
                pass
    except Exception as e:
        st.markdown("No Pledge Statement Reported Yet")
        pass
    # END PLEDGE REPORTING INFORMATION        




    #PLANS REPORTING INFORMATION
    
    try:
        if n_plans == 0:
            pass
        else: 
            tile_partner_pledge =f"""##### RESILIENCE-BUILDING PLAN SUBMISSIONS"""
            st.markdown(tile_partner_pledge)  
    except Exception as e:
        pass
    
    
    try:
        replace_list = ['n_direc_indiv_plan', 'n_indiv_companies_plan', 'n_indiv_regions_plan', 'n_indiv_cities_plan', 'n_hecta_natsys_plan',
                    'US_Dollars_Mobilized_plan', 'n_companies_plan', 'n_regions_plan', 'n_cities_plan']

        # Replace 0 with NaN in the specified columns
        # df_2022_2023_plan_consolidated_by_partner[replace_list] = df_2022_2023_plan_consolidated_by_partner[replace_list].replace(0, np.nan)

        n_direc_indiv_plan = df_2022_2023_plan_consolidated_by_partner['n_direc_indiv_plan'].iloc[0]
        n_indiv_companies_plan = df_2022_2023_plan_consolidated_by_partner['n_indiv_companies_plan'].iloc[0]
        n_indiv_regions_plan = df_2022_2023_plan_consolidated_by_partner['n_indiv_regions_plan'].iloc[0]
        n_indiv_cities_plan = df_2022_2023_plan_consolidated_by_partner['n_indiv_cities_plan'].iloc[0]
        n_hecta_natsys_plan = df_2022_2023_plan_consolidated_by_partner['n_hecta_natsys_plan'].iloc[0]
        US_Dollars_Mobilized_plan = df_2022_2023_plan_consolidated_by_partner['US_Dollars_Mobilized_plan'].iloc[0]
        n_companies_plan = df_2022_2023_plan_consolidated_by_partner['n_companies_plan'].iloc[0]
        n_regions_plan = df_2022_2023_plan_consolidated_by_partner['n_regions_plan'].iloc[0]
        n_cities_plan = df_2022_2023_plan_consolidated_by_partner['n_cities_plan'].iloc[0]
        n_indiv_total_plan = np.nansum([n_direc_indiv_plan, n_indiv_companies_plan, n_indiv_regions_plan, n_indiv_cities_plan])

        col1, col2, col3, col4, col5,col6 = st.columns(6)

        try:
            col1.metric("Individuals",numerize(n_indiv_total_plan))
        except Exception as e:
            col1.markdown("Individuals Total: No available yet")

        try:
            col2.metric("Companies:",numerize(n_companies_plan))
        except Exception as e:
            pass

        try:
            col3.metric("Regions",numerize(n_regions_plan))
        except Exception as e:
            pass

        try:
            col4.metric("Cities",numerize(n_cities_plan))
        except Exception as e:
            pass

        try:
            col5.metric("Natural Systems",numerize(n_hecta_natsys_plan))
        except Exception as e:
            pass

        try:
            col6.metric("Countries",n_countries_plan)
        except Exception as e:
            pass


        with st.expander("Explore More of Metrics about Individuals in Partners' Plans"):
            col1, col2, col3, col4,  = st.columns(4)

            col1.markdown("AGGREGATED METRICS")
            col1, col2, col3, col4,  = st.columns(4)
            try:
                col1.metric("N Plans", numerize(n_plans))
            except Exception as e:
                pass

            try:
                col2.metric("Individuals Total Plan:",numerize(n_indiv_total_plan))
            except Exception as e:
                col2.markdown("Individuals Total: No available yet")
                
            col1, col2, col3, col4,  = st.columns(4)
            col1.markdown("DISAGGREGATED METRICS")
            col1, col2, col3, col4,  = st.columns(4)
            try:
                col1.metric("Individuals (Direct):",numerize(n_direc_indiv_plan))
            except Exception as e:
                pass

            try:
                col2.metric("Individuals (Companies):",numerize(n_indiv_companies_plan))
            except Exception as e:
                pass
                
            try:
                col3.metric("Individuals (Regions):",numerize(n_indiv_regions_plan))
            except Exception as e:
                pass
                
            try:
                col4.metric("Individuals (Cities):",numerize(n_indiv_cities_plan))
            except Exception as e:
                pass
    except Exception as e:
        st.markdown("No Information About Plans Submitted Yet")
        pass
    #END PLAN REPORTING PROCESS


    #ADAPTATION FINANCE
    # us_dollar_pledge = df_pledge['s3107'].iloc[0]
    # US_Dollars_Mobilized_plan = df_2022_2023_plan_consolidated_by_partner['US_Dollars_Mobilized_plan'].iloc[0]
    try:
        if us_dollar_pledge + US_Dollars_Mobilized_plan != 0:
            col1, col2 = st.columns(2)
            col1.markdown("##### ADAPTATION FINANCE")
            col1, col2 = st.columns(2)
            try:
                col1.metric("US Dollars\nExpected (Pledge):", numerize(us_dollar_pledge))
            except Exception as e:
                col1.metric("US Dollars\nExpected (Pledge):", 0)
            try:
                col2.metric("US Dollars\nMobilizing (Plan):", numerize(US_Dollars_Mobilized_plan))
            except Exception as e:
                col2.metric("US Dollars\nMobilizing (Plan):", 0)
        else:
            st.markdown('"No Information About Adaptation Finance Reported Yet"')
    except Exception as e:
        st.markdown('No Information About Adaptation Finance Reported Yet')
    #END ADAPTATION FINANCE


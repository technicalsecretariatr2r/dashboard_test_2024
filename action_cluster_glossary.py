import streamlit as st
import fitz  # PyMuPDF
import os



def action_clusters_glossary():
    st.markdown("### RESILIENCE ACTION CLUSTERS")
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
    selected_action_type = st.selectbox('Select a Marrakech Partnership Action Type:', action_type_names)

    # Initialize an empty list for cluster names
    cluster_names = ["Select Cluster"]

    # Update cluster_names based on the selected action type
    if selected_action_type != "Select Action Type":
        cluster_names += list(action_clusters[selected_action_type].keys())

    # Create a selectbox for Clusters that updates based on the selected action type
    selected_cluster = st.selectbox('Select a RtR Action Cluster:', cluster_names)

    # Function to display the selected Action Type and Cluster
    def display_selected_action_type_and_cluster(action_type, cluster):
        st.markdown("**Marrakech Partnership for Global Climate Action - Action Type:**")
        st.markdown(f"{action_type}")
        st.markdown("### RtR Action Cluster:")
        if cluster != "Select Cluster":
            st.markdown(f"- **{cluster}:** {action_clusters[action_type][cluster]}")
        else:
            for cluster_action, description in action_clusters[action_type].items():
                st.markdown(f"- **{cluster_action}:** {description}")
        # st.markdown("---")  # Adds a horizontal line for better separation

    # Display based on selections
    if selected_action_type != "Select Action Type" and selected_cluster != "Select Cluster":
        display_selected_action_type_and_cluster(selected_action_type, selected_cluster)
    elif selected_action_type != "Select Action Type":
        # Display all clusters under the selected action type
        display_selected_action_type_and_cluster(selected_action_type, "Select Cluster")


    
    
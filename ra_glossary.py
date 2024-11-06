    
import streamlit as st
import fitz  # PyMuPDF
import os
    
def ra_glossary():
    st.markdown("### RESILIENCE ATTRIBUTES")
    # st.caption("An assessment of resilience attributes, evaluating how partners' actions are effectively enhancing individual resilience to climate change.")
    st.markdown("Resilience Attributes are critical qualities enabling systems to withstand, adapt, and recover from adverse conditions. The identification and definition of these attributes and corresponding sub-categories were the result of an exhaustive collaborative process involving a literature review and expert consultations including the Race to Resilience's Methodological Advisory Group and stakeholders from the Resilience Knowledge Coalition. They serve as a predictive measure of resilience, aiding in the design, supervision, and initial assessment of resilient action. In this sense, interventions that positively impact these attributes are seen to improve the capacity of climate-vulnerable beneficiaries to respond to and adapt to changes. Within the context of the RtR's Metrics Framework, Resilience Attributes constitute the depth metrics, representing the qualitative dimension of the index that measures the increased resilience resulting from our partner's efforts.")
    
    # Define the two-level nested dictionary for Resilience Attributes and their Sub-Categories
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
        
        # st.markdown("---")  # Adds a horizontal line for better separation

    # Display based on selections
    if selected_attribute != "Select Attribute":
        display_selected_information(selected_attribute, selected_sub_category)

    
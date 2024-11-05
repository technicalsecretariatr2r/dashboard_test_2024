import streamlit as st

def glossary_rtr():
    rtr_extended_info = {
        "RtR Campaign": """
            The Race to Resilience (RtR) Campaign is a pivotal global initiative spearheaded by High-Level Climate Action Champions, aimed at significantly enhancing the resilience of four billion people in vulnerable communities by 2030. It mobilizes a diverse array of non-state actors, including businesses, investors, cities, regions, and civil society, to implement practical and impactful actions for climate resilience. RtR serves as a governance system focused on climate resilience, coordinating efforts across various sectors and stakeholders to ensure a cohesive and strategic approach to resilience-building. This governance framework ensures that initiatives are inclusive, locally-led, and align with broader climate action strategies, fostering collaborations for a resilient and sustainable future.
        """,
        "Resilience": """
            Resilience is defined as the structural capacity of a complex adaptive system to maintain a certain level of functionality despite experiencing disturbances in its critical components. It encompasses the system's ability to absorb impacts, adapt, and recover from challenging or adverse events while maintaining its operational and structural integrity. Essentially, resilience is about the strength and flexibility of a system to confront and overcome difficulties.
        """,
        "Climate Resilience": """
            Climate resilience, as described by the Intergovernmental Panel on Climate Change (IPCC), refers to the capacity of social, economic, and environmental systems to cope with a hazardous event, trend, or disturbance related to climate. It involves understanding and managing not just the risks that climate variability and change pose, but also harnessing the potential opportunities for a sustainable future. This concept integrates the ability to anticipate, prepare for, respond to, and recover from climate-related disruptions in a way that preserves essential structures and functions and fosters sustainability.
        """,
        "Increased Climate Resilience": """
            Increased climate resilience denotes the augmented capacity of individuals, communities, or systems to adapt to and effectively manage climate-related hazards to which they are exposed and vulnerable. This concept emphasizes both immediate adaptive responses and long-term strategies to modify physical and socio-economic environments, reducing vulnerability and enhancing overall resilience to climate change. It embodies a proactive approach to understanding, preparing for, and mitigating the impacts of climate change, thereby contributing to a more resilient and sustainable future.
        """,
        "Reporting Tool": """
            The "Reporting Tool" in the Race to Resilience context is an essential tool for gathering and analyzing data on climate resilience initiatives by partners. Comprising surveys like the General Information Survey, Pledge Statement Survey, and Resilience-Building Plan, it facilitates the collection of vital information ranging from basic details to specific strategies and actions for fulfilling commitments. In addition to using Magnitude and Depth indices to assess the scope and impact of actions, it also incorporates a Confidence Index to ensure the robustness and reliability of the collected data. This structured and transparent design not only enables effective tracking and validation of resilience initiatives but also ensures the integrity and credibility of climate resilience efforts. It contributes to informed and adaptive management in the campaign, enhancing climate resilience.
        """,
        "Confidence Index": """
            In the context of the Race to Resilience (RtR) campaign, the Confidence Index plays a crucial role in ensuring the reliability and robustness of data collected through the Reporting Tool. This index assesses the quality of the data based on criteria such as the level of response to the Reporting Tool's surveys, consultation with members involved in the initiatives, and the conduct of risk or vulnerability assessments. Its purpose is to ensure that the information reported by partners is accurate and trustworthy, providing a solid foundation for analysis and decision-making within the campaign. Therefore, the Confidence Index is essential for validating the contributions of RtR partners, ensuring that reports and conclusions derived are grounded in solid and verifiable data, accurately reflecting the progress and impact of climate resilience actions.
        """,
        "Magnitude Metrics": """
            The Race to Resilience Campaign uses Magnitude Metrics as essential quantitative tools to measure the impact of resilience-building activities, focusing on the scale and reach across various groups like Companies, Regions, Cities, Natural Systems, and Individuals. The primary goal is to quantify how many people become more resilient due to the Campaign's actions, aligning with the ambitious target of making 4 billion people more resilient by 2030. These metrics, crucial for tracking progress towards enhancing individual resilience globally, also align with the Sharm-el-Sheikh Adaptation Agenda's systemic adaptation goals. They play a critical role in quantifying the Campaign's reach but are part of a broader set of tools needed to fully capture the complex and multifaceted nature of resilience, which includes qualitative improvements and systemic changes.
        """,
        "Depth Metrics": """
            The Depth Metrics in the Race to Resilience Campaign are a comprehensive tool for qualitatively measuring resilience-building efforts. Focusing on Resilience Attributes (RAs), which are key qualities enhancing the capacity of systems and communities against adverse conditions, these metrics assess substantial changes and long-term impacts of interventions on resilience. They involve a process of self-assessment and narratives from implementers, compared against the theoretical contributions of the Methodological Advisory Group, to ensure a balanced and integrated approach, guaranteeing that the built resilience is profound, sustainable, and aligned with the multifaceted nature of the challenges being addressed.
        """,
        "Resilience Attributes": """
            Resilience Attributes are critical qualities enabling systems to withstand, adapt, and recover from adverse conditions. The identification and definition of these attributes and corresponding sub-categories were the result of an exhaustive collaborative process involving a literature review and expert consultations including the Race to Resilience's Methodological Advisory Group and stakeholders from the Resilience Knowledge Coalition. They serve as a predictive measure of resilience, aiding in the design, supervision, and initial assessment of resilient action. In this sense, interventions that positively impact these attributes are seen to improve the capacity of climate-vulnerable beneficiaries to respond to and adapt to changes. Within the context of the RtR's Metrics Framework, Resilience Attributes constitute the depth metrics, representing the qualitative dimension of the index that measures the increased resilience resulting from our partner's efforts.
        """,
        "Resilience Action Clusters": """
            Resilience Action Clusters serve to identify and categorise actions focused on building climate resilience. These emerged from a collaboration between different actors, originating in the collection of resilience actions from the Marrakech Partnership (Global Climate Action, 2021), the consulting firm Carbon Disclosure Project (CDP, 2022), and the IPCC Action List (IPCC, 2021). These actions were classified into 29 categories, the “Resilience Action Clusters”, which were validated by the campaign's Methodology Advisory Group (MAG). Resilience actions clusters usually include a combination of adaptation and response measures, as well as capacity building and awareness raising actions. Partners are asked to specify which action clusters align with their actions on the first step of the reporting tool: The General Information Survey.
        """,
        "MEL Cycle": """
            Within the context of the Race to Resilience Metrics Framework, the Monitoring, Evaluation, and Learning (MEL) cycle plays a crucial role in transforming Depth and Magnitude metrics from static to dynamic measures. By integrating these metrics into the MEL cycle, continuous evaluation and adaptation of resilience strategies and actions are enabled. Constant monitoring provides up-to-date insights into progress and impacts, systematic evaluation offers reflections on the effectiveness and efficiency of interventions, and learning facilitates the adaptation and improvement based on feedback and outcomes. This methodology ensures that the metrics not only reflect a fixed point in time but evolve and adapt as initiatives progress and contexts change. This keeps resilience actions relevant, effective, and aligned with the goals of climate change adaptation and mitigation.
        """,
        "Hazards": """
            Hazards are the potential occurrence of a natural or human-induced physical event or trend that may cause loss of life, injury, or other health impacts, as well as damage and loss to property, infrastructure, livelihoods, service provision, ecosystems, and environmental resources. Hazards events are exacerbated by climate change and may cause adverse consequences for society and ecosystems.
        """,
        "Priority Groups": """
            Partners present targeted initiatives, emphasizing a commitment to combating climate challenges faced by priority groups and beneficiaries, particularly those most vulnerable. Priority groups reflect specific populations that have a higher level of vulnerability, exposure or need in the context of a particular initiative's action, acknowledging human rights, social equity, and well-being of future generations. This approach reflects a joint commitment to increase resilience to climate change through tailored interventions that prioritize those most susceptible to its impacts.
        """
    }
    # Dropdown for selecting a metric category
    st.markdown("### GLOSSARY OF KEY CONCEPTS")
    selected_metric = st.selectbox("**Select a Key Concept to Explore More:**", list(rtr_extended_info.keys()))
    # Display the description of the selected metric category
    st.markdown(f"#### {selected_metric}")
    st.markdown(rtr_extended_info[selected_metric])







"""### GI Overall Status Documentation

The `gi_overall_status` variable within the `df_gi` DataFrame synthesizes the outcomes of both the completeness and reliability assessments of the General Information (GI) Survey responses. It provides a comprehensive overview of each initiative's current status regarding the quality and reliability of the information they have submitted. This metric is pivotal for evaluating an initiative's engagement and operational transparency within the survey's framework.

#### Purpose

The `gi_overall_status` aims to give stakeholders a quick and integrated understanding of how well initiatives are performing in terms of providing complete and reliable information through the GI Survey. It combines insights from the GI Completeness Index (`gi_completeness_idx`) and the Reliability Members 2022-2023 Difference Status (`reliability_members_22_23_dif_status`) to offer a holistic view of each initiative's data quality.

#### Components

The `gi_overall_status` is derived from two key components:

1. **GI Completeness Status** - Reflects whether an initiative has provided sufficient information across all required sections of the GI Survey to be considered "Accepted" or is "Awaiting Completion" due to missing or incomplete data.

2. **Reliability Members 2022-2023 Difference Status** - Indicates the consistency and accuracy of reported membership data over two consecutive years, categorizing initiatives based on whether their membership has increased, decreased, remained unchanged, or if no members have been reported.

#### Calculation and Format

The overall status is formatted as a string that combines the outcomes of the completeness and reliability assessments. For example:

- "Completeness: Accepted & Reliability Accepted: Members Increased in 2023"
- "Completeness: Awaiting Completion & Reliability Need Review: Members Decreased in 2023"

This format provides a clear and immediate understanding of where an initiative stands regarding the GI Survey's data quality expectations.

#### Implementation

To determine the `gi_overall_status`, the following approach is used:

- Calculate the `gi_completeness_idx` and determine the `gi_completeness_status`.
- Assess the `reliability_members_22_23_dif_status` based on year-over-year membership data comparison.
- Combine these assessments into a single status string that reflects both completeness and reliability dimensions.

#### Impact on Initiatives

The `gi_overall_status` serves as a critical indicator for initiatives to gauge their performance in meeting the survey's reporting standards. It highlights areas of strength and opportunities for improvement, encouraging initiatives to strive for both thoroughness in their responses and accuracy in their data reporting. Initiatives are thus motivated to maintain high standards of data quality, enhancing their credibility and the overall effectiveness of their engagement with the survey.

#### Summary

The `gi_overall_status` is a vital metric that encapsulates the quality of information provided by initiatives in the GI Survey, covering both completeness and reliability aspects. It helps stakeholders quickly assess the level of engagement and data integrity of each initiative, facilitating informed decisions and actions to support continuous improvement in reporting and operational transparency.
"""

"""### GI Completeness Index Documentation

The `gi_completeness_idx` within the `df_gi` DataFrame represents the overall percentage of completeness of the General Information (GI) Survey responses. It is a comprehensive metric that quantifies the extent to which the initiatives have provided necessary information across various critical sections of the survey. This index is calculated as a weighted sum of several sub-indices, each corresponding to different sections of the GI Survey. The formula for this index incorporates the importance of each section through assigned weights, reflecting their relative significance in assessing the initiative's completeness.

#### Sub-Indices and Their Weights

1. **Partner Information GI Sub-Index** (`partner_info_gi_subidx` - Weight: 8.33%)
   - Evaluates the completeness of information regarding the initiative's partners, including descriptions, locations, priority groups, and regions.

2. **Members Information GI Sub-Index** (`members_info_gi_subdix` - Weight: 25%)
   - Assesses detailed information about the members involved with the initiative, including confirmation of membership, types of members, general member information, reported member numbers, and member data uploads.

3. **Metrics GI Sub-Index** (`metrics_gi_subidx` - Weight: 8.33%)
   - Measures the submission and consistency of metrics strategies, data validation, and tracking information.

4. **Sharm-El-Sheikh Adaptation Agenda (SAA) GI Sub-Index** (`saa_gi_subidx` - Weight: 25%)
   - Evaluates the initiative's alignment with and reporting on the Sharm-El-Sheikh Adaptation Agenda through various systems and cross-cutting enablers.

5. **Action Clusters GI Sub-Index** (`action_clusters_gi_subdix` - Weight: 25%)
   - Assesses the initiative's identification and elaboration on resilience actions categorized into Action Clusters.

6. **Type of Impact GI Sub-Index** (`type_impact_gi_subdix` - Weight: 8.33%)
   - Focuses on the initiative's aim for a clear and measurable impact on different beneficiaries.

#### Calculation Methodology

The `gi_completeness_idx` is calculated by taking the sum of these weighted sub-indices. Each sub-index contributes to the overall completeness index based on its assigned weight. This method ensures a nuanced evaluation that highlights the importance of thorough and detailed survey responses across all sections.

#### Completeness Status and Requirements

- **Completeness Status** (`gi_completeness_status`): Indicates whether the GI Survey is considered "Accepted" (if the `gi_completeness_idx` is greater than 90%) or "Awaiting Completion" (if the index is 90% or below).
- **Completeness Requirements Priority** (`gi_completeness_req_priority`): Lists the specific areas requiring attention or completion, prioritized based on their impact on the overall completeness index. This helps initiatives identify and focus on sections that need further information or improvement.

#### Implementation

The calculation and evaluation are implemented programmatically within the data processing pipeline. After computing the `gi_completeness_idx`, the DataFrame `df_gi` is updated with the completeness index, status, and prioritized requirements for each initiative. This comprehensive approach aids in assessing the quality and completeness of the information provided by initiatives, facilitating effective monitoring and management.
"""

"""### Reliability GI Members Overall Index Documentation

The `reliability_gi_members_overall_idx` within the `df_gi` DataFrame quantifies the reliability of the member information provided by initiatives in the General Information (GI) Survey. This index evaluates the consistency and accuracy of membership data reported over two consecutive years, providing a numerical value that reflects the overall reliability of this information.

#### Purpose

The `reliability_gi_members_overall_idx` is designed to assess and quantify the reliability of the membership information reported by initiatives. It focuses on year-over-year changes in membership numbers, verifying the consistency and accuracy of the data submitted. This index plays a crucial role in ensuring the credibility and trustworthiness of the initiatives' reported data.

#### Components

The reliability index is calculated based on the following components:

1. **Year-over-Year Membership Change**: Analyzes the difference in reported membership numbers between two consecutive years to identify increases, decreases, or no changes.

2. **Member Information Upload**: Considers whether initiatives have uploaded supporting documents that validate the reported membership data.

Based on these components, initiatives are categorized into different reliability statuses, which are then quantified into the overall index.

#### Calculation and Index Values

The `reliability_gi_members_overall_idx` assigns numerical values to categorize the reliability of initiatives' member information. The index ranges from a lower value indicating less reliability to a higher value signifying higher reliability. Categories may include:

- **High Reliability**: Assigned to initiatives that show consistent or increasing membership numbers with supporting documentation.
- **Medium Reliability**: Given to initiatives with some discrepancies in reported data or lacking comprehensive documentation, requiring further review.
- **Low Reliability**: Indicates significant issues with the data's consistency, accuracy, or documentation, signaling a need for improvement.

#### Implementation

To compute the `reliability_gi_members_overall_idx`, the following steps are undertaken:

- Analyze the year-over-year change in reported membership numbers.
- Evaluate the presence and quality of uploaded supporting documents.
- Assign a reliability status based on the analysis and categorize it into the overall index.

#### Impact on Initiatives

The `reliability_gi_members_overall_idx` serves as a key metric for initiatives to understand how their reported membership information is perceived in terms of reliability. A higher index value enhances an initiative's credibility, while a lower value may indicate areas requiring attention and improvement. This feedback mechanism encourages initiatives to maintain accurate and well-documented records, thereby strengthening their engagement with the survey.

#### Summary

The `reliability_gi_members_overall_idx` is an essential metric that encapsulates the reliability of membership information provided by initiatives in the GI Survey. By quantifying the credibility of reported data, it enables stakeholders to assess the trustworthiness of initiatives, facilitating informed decisions and supporting the overall integrity of the survey's findings.
"""












"""### Partner Information GI Sub-Index Documentation

The `partner_info_gi_subidx` within the `df_gi` DataFrame evaluates the extent of comprehensive partner information provided by initiatives in the General Information (GI) Survey. This sub-index is critical for understanding the scope and depth of an initiative's partnerships and collaborations.

#### Components and Weights

The Partner Information GI Sub-Index is comprised of the following components with their respective weights contributing to the sub-index:

1. `descrip_n_location_gi_status`: 45% - This measures whether initiatives have provided a complete description and location for their partners.
2. `priority_groups_gi_status`: 45% - This assesses whether initiatives have identified and described priority groups they are targeting or working with.
3. `regions_gi_status`: 10% - This evaluates the geographical spread and regional information of the partners.

#### Calculation Methodology

- The `partner_info_gi_subidx` is calculated by aggregating the weighted values of the above components based on the completeness of the information provided.
- A score is assigned to each component based on the presence and quality of data, which is then multiplied by the respective weight.
- The sum of these weighted scores is scaled to a percentage to produce the sub-index value.

#### Implementation

- Questions in the GI Survey are designed to elicit detailed responses about partners, priority groups, and regional engagement.
- The provided information is verified against predetermined criteria to ensure accuracy and completeness.
- The weighted scores are calculated programmatically to update the sub-index in real-time as survey data is entered or amended.

#### Impact and Importance

- The Partner Information GI Sub-Index is vital for gauging the breadth and depth of an initiative's network and its capacity to mobilize and engage various stakeholders.
- It also serves as a measure of transparency and operational openness, reflecting the initiative's commitment to inclusivity and collaboration.

---

### Members Information GI Sub-Index Documentation

The `members_info_gi_subidx` measures the completeness and detail of information provided about an initiative's members, crucial for assessing the initiative's base and level of support.

#### Components and Weights

The sub-index includes the following components:

1. `member_confirmation_gi_status`: 5% - Verifies whether an initiative has confirmed its members.
2. `members_type_gi_status`: 5% - Assesses the diversity of member types within the initiative.
3. `members_general_info_gi_status`: 20% - Evaluates the general information provided about members.
4. `members_n_reported_gi_status`: 40% - Measures the accuracy of member numbers reported by the initiative.
5. `members_data_upload_gi_status`: 30% - Checks for the presence of uploaded member data, indicating active and documented participation.

#### Calculation Methodology

- Scores are assigned based on the quality of information provided in each area, reflecting both the presence and depth of member-related data.
- These scores are weighted according to their relative importance and summed to calculate the `members_info_gi_subidx`.
- The final sub-index is presented as a percentage, providing a clear indication of how well the initiative has reported on its members.

#### Implementation

- The GI Survey collects detailed member information, which is then processed to determine the `members_info_gi_subidx`.
- This sub-index is updated continuously as new or revised member information is received and validated.

#### Impact and Importance

- Understanding the composition and scope of an initiative's membership is key to evaluating its reach and influence.
- The Members Information GI Sub-Index highlights the strength of the initiative's foundation, driving engagement and policy-making.

---

### Metrics GI Sub-Index Documentation

The `metrics_gi_subidx` evaluates the robustness of an initiative's strategies for metrics, data tracking, and validation as reported in the General Information (GI) Survey.

#### Components and Weights

The sub-index is composed of the following elements:

1. `metrics_info_gi_status`: 91% - This measures the initiative's methods and processes for tracking progress and collecting data to assess performance.
2. `metrics_upload_file_gi_status`: 9% - This assesses whether the initiative has uploaded documents that validate and support their data and metrics.

#### Calculation Methodology

- Each component is assigned a score reflecting the quality and completeness of the information provided.
- These scores are then weighted according to their assigned significance and aggregated to form the `metrics_gi_subidx`.
- The index is expressed as a percentage, clearly depicting the initiative's commitment to data accuracy and strategic metrics use.

#### Implementation

- Information for this sub-index is sourced from the GI Survey, specifically sections questioning the initiative's metrics and data validation practices.
- As initiatives update or provide additional documentation, the `metrics_gi_subidx` is recalculated to reflect these changes accurately.

#### Impact and Importance

- The precision of an initiative's metrics and data validation processes is crucial for ensuring the reliability of its reported progress and achievements.
- The Metrics GI Sub-Index serves as a benchmark for the initiative's analytical rigor and operational transparency.

---

### Sharm-El-Sheikh Adaptation Agenda (SAA) GI Sub-Index Documentation

The `saa_gi_subidx` quantifies the alignment and contribution of an initiative to the Sharm-El-Sheikh Adaptation Agenda (SAA) through responses given in the General Information (GI) Survey.

#### Components and Weights

The `saa_gi_subidx` is comprised of responses related to several key impact systems and cross-cutting enablers within the SAA framework. The components and their corresponding weights in the calculation of this sub-index are as follows:

1. `foodandagriculture_sub_subidx`: Represents the initiative's actions related to food and agriculture systems.
2. `waterandnatural_sub_subidx`: Covers the water and natural systems.
3. `humansettlements_sub_subidx`: Pertains to human settlements systems.
4. `coastalandoceanic_sub_subidx`: Involves coastal and oceanic systems.
5. `insfraestructure_sub_subidx`: Concerns infrastructure systems.
6. `health_sub_subidx`: Relates to health systems.
7. `planing_cross_sub_subidx`: Encompasses planning and policy with a cross-cutting approach.
8. `finance_cross_sub_subidx`: Includes finance and investment mechanisms with a cross-cutting approach.

Each of these components contributes an equal weight towards the final `saa_gi_subidx`.

#### Calculation Methodology

- The `saa_gi_subidx` is calculated by averaging the scores of the above-mentioned components, each reflecting the initiative's engagement with the corresponding system or enabler.
- The index is normalized to a scale of 0-100, where a higher score indicates greater alignment with the SAA objectives.

#### Implementation

- Initiatives report their activities and strategies within the GI Survey, which are then analyzed to score each component of the SAA GI Sub-Index.
- The sub-index is regularly updated to incorporate new information or improved responses, ensuring an accurate reflection of the initiative's current alignment with the SAA.

#### Impact and Importance

- The SAA GI Sub-Index serves as a comprehensive metric to assess how initiatives' actions support the overarching goals of the SAA.
- It encourages initiatives to engage with the SAA systematically, enhancing their contribution to global adaptation efforts.

---


### Action Clusters GI Sub-Index Documentation

The `action_clusterss_gi_subidx` assesses an initiative's identification and elaboration of resilience actions categorized into different clusters, a key aspect of their operational strategy.

#### Components and Weights

This sub-index is based on the initiative's engagement with various resilience action clusters. The responses are not weighted individually but are evaluated for their collective comprehensiveness.

#### Calculation Methodology

- Responses across multiple action clusters are reviewed for their completeness and relevance to the initiative's resilience strategies.
- The `action_clusterss_gi_subidx` is calculated based on the presence and quality of information across the different clusters, reflecting the initiative's overall engagement with resilience actions.

#### Implementation

- Detailed questions in the GI Survey capture the scope of the initiative's actions within each cluster.
- The sub-index is dynamically updated as initiatives provide new information or improve upon their existing responses.

#### Impact and Importance

- By measuring the initiative's involvement across various action clusters, the sub-index highlights the breadth and depth of their commitment to resilience.
- It encourages a holistic approach to resilience, emphasizing the importance of multi-faceted action plans.

---

### Type of Impact GI Sub-Index Documentation

The `type_impact_gi_subidx` measures an initiative's clarity and projected impact on different beneficiaries, a critical aspect of its goal-setting and strategic planning.

#### Components and Weights

The sub-index focuses solely on the reported type of impact, with a full weighting of 100% on the `type_of_impact` variable.

#### Calculation Methodology

- The initiative's intended impact is analyzed for its specificity and potential measurability.
- The `type_impact_gi_subidx` is determined by the presence of clear, targeted, and impactful goals as reported in the survey.

#### Implementation

- The GI Survey includes questions that directly address the type and scope of impact the initiative aims to achieve.
- This sub-index is updated as initiatives refine their impact statements and provide additional evidence of their targeted outcomes.

#### Impact and Importance

- Clear articulation of the type of impact is essential for aligning an initiative's activities with its overarching goals.
- The Type of Impact GI Sub-Index serves as a measure of the initiative's strategic focus and potential for real-world change.

---
"""


## PLEDGE 

"""### Pledge Overall Status Documentation

The pledge_overall_status column in the provided dataset is a comprehensive field that combines the completeness and reliability status of a pledge statement. This status is crucial for understanding the current state of a pledge in terms of its submission readiness and the trustworthiness of the information provided. The pledge_overall_status is derived by concatenating the pledge_completeness_status with the reliability_pledge_overall_status, providing a clear, at-a-glance indicator of both key aspects.

Completeness refers to whether all necessary information has been provided in the pledge statement. It is determined based on a completeness index (pledge_completeness_idx) that calculates the filled percentage of required fields. The pledge_completeness_status categorizes pledges into "Accepted" (for those with a high completeness index) or "Awaiting Completion" (for those missing crucial information).

Reliability addresses the credibility of the information provided in the pledge, focusing on how the pledge was prepared, specifically whether it was done in consultation with members. This aspect is captured in the reliability_pledge_overall_status, which aggregates specific reliability indicators related to metrics reliability and member consultation feedback.

The combination of these two dimensions into the pledge_overall_status provides a nuanced view of each pledge's readiness and reliability, highlighting those that are complete and have engaged their members in the pledge-making process (indicating higher reliability) and those that may require additional information or verification to reach an acceptable level of completeness and reliability. This status helps in prioritizing follow-ups, updates, or validations needed to enhance the quality and integrity of the pledge statements."""




"""### Pledge Completeness Index Documentation

The `pledge_completeness_idx` within the `df_pledge` DataFrame is a calculated metric representing the overall completeness percentage of responses to the Pledge Survey. This index is a crucial indicator of how thoroughly initiatives have provided information across key sections of the survey. The calculation of this index is based on a weighted sum of various sub-indices, each related to a specific aspect of the Pledge Survey. The weights assigned to each sub-index reflect their relative importance in gauging the comprehensive nature of the information provided.

#### Sub-Indices and Their Weights

1. **Responder ID Pledge Sub-Index** (`responder_id_pledge_subidx` - Weight: 3.33%)
   - Assesses the completeness of responder identification details.

2. **Primary Beneficiaries All Pledge Sub-Index** (`p_benefic_all_pledge_subidx` - Weight: 33.33%)
   - Evaluates the extent of detailed information provided about the primary beneficiaries of the initiative.

3. **Locally Led Commitment Pledge Sub-Index** (`locally_led_commitment_pledge_subidx` - Weight: 5.56%)
   - Measures the initiative's commitment to locally led approaches.

4. **Finance Pledge Sub-Index** (`finance_pledge_subidx` - Weight: 11.11%)
   - Assesses the clarity and detail of financial commitment and strategies.

5. **Metrics Explanation Pledge Sub-Index** (`metrics_explanation_pledge_subidx` - Weight: 11.11%)
   - Evaluates the thoroughness of the initiative's metrics and evaluation strategies.

6. **Climate Risk Assessment Pledge Sub-Index** (`climate_risk_assess_pledge_subidx` - Weight: 11.11%)
   - Measures the initiative's approach to climate risk assessment.

7. **Climate Diagnostic Pledge Sub-Index** (`climate_diagnost_pledge_subidx` - Weight: 11.11%)
   - Assesses the initiative's diagnostic measures related to climate impacts.

8. **Members Consultation Pledge Sub-Index** (`members_consultation_pledge_subidx` - Weight: 11.11%)
   - Evaluates the extent of consultation and involvement of members in the initiative.

9. **Confirmation Future Plans Pledge Sub-Index** (`confirmation_future_plans_pledge_subidx` - Weight: 2.22%)
   - Assesses the clarity and confirmation of future plans and strategies.

#### Calculation Methodology

The `pledge_completeness_idx` is calculated by aggregating the products of each sub-index score and its corresponding weight, as defined above. This approach ensures a comprehensive assessment, emphasizing areas of greater importance for a thorough understanding of each initiative's pledge.

#### Completeness Status and Requirements

The completeness status (`pledge_completeness_status`) is determined based on the `pledge_completeness_idx`, with initiatives scoring above 90% deemed "Accepted" and those below as "Awaiting Completion". The `pledge_completeness_req_priority` field identifies areas needing improvement, guiding initiatives to enhance their completeness.

#### Implementation

This calculation is implemented within the data processing pipeline, ensuring that each initiative's `pledge_completeness_idx`, along with its completeness status and areas for improvement, are accurately reflected in the `df_pledge` DataFrame. This structured approach facilitates effective monitoring and evaluation of the completeness of the information provided by initiatives.
"""

"""### Documentation of `reliability_pledge_overall_idx`

The `reliability_pledge_overall_idx` is a pivotal metric developed to quantify the overall reliability of the pledge statements provided by initiatives in the Pledge Statement Survey 2023. This index is crucial for understanding the credibility and trustworthiness of the commitments towards climate action and sustainability goals by the year 2030. Below is the detailed documentation of how the `reliability_pledge_overall_idx` is determined and its significance in the survey analysis.

#### Definition
- **`reliability_pledge_overall_idx`**: A numerical index ranging from 1 to 4, designed to represent the overall reliability of each initiative's pledge based on specific criteria evaluated from their survey responses. This index helps in categorizing the pledges into different levels of reliability, reflecting the thoroughness, documentation, and participatory approach in preparing their pledge statements.

#### Calculation
The `reliability_pledge_overall_idx` is calculated based on a set of predefined criteria that focus on the consultation process with members and the documentation provided for the metrics reported. The criteria include:
1. **Consultation with Members**: Initiatives are assessed on whether they have consulted their members while preparing the pledge statement. The degree of consultation plays a significant role in determining the index.
2. **Documentation of Metrics**: The reliability of the metrics reported in the pledge, including the process used to calculate or determine the number of individuals benefiting from the initiative, affects the index.
3. **Specific Responses**: Responses to targeted questions in the survey related to the consultation process and metrics documentation are used to assign a preliminary score.

#### Scoring Criteria
- **High Reliability (Score 4)**: Initiatives that have completed their pledge in thorough consultation with members and have provided detailed documentation for their metrics.
- **Medium Reliability (Score 3)**: Pledges partially completed in consultation with members, indicating a need for potential updates based on further member feedback.
- **Medium-Low Reliability (Score 2)**: Pledges that have not been consulted with members but indicate a plan for validation and update based on member feedback.
- **Low Reliability (Score 1)**: No information available indicating whether the pledge was completed in consultation with members, leading to the lowest reliability score.

#### Significance
- **Credibility Assessment**: The index serves as a benchmark for assessing the credibility of the pledges made by initiatives. A higher index indicates a more reliable and well-documented pledge.
- **Guidance for Improvement**: Initiatives with lower reliability scores are encouraged to enhance their consultation processes and documentation, thereby increasing the reliability of their pledges.
- **Comparative Analysis**: Allows for a comparative analysis of the reliability across different initiatives, highlighting areas of strength and opportunities for enhancement.

#### Conclusion
The `reliability_pledge_overall_idx` is a comprehensive measure that encapsulates the reliability of the pledges made by initiatives in the Pledge Statement Survey 2023. By assessing the degree of member consultation and the robustness of metrics documentation, this index plays a crucial role in ensuring the integrity and credibility of the commitments towards achieving climate action and sustainability goals by 2030.
"""


"""### Primary Beneficiaries All Pledge Sub-Index Documentation

The `p_benefic_all_pledge_subidx` within the `df_pledge` DataFrame aggregates the completeness and detail of reporting across various categories of primary beneficiaries. This composite metric is crucial for evaluating the pledge's scope and impact by measuring the thoroughness of beneficiary reporting.

#### Sub-Indices and Their Components

The overall sub-index is derived from the following sub-indices, each representing a specific category of primary beneficiaries, with their components and associated weights:

1. **Direct Individuals (`d_individuals_pledge_sub_subidx`)**: 
   - Components and Weights:
     - Priority Groups Status: 15%
     - Hazards Status: 5%
     - Number of Direct Individuals Status: 40%
     - Countries Status: 40%
   - Focuses on the detailed reporting of direct individual beneficiaries, including priority groups, hazards faced, total number impacted, and their geographical distribution.

2. **Companies (`companies_pledge_sub_subidx`)**: 
   - Components and Weights:
     - Number of Companies Status: 17.5%
     - Sector Status: 4.166%
     - Hazards Status: 4.166%
     - Types of Individuals Status: 4.166%
     - Number of Individuals Status: 35%
     - Countries Status: 35%
   - Assesses the level of detail provided about companies benefiting from the pledge, encompassing the number of companies, sectors involved, hazards addressed, types of individuals impacted, number of individuals, and geographical presence.

3. **Regions (`regions_pledge_sub_subidx`)**: 
   - Components and Weights:
     - Number of Regions Status: 17.5%
     - Beneficial All Status: 4.166%
     - Hazards Status: 4.166%
     - Types of Individuals Status: 4.166%
     - Number of Individuals Status: 35%
     - Countries Status: 35%
   - Measures the completeness of information on regional beneficiaries, covering the number of regions, types of hazards, types of individuals impacted, number of individuals, and geographical specifics.

4. **Cities (`cities_pledge_sub_subidx`)**: 
   - Components and Weights:
     - Number of Cities Status: 17.5%
     - Beneficial All Status: 4.166%
     - Hazards Status: 4.166%
     - Types of Individuals Status: 4.166%
     - Number of Individuals Status: 35%
     - Countries Status: 35%
   - Gauges the detail in reporting city beneficiaries, including the number of cities, hazards addressed, types of individuals affected, number of individuals, and the geographical scope.

5. **Natural Systems (`natsyst_pledge_sub_subidx`)**: 
   - Components and Weights:
     - Number of Hectares Status: 27.5%
     - Type of Natural Systems Status: 4.166%
     - Hazards Status: 4.166%
     - Types of Individuals Status: 4.166%
     - Number of Individuals Status: 30%
     - Countries Status: 30%
   - Evaluates the reporting on natural systems as beneficiaries, focusing on the types of natural systems, area covered, hazards addressed, types of individuals impacted, number of individuals, and geographical details.

#### Calculation Methodology

- The sub-index for each category is computed by aggregating the products of each component score and its corresponding weight.
- The `p_benefic_all_pledge_subidx` is then calculated by summing the scores of the individual sub-indices and dividing by the count of categories with reported information. This method ensures that the overall score reflects the average completeness across all reported beneficiary categories.

#### Application and Utility

- Facilitates initiatives in enhancing their reporting on primary beneficiaries by identifying areas needing improvement.
- Helps stakeholders in assessing the thoroughness of pledges' reporting, promoting transparency and accountability.

This comprehensive approach to evaluating primary beneficiaries' reporting emphasizes the importance of detailed information in understanding the impact and scope of pledges, aligning with the goals of transparency and accountability.
"""


"""### Metrics Explanation Pledge Sub-Index Documentation

The `metrics_explanation_pledge_subidx` within the `df_pledge` DataFrame quantifies the adequacy and clarity of explanations provided for the numbers reported in the pledge. This sub-index is critical for assessing how well the initiative understands and communicates the basis of its projected impacts by 2030.

#### Component

This sub-index is focused on a single component, the explanation for the numbers reported, which encompasses:

- **Explanation for Numbers Reported (`metrics_explanation_pledge`)**: 
  - Status: Whether an explanation is provided and deemed adequate.
  - Consideration is given to whether the provided explanations are sufficiently detailed and relevant, avoiding placeholders like 'TBD' or 'will add later', which indicate incomplete reporting.

#### Calculation Methodology

- The sub-index status is binary, with a status marked as true if an adequate explanation is provided, translating to a sub-index score of 100. Conversely, a lack of sufficient explanation or the use of placeholders results in a score of 0.
- The `metrics_explanation_pledge_subidx` directly reflects this binary assessment, emphasizing the importance of transparency and clarity in reporting pledge-related metrics.

#### Identifying Information Required

- Initiatives are guided to enhance their reporting by identifying areas where explanations for reported numbers are lacking or insufficient.
- The requirement highlights the need for initiatives to provide clear, comprehensible explanations that substantiate the numbers reported in their pledges.

#### Application and Utility

- This sub-index underscores the value of clear and logical explanations behind reported numbers, fostering greater understanding and confidence among stakeholders regarding the initiative's goals and methodologies.
- It serves as a benchmark for the initiative's commitment to transparency and accountability in reporting, encouraging continuous improvement in how data and projections are communicated.

The `metrics_explanation_pledge_subidx` thus plays a vital role in ensuring that stakeholders have a clear understanding of the basis for the initiative's projections, enhancing the credibility and impact of the pledge.

"""


"""### Members Consultation Pledge Sub-Index Documentation

The `members_consultation_pledge_subidx` within the `df_pledge` DataFrame evaluates the extent to which initiatives have involved their members in preparing the pledge statement. This sub-index reflects the participatory nature of the pledge-making process, underscoring the importance of member involvement for enhanced credibility and alignment with collective goals.

#### Components and Assessment Criteria

The sub-index is based on the responses to whether members were consulted in the pledge-making process, with a focus on:

- **Consultation of Members (`members_consultation_pledge`)**:
  - Status: Indicates if members were consulted, with a binary outcome determining the sub-index score.
  - A score of 100 signifies active member consultation, whereas 0 indicates no or insufficient consultation.

#### Calculation Methodology

- The score is binary, directly translating the consultation status into a sub-index score. The approach underscores the binary nature of member consultation in the pledge process, emphasizing it as a crucial factor for reliability and inclusiveness.

#### Identifying Information Required

- The initiative is prompted to disclose the degree of member consultation, aiming to highlight areas where participatory processes could be enhanced.
- The requirement encourages initiatives to ensure that their pledges are developed in a consultative manner, reflecting a broad consensus and input from all stakeholders.

#### Reliability Assessment

The reliability of the pledge in terms of member consultation is categorized based on the nature of member involvement:

- **High Reliability**: Indicates comprehensive member consultation, enhancing the pledge's credibility.
- **Medium Reliability**: Reflects partial member consultation, suggesting potential updates to the pledge based on further member input.
- **Medium-Low Reliability**: Points to a pledge not yet validated by member consultation, necessitating future confirmation and potential updates.
- **Low Reliability**: Marks pledges with minimal or no information on member consultation, highlighting a significant area for improvement.

#### Application and Utility

- The sub-index and associated reliability assessment serve as tools for initiatives to gauge and improve the inclusivity and representativeness of their pledge-making processes.
- By emphasizing member consultation, the framework promotes transparency, accountability, and collective ownership of the pledge, facilitating a more robust and aligned approach to achieving the initiative's goals.

This documentation lays the groundwork for understanding the significance of member consultation in the pledge-making process, encouraging initiatives to prioritize stakeholder engagement for more effective and inclusive climate action pledges.
"""
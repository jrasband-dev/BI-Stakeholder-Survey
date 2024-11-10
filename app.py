import streamlit as st
import pandas as pd
from io import StringIO

# Title of the app
st.title("Business Intelligence Department Survey")

# Introduction
st.write("""
    This survey is designed to assess how well the Business Intelligence (BI) department is serving its stakeholders. 
    Please answer the following questions based on your experience with the BI department's reports and services.
""")

# Likert scale options with numeric values
scale_options = {
    "Strongly Disagree": 1,
    "Disagree": 2,
    "Neutral": 3,
    "Agree": 4,
    "Strongly Agree": 5
}

# Grouping questions by section
sections = {
    "Accuracy and Reliability": [
        "The reports created by the BI department are accurate and reliable.",
        "I trust the reports the BI department has created for me."
    ],
    "Communication and Responsiveness": [
        "The BI department is responsive to my requests for information.",
        "The BI department communicates effectively about data sources and methodologies used in reports."
    ],
    "Value and Insight": [
        "The reports provided by the BI department add value to my decision-making.",
        "The BI department helps me uncover insights that I wouldn't have identified on my own."
    ],
    "Timeliness": [
        "The BI department delivers reports in a timely manner."
    ],
    "Usability and Clarity": [
        "The reports from the BI department are easy to understand and interpret.",
        "I can easily access and use the data in the BI reports."
    ],
    "Support and Training": [
        "The BI department provides sufficient training or support to help me understand how to use the reports.",
        "The BI department is willing to work with me on customizing reports to fit my needs."
    ],
    "Collaboration": [
        "The BI department collaborates well with other departments to ensure data meets organizational needs."
    ]
}

# Collect responses from the user
responses = {}
for section, questions in sections.items():
    st.write(f"### {section}")
    section_responses = []
    for question in questions:
        response = st.radio(question, list(scale_options.keys()))
        section_responses.append(response)
    responses[section] = section_responses

# Button to submit the survey
if st.button('Submit Survey'):
    st.write("Thank you for completing the survey!")

    # Create a DataFrame for the responses
    survey_data = []

    for section, questions in sections.items():
        for i, question in enumerate(questions):
            survey_data.append({
                "Section": section,
                "Question": question,
                "Response": responses[section][i]
            })
    
    df = pd.DataFrame(survey_data)

    # Calculate aggregate percentage for each section
    section_percentages = []
    for section, questions in sections.items():
        total_score = 0
        max_score = len(questions) * 5  # Maximum score if all responses are Strongly Agree (5)

        for i, question in enumerate(questions):
            response = responses[section][i]
            score = scale_options[response]
            total_score += score

        aggregate_percentage = (total_score / max_score) * 100
        section_percentages.append({
            "Section": section,
            "Aggregate Percentage": f"{aggregate_percentage:.2f}%"
        })

    # Create a DataFrame for the percentages
    df_percentages = pd.DataFrame(section_percentages)

    # Merge the responses and the percentages into one DataFrame
    df_merged = pd.merge(df, df_percentages, on="Section", how="left")

    # Display the merged data with responses and percentages
    st.write("### Survey Results with Percentages:")
    st.write(df_merged)

    # Prepare the CSV export
    csv = df_merged.to_csv(index=False)
    st.download_button(
        label="Download Survey Responses and Percentages as CSV",
        data=csv,
        file_name="bi_survey_responses_and_percentages.csv",
        mime="text/csv"
    )

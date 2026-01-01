import streamlit as st
import pickle as pickle
import pandas as pd
from streamlit.source_util import page_icon_and_name
import joblib


def add_sidebar():
    st.sidebar.header('User Inputs')

    bundle = joblib.load("model/attrition_bundle.pkl")

    model = bundle["model"]
    feature_names = bundle["feature_names"]
    feature_min = bundle["feature_min"]
    feature_max = bundle["feature_max"]

    print(feature_names)

    sidebar_labels = [
        # Numeric / ordinal features
        ("Age", "Age"),
        ("Daily Rate", "DailyRate"),
        ("Distance From Home", "DistanceFromHome"),
        ("Education Level", "Education"),
        ("Environment Satisfaction", "EnvironmentSatisfaction"),
        ("Gender (Male=1, Female=0)", "Gender"),
        ("Hourly Rate", "HourlyRate"),
        ("Job Involvement", "JobInvolvement"),
        ("Job Level", "JobLevel"),
        ("Job Satisfaction", "JobSatisfaction"),
        ("Monthly Income", "MonthlyIncome"),
        ("Monthly Rate", "MonthlyRate"),
        ("Number of Companies Worked", "NumCompaniesWorked"),
        ("Over Time (Yes=1, No=0)", "OverTime"),
        ("Percent Salary Hike", "PercentSalaryHike"),
        ("Performance Rating", "PerformanceRating"),
        ("Relationship Satisfaction", "RelationshipSatisfaction"),
        ("Stock Option Level", "StockOptionLevel"),
        ("Total Working Years", "TotalWorkingYears"),
        ("Training Times Last Year", "TrainingTimesLastYear"),
        ("Work Life Balance", "WorkLifeBalance"),
        ("Years At Company", "YearsAtCompany"),
        ("Years In Current Role", "YearsInCurrentRole"),
        ("Years Since Last Promotion", "YearsSinceLastPromotion"),
        ("Years With Current Manager", "YearsWithCurrManager"),

        # Business Travel (one-hot)
        ("Business Travel: Non-Travel", "Travel_Non-Travel"),
        ("Business Travel: Frequently", "Travel_Travel_Frequently"),
        ("Business Travel: Rarely", "Travel_Travel_Rarely"),

        # Department (one-hot)
        ("Department: Human Resources", "Department_Human Resources"),
        ("Department: Research & Development", "Department_Research & Development"),
        ("Department: Sales", "Department_Sales"),

        # Education Field (one-hot)
        ("Education Field: Human Resources", "EducationField_Human Resources"),
        ("Education Field: Life Sciences", "EducationField_Life Sciences"),
        ("Education Field: Marketing", "EducationField_Marketing"),
        ("Education Field: Medical", "EducationField_Medical"),
        ("Education Field: Other", "EducationField_Other"),
        ("Education Field: Technical Degree", "EducationField_Technical Degree"),

        # Job Role (one-hot)
        ("Job Role: Healthcare Representative", "JobRole_Healthcare Representative"),
        ("Job Role: Human Resources", "JobRole_Human Resources"),
        ("Job Role: Laboratory Technician", "JobRole_Laboratory Technician"),
        ("Job Role: Manager", "JobRole_Manager"),
        ("Job Role: Manufacturing Director", "JobRole_Manufacturing Director"),
        ("Job Role: Research Director", "JobRole_Research Director"),
        ("Job Role: Research Scientist", "JobRole_Research Scientist"),
        ("Job Role: Sales Executive", "JobRole_Sales Executive"),
        ("Job Role: Sales Representative", "JobRole_Sales Representative"),

        # Marital Status (one-hot)
        ("Marital Status: Divorced", "MaritalStatus_Divorced"),
        ("Marital Status: Married", "MaritalStatus_Married"),
        ("Marital Status: Single", "MaritalStatus_Single"),
    ]

    BINARY_FEATURES = {
        "Gender": "Male",
        "OverTime": "Over Time"
    }

    ONE_HOT_GROUPS = {
        "Business Travel": {
            "Non-Travel": "Travel_Non-Travel",
            "Frequently": "Travel_Travel_Frequently",
            "Rarely": "Travel_Travel_Rarely"
        },
        "Department": {
            "Human Resources": "Department_Human Resources",
            "Research & Development": "Department_Research & Development",
            "Sales": "Department_Sales"
        },
        "Education Field": {
            "Human Resources": "EducationField_Human Resources",
            "Life Sciences": "EducationField_Life Sciences",
            "Marketing": "EducationField_Marketing",
            "Medical": "EducationField_Medical",
            "Other": "EducationField_Other",
            "Technical Degree": "EducationField_Technical Degree"
        },
        "Job Role": {
            "Healthcare Representative": "JobRole_Healthcare Representative",
            "Human Resources": "JobRole_Human Resources",
            "Laboratory Technician": "JobRole_Laboratory Technician",
            "Manager": "JobRole_Manager",
            "Manufacturing Director": "JobRole_Manufacturing Director",
            "Research Director": "JobRole_Research Director",
            "Research Scientist": "JobRole_Research Scientist",
            "Sales Executive": "JobRole_Sales Executive",
            "Sales Representative": "JobRole_Sales Representative"
        },
        "Marital Status": {
            "Divorced": "MaritalStatus_Divorced",
            "Married": "MaritalStatus_Married",
            "Single": "MaritalStatus_Single"
        }
    }

    inputs = {}

    st.sidebar.subheader("Numeric Features")
    for label, key in sidebar_labels:
        if key in BINARY_FEATURES:
            continue
        if any(key in group.values() for group in ONE_HOT_GROUPS.values()):
            continue

        inputs[key] = st.sidebar.slider(
            label=label,
            min_value=float(feature_min[key]),
            max_value=float(feature_max[key]),
            value=float((feature_min[key] + feature_max[key]) / 2)
        )


    st.sidebar.subheader("Binary Features")
    for key, label in BINARY_FEATURES.items():
        inputs[key] = 1 if st.sidebar.checkbox(label) else 0

    st.sidebar.subheader("Categorical Features")

    for group_label, options in ONE_HOT_GROUPS.items():
        choice = st.sidebar.selectbox(group_label, list(options.keys()))

        for col in options.values():
            inputs[col] = 0

        inputs[options[choice]] = 1
    return inputs

def main():
    st.set_page_config(
        page_title = "Employee Attrition Predictor",
        page_icon = ":female:",
        layout = "wide",
        initial_sidebar_state = "expanded",
    )

    input_data = add_sidebar()

    with st.container():
        st.title("Employee Attrition Predictor")
        st.write("Welcome to the Employee Attrition Predictor! This tool is here to help you explore employee data and gain insights that support better workplace decisions.Simply provide the details, and let the system assist you in understanding attrition patterns with ease.")

    col1, col2 = st.columns([4,1])

    with col1:
        st.write("This is column 1")
    with col2:
        st.write("This is column 2")

if __name__ == "__main__":
    main()

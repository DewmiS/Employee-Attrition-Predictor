import streamlit as st
import pandas as pd
import joblib
import plotly.graph_objects as go
import numpy as np

RADAR_FEATURES = {
    "MonthlyIncome", "StockOptionLevel", "PercentSalaryHike",
    "OverTime", "TotalWorkingYears", "YearsAtCompany",
    "JobSatisfaction", "EnvironmentSatisfaction", "WorkLifeBalance",
    "JobLevel", "TrainingTimesLastYear", "YearsSinceLastPromotion",
    "NumCompaniesWorked", "YearsWithCurrManager"
}

def add_sidebar():
    st.sidebar.header('User Inputs')

    bundle = joblib.load("model/attrition_bundle.pkl")

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

    binary_features = {
        "Gender": "Male",
        "OverTime": "Over Time"
    }

    one_hot_groups = {
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
        if key in binary_features:
            continue
        if any(key in group.values() for group in one_hot_groups.values()):
            continue

        inputs[key] = st.sidebar.slider(
            label=label,
            min_value=float(feature_min[key]),
            max_value=float(feature_max[key]),
            value=float((feature_min[key] + feature_max[key]) / 2)
        )


    st.sidebar.subheader("Binary Features")
    for key, label in binary_features.items():
        inputs[key] = 1 if st.sidebar.checkbox(label) else 0

    st.sidebar.subheader("Categorical Features")

    for group_label, options in one_hot_groups.items():
        choice = st.sidebar.selectbox(group_label, list(options.keys()))

        for col in options.values():
            inputs[col] = 0

        inputs[options[choice]] = 1
    return inputs, feature_min, feature_max


def normalize(value, min_val, max_val):
    if max_val == min_val:
        return 0
    return (value - min_val) / (max_val - min_val)


def get_radar_chart(input_data, feature_min, feature_max):

    radar = build_radar_values(input_data, feature_min, feature_max)

    categories = list(radar.keys())
    values = list(radar.values())

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Employee Profile'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1]
            )
        ),
        showlegend=False
    )

    return fig


def build_radar_values(inputs, feature_min, feature_max):
    radar_norm = {}

    for feature in RADAR_FEATURES:
        radar_norm[feature] = normalize(
            inputs[feature],
            feature_min[feature],
            feature_max[feature]
        )

    return radar_norm


def add_predictions(input_data):
    model = joblib.load(open("model/attrition_random_forest_model.pkl", "rb"))

    input_array = np.array(list(input_data.values())).reshape(1, -1)

    predictions = model.predict(input_array)

    if predictions[0] == 1:
        st.write("Employee may leave the company")
    else:
        st.write("Employee may not leave the company")

    st.write("Probability of leaving company", model.predict_proba(input_array)[0][1])
    st.write("Probability of not leaving company", model.predict_proba(input_array)[0][0])


def main():
    st.set_page_config(
        page_title = "Employee Attrition Predictor",
        page_icon = ":female:",
        layout = "wide",
        initial_sidebar_state = "expanded",
    )

    input_data, feature_min, feature_max = add_sidebar()

    with st.container():
        st.title("Employee Attrition Predictor")
        st.write("Welcome to the Employee Attrition Predictor! This tool is here to help you explore employee data and gain insights that support better workplace decisions.Simply provide the details, and let the system assist you in understanding attrition patterns with ease.")

    col1, col2 = st.columns([3,2])

    with col1:
        radar_chart = get_radar_chart(input_data, feature_min, feature_max)
        st.plotly_chart(radar_chart, width="stretch")

        add_predictions(input_data)

        st.markdown("---")

        bundle = joblib.load("model/attrition_bundle.pkl")
        model = bundle["model"]
        feature_names = bundle["feature_names"]

        importance_df = pd.DataFrame({
            "Feature": feature_names,
            "Importance": model.feature_importances_
        }).sort_values(by="Importance", ascending=False).head(15)

        fig_importance = go.Figure(
            go.Bar(
                x=importance_df["Importance"],
                y=importance_df["Feature"],
                orientation="h"
            )
        )

        fig_importance.update_layout(
            title="Top Factors Influencing Attrition",
            yaxis=dict(autorange="reversed")
        )

        st.plotly_chart(fig_importance, width="stretch")

    with col2:
        st.subheader("Live Model Inputs")

        feature_df = pd.DataFrame(
            input_data.items(),
            columns=["Feature", "Value"]
        )

        st.dataframe(feature_df, use_container_width=True, height=600)

        st.subheader("Input VS Average")
        avg_values = feature_min + (feature_max - feature_min) / 2

        compare_df = pd.DataFrame({
            "User": input_data,
            "Average": avg_values
        }).head(10)

        st.line_chart(compare_df)


if __name__ == "__main__":
    main()

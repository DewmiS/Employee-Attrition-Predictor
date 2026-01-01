import streamlit as st
import pickle as pickle
import pandas as pd
from streamlit.source_util import page_icon_and_name


def add_sidebar():
    st.sidebar.header('User Inputs')


def main():
    st.set_page_config(
        page_title = "Employee Attrition Predictor",
        page_icon = ":female:",
        layout = "wide",
        initial_sidebar_state = "expanded",
    )

    add_sidebar()

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

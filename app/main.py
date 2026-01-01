import streamlit as st
import pickle as pickle
import pandas as pd
from streamlit.source_util import page_icon_and_name


def main():
    st.set_page_config(
        page_title = "Employee Attrition Predictor",
        page_icon = ":female:",
        layout = "wide",
        initial_sidebar_state = "expanded",
    )

    st.write("# Employee Attrition Predictor")


if __name__ == "__main__":
    main()

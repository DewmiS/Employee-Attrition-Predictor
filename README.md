# Employee Attrition Predictor 

An interactive **Machine Learning dashboard** built with **Streamlit** to predict employee attrition and explain the underlying factors influencing the prediction.

This project allows users to input employee-related features, visualize them interactively, and understand attrition risk through intuitive charts and tables.

---

##  Features

-  **Attrition Prediction**
  - Predicts whether an employee is likely to leave the organization
  - Uses a trained **Random Forest Classifier**

-  **Interactive User Inputs**
  - Sliders for numeric features
  - Checkboxes for binary features
  - Select boxes for categorical (one-hot encoded) features

-  **Radar Chart Visualization**
  - Values are normalized for fair comparison

-  **Live Feature Table**
  - Displays **all model input features live**
  - Updates instantly as user inputs change
  - Ensures full transparency of model inputs

-  **Explainable Design**
  - Clear separation between:
    - Model inputs
    - Visualization
    - Prediction logic

---

##  Machine Learning Details

- **Model**: Random Forest Classifier  
- **Target Variable**: `Attrition` (Yes / No)  
- **Preprocessing**:
  - Binary encoding (Yes/No, Male/Female)
  - One-hot encoding for categorical variables
- **Artifacts Stored**:
  - Trained model
  - Feature names
  - Feature-wise minimum and maximum values (used for normalization)

All artifacts are bundled and loaded from a pickle file.

---

##  Tech Stack

- **Python**
- **Streamlit** – Web application framework
- **Scikit-learn** – Machine learning
- **Plotly** – Interactive visualizations
- **Pandas / NumPy** – Data handling
- **Joblib** – Model persistence

---

##  How to Run the App

1. **Clone the repository**
```bash
git clone https://github.com/DewmiS/employee-attrition-predictor.git
cd employee-attrition-predictor
```
2. **Install dependencies**
 ```
   pip install -r requirements.txt
  
```
4. **Run the Streamlit app**
```
  streamlit run app/main.py
```

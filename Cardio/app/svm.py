import streamlit as st
from app.models import read_svm
import numpy as np

st.header('Cardio Vascular Disease Prediction')
st.subheader('Using :blue[SVM]')

model, scaler = read_svm()

st.sidebar.header(
    'Filter Data'
)

age = st.sidebar.slider(
    'Age',
    min_value=28,
    max_value=65,
    value=40,
    step=1
)

gender_dict = {1: 'Female', 2: 'Male'}
gender = st.sidebar.radio(# selectbox for dropdown
    'Gender',
    options=gender_dict.keys(),
    format_func=lambda x: gender_dict.get(x)
)

height = st.sidebar.slider(
    'Height', min_value=150, max_value=190, value=160
)

weight = st.sidebar.slider(
    'Weight', min_value=45, max_value=110, value=55
)

ap_hi = st.sidebar.slider(
    'Systolic Pressure', min_value=90, max_value=180, value=120
)

ap_lo = st.sidebar.slider(
    'Disystolic Pressure', min_value=60, max_value=130, value=80
)

cholesterol_dict = {1: 'Low Cholesterol', 2: 'Mid Cholesterol', 3: 'High Cholesterol'}
cholesterol = st.sidebar.radio(# selectbox for dropdown
    'Cholesterol',
    options=cholesterol_dict.keys(),
    format_func=lambda x: cholesterol_dict.get(x)
)

gluc_dict = {1: 'Low Glucose', 2: 'Mid Glucose', 3: 'High Glucose'}
gluc = st.sidebar.radio(# selectbox for dropdown
    'Glucose',
    options=gluc_dict.keys(),
    format_func=lambda x:gluc_dict.get(x)
)

smoke_dict = {0:'Does not Smoke', 1: 'Does Smoke'}
smoke= st.sidebar.radio(# selectbox for dropdown
    'Smoke',
    options=smoke_dict.keys(),
    format_func=lambda x: smoke_dict.get(x)
)

alco_dict = {0:'Does not drink', 1: 'Does drink'}
alco= st.sidebar.radio(# selectbox for dropdown
    'Alcohol',
    options=alco_dict.keys(),
    format_func=lambda x: alco_dict.get(x)
)

active_dict = {0:'Does do PA', 1: 'Does not do PA'}
active= st.sidebar.radio(# selectbox for dropdown
    'Physical Activities',
    options=active_dict.keys(),
    format_func=lambda x: active_dict.get(x)
)

# Predict
if st.button('Predict'):
    input_data = np.array([[
        age, gender, height, weight, ap_hi, ap_lo, cholesterol, gluc, smoke, alco, active
    ]])
    
    input_scaler = scaler.transform(input_data)
    
    prediction = model.predict(input_scaler)[0]
    
    if prediction == 0:
        st.success('No cardiovascular disease found.')
        st.write('Likely to be healthy.')
        
    else:
        st.warning('Cardiovascular disease found.')
        st.write('Likely to be unhealthy.')
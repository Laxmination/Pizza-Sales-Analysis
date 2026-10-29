import streamlit as st

st.set_page_config(
    page_title='Cardiovascular Prediction - Dashboard'
)

def home():
    st.Page("home.py")
    st.header('Cardiovascular Disease Prediction')

pages ={
    'Home':{
        st.Page(home)
    },
    'Models':{
        st.Page('app/logistic.py', title='Logistic Regression'),
        st.Page('app/svm.py', title='SVM')
    }
}

pg = st.navigation(pages, position='top')
pg.run()

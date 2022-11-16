# import necessary files
import streamlit as st
import tabs

# setting up streamlit for interactive user experience
# two types for olympic data analysis
st.set_page_config(layout="wide")
tab1, tab2 = st.tabs(["Summer Olympics", "Winter Olympics"])
st.sidebar.title("Olympics Data Analysis")
# image source: https://1000logos.net/wp-content/uploads/2017/05/Olympics-Logo-1986.png
st.sidebar.image('https://1000logos.net/wp-content/uploads/2017/05/Olympics-Logo-1986.png')

# selection for user menu :
# can switch between tabs for summer and winter olympics
user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally', 'Overall Stats', 'Country-wise Stats')
)
with tab1:
    tabs.select_season("Summer", user_menu)

with tab2:
    tabs.select_season("Winter", user_menu)


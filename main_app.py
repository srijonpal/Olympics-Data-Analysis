import streamlit as st
import tabs

st.set_page_config(layout="wide")
tab1, tab2 = st.tabs(["Summer Olympics", "Winter Olympics"])
st.sidebar.title("Olympics Data Analysis")
st.sidebar.image('https://e7.pngegg.com/pngimages/1020/402/png-clipart-2024-summer-olympics-brand-circle-area-olympic-rings-olympics-logo-text-sport.png')
user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally', 'Overall Stats', 'Country-wise Stats')
)
with tab1:
    tabs.select_season("Summer",user_menu)

with tab2:
    tabs.select_season("Winter",user_menu)


import streamlit as st

st.set_page_config(
    page_title="DSE Market Insights",
    page_icon="📊",
    layout="wide",
    # initial_sidebar_state="expanded",
)

# Load external CSS file
main_css = open("styles/main_pages.css", encoding='utf-8').read()
st.markdown(f'<style>{main_css}</style>', unsafe_allow_html=True)

st.write("# Coming Soon! ")

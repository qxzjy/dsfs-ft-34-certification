import streamlit as st
st.set_page_config(layout="wide")

from utils.common import load_delay, load_pricing

# Load data
df_delay = load_delay()
df_pricing = load_pricing()

pages = [
    st.Page("pages/home.py", title="Getaround"),
    st.Page("pages/eda.py", title="EDA", icon="📈"),
    st.Page("pages/thresholds.py", title="Thresholds analysis", icon="🔬"),
    st.Page("pages/pricing.py", title="Daily rental price prediction", icon="💵")
]

pg = st.navigation(pages)
pg.run()
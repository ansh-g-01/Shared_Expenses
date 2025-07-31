import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="User Directory", layout="wide")
st.title("📋 Registered Users")

BASE_URL = "http://localhost:8000"  # Change if deployed

# --- Fetch Users from API ---
try:
    response = requests.get(f"{BASE_URL}/users/all/")
    response.raise_for_status()
    users = response.json()
except Exception as e:
    st.error("Failed to fetch users.")
    st.exception(e)
    st.stop()

# --- Convert to DataFrame ---
df = pd.DataFrame(users)

# --- Format created_at nicely ---
df['created_at'] = pd.to_datetime(df['created_at']).dt.strftime('%Y-%m-%d %H:%M')

# --- Display as Table ---
st.subheader("👥 All Registered Users")
st.dataframe(df[['id', 'name', 'email', 'phone', 'created_at']], use_container_width=True)

# Optional: Filter or search
with st.expander("🔍 Filter Users"):
    search_name = st.text_input("Search by name")
    if search_name:
        filtered_df = df[df["name"].str.contains(search_name, case=False)]
        st.dataframe(filtered_df[['id', 'name', 'email', 'phone', 'created_at']], use_container_width=True)

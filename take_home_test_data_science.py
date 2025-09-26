# take_home_test_data_science.py
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="whitegrid")

st.set_page_config(page_title="Food Delivery Times Dashboard", layout="wide")

@st.cache_data
def load_data(path="food_delivery_times_clean.csv"):
    return pd.read_csv(path)

# ---------- Load data ----------
st.title("🍽 Food Delivery Times — Dashboard")
st.caption("Interactive dashboard untuk eksplorasi data pengiriman dan identifikasi risiko keterlambatan")

df = load_data()

# --- debug: lihat kolom & sample (hapus nanti) ---
with st.expander("DEBUG: Dataset info (hapus jika sudah oke)"):
    st.write("Jumlah baris:", len(df))
    st.write("Columns:", df.columns.tolist())
    st.write(df.dtypes)
    st.dataframe(df.head(5))
# ------------------------------------------------



# take_home_test_data_science.py
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO

sns.set(style="whitegrid")

st.set_page_config(page_title="Food Delivery Times Dashboard", layout="wide")

@st.cache_data
def load_data(path="food_delivery_times_clean.csv"):
    df = pd.read_csv(path)
    return df

# ---------- Load data ----------
st.title("🍽 Food Delivery Times — Dashboard")
st.caption("Interactive dashboard untuk eksplorasi data pengiriman dan identifikasi risiko keterlambatan")

df = load_data()

# ---------- Sidebar filters ----------
st.sidebar.header("Filter Data")
unique_weather = ["All"] + sorted(df['weather'].astype(str).unique().tolist())
weather_sel = st.sidebar.selectbox("Weather", unique_weather, index=0)

unique_dist_cat = ["All"] + sorted(df['distance_category'].astype(str).unique().tolist())
dist_cat_sel = st.sidebar.selectbox("Distance category", unique_dist_cat, index=0)

unique_time_of_day = ["All"] + sorted(df['time_of_day'].astype(str).unique().tolist())
time_sel = st.sidebar.selectbox("Time of day", unique_time_of_day, index=0)

unique_vehicle = ["All"] + sorted(df['vehicle_type'].astype(str).unique().tolist())
vehicle_sel = st.sidebar.selectbox("Vehicle type", unique_vehicle, index=0)

min_dist, max_dist = float(df['distance_km'].min()), float(df['distance_km'].max())
dist_range = st.sidebar.slider("Distance (km) range", min_value=0.0, max_value=float(max_dist), value=(min_dist, max_dist), step=0.5)

# Apply filters
df_filtered = df.copy()
if weather_sel != "All":
    df_filtered = df_filtered[df_filtered['weather'].astype(str) == weather_sel]
if dist_cat_sel != "All":
    df_filtered = df_filtered[df_filtered['distance_category'].astype(str) == dist_cat_sel]
if time_sel != "All":
    df_filtered = df_filtered[df_filtered['time_of_day'].astype(str) == time_sel]
if vehicle_sel != "All":
    df_filtered = df_filtered[df_filtered['vehicle_type'].astype(str) == vehicle_sel]

df_filtered = df_filtered[(df_filtered['distance_km'] >= dist_range[0]) & (df_filtered['distance_km'] <= dist_range[1])]

# ---------- KPI cards ----------
st.subheader("Overview")
col1, col2, col3, col4 = st.columns([1.5,1.5,1.5,1.5])

with col1:
    st.metric("Total Orders (filtered)", f"{len(df_filtered):,}")

with col2:
    avg_dt = df_filtered['delivery_time_min'].mean()
    st.metric("Avg Delivery Time (min)", f"{avg_dt:.1f}")

with col3:
    if 'prep_per_km' in df_filtered.columns:
        avg_ppk = df_filtered['prep_per_km'].mean()
        st.metric("Avg Prep per Km", f"{avg_ppk:.2f}")
    else:
        st.write("")

with col4:
    if 'is_bad_weather' in df_filtered.columns:
        pct_bad = (df_filtered['is_bad_weather'].sum() / (len(df_filtered) + 1e-9)) * 100
        st.metric("% Bad Weather", f"{pct_bad:.1f}%")
    else:
        st.write("")

# ---------- Simple segmentation: High vs Low delay risk ----------
st.subheader("Segmentation: High vs Low Delay Risk ( contoh rule-based )")
# Rule: High risk if distance > 15 km OR is_bad_weather == 1
df_filtered['risk'] = np.where((df_filtered['distance_km'] > 15) | (df_filtered.get('is_bad_weather', 0) == 1), 'High', 'Low')
risk_count = df_filtered['risk'].value_counts(normalize=True).mul(100).round(1)
colA, colB = st.columns(2)
with colA:
    st.write("Risk distribution (%)")
    st.bar_chart(risk_count)

with colB:
    high_mean = df_filtered[df_filtered['risk']=='High']['delivery_time_min'].mean()
    low_mean = df_filtered[df_filtered['risk']=='Low']['delivery_time_min'].mean()
    st.write(f"Avg delivery time — High risk: {high_mean:.1f} min")
    st.write(f"Avg delivery time — Low risk: {low_mean:.1f} min")
    st.write(f"Avg extra delay (High - Low): {high_mean - low_mean:.1f} min")

# ---------- Visualizations ----------
st.subheader("Visualisasi")

# 1. Histogram delivery time
st.markdown("*Distribusi Delivery Time*")
fig1, ax1 = plt.subplots(figsize=(8,3))
sns.histplot(df_filtered['delivery_time_min'], bins=30, kde=True, ax=ax1)
ax1.set_xlabel("Delivery time (min)")
st.pyplot(fig1)

# 2. Boxplot by weather (if exists)
if 'weather' in df_filtered.columns:
    st.markdown("*Boxplot: Delivery Time per Weather*")
    fig2, ax2 = plt.subplots(figsize=(8,3))
    sns.boxplot(x='weather', y='delivery_time_min', data=df_filtered, ax=ax2)
    ax2.set_xlabel("Weather")
    ax2.set_ylabel("Delivery time (min)")
    st.pyplot(fig2)

# 3. Bar: avg delivery time per distance category
if 'distance_category' in df_filtered.columns:
    st.markdown("*Rata-rata Delivery Time per Distance Category*")
    avg_by_cat = df_filtered.groupby('distance_category')['delivery_time_min'].mean().sort_index()
    fig3, ax3 = plt.subplots(figsize=(6,3))
    avg_by_cat.plot(kind='bar', ax=ax3)
    ax3.set_ylabel("Avg delivery time (min)")
    st.pyplot(fig3)

# 4. Scatter distance vs delivery with regression line
st.markdown("*Distance vs Delivery Time (Trend)*")
fig4, ax4 = plt.subplots(figsize=(7,4))
sns.regplot(x='distance_km', y='delivery_time_min', data=df_filtered.sample(min(800, len(df_filtered))), scatter_kws={'s':20, 'alpha':0.5}, line_kws={'color':'red'}, ci=None, ax=ax4)
ax4.set_xlabel("Distance (km)")
ax4.set_ylabel("Delivery time (min)")
st.pyplot(fig4)

# ---------- Data preview & download ----------
st.subheader("Preview Data (filtered)")
st.dataframe(df_filtered.reset_index(drop=True).head(200))

def convert_df_to_csv_bytes(df_in):
    return df_in.to_csv(index=False).encode('utf-8')

csv_bytes = convert_df_to_csv_bytes(df_filtered)
st.download_button(label="Download filtered data as CSV", data=csv_bytes, file_name="food_delivery_times_filtered.csv", mime="text/csv")

# ---------- Footer / Notes ----------
st.markdown("---")
st.markdown("*Notes:*")
st.markdown("- Gunakan filter di sidebar untuk eksplorasi lebih lanjut.")
st.markdown("- Segmentasi yang dipakai adalah contoh rule-based; untuk production sebaiknya gunakan model risiko terlatih.")
st.markdown("- Kalau mau tambahkan prediksi model (XGBoost), upload file model (.pkl) dan kita bisa tambahkan form prediction.")

st.info("Ready — Jalankan streamlit run take_home_test_data_science.py di environment yang sudah menginstall requirements.txt")


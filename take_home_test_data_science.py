# app_food_delivery_insight.py
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Food Delivery Dashboard", layout="wide")
sns.set(style="whitegrid")

@st.cache_data
def load_data(path="food_delivery_times_clean.csv"):
    return pd.read_csv(path)

# ---------------- LOAD DATA ----------------
st.title("🍽 Food Delivery Times — Analisis & Insight Dashboard")
st.caption("Dashboard interaktif untuk analisis waktu pengiriman makanan dan rekomendasi bisnis")

df = load_data()

# ---------------- KPI ----------------
st.subheader("📊 Key Metrics")
col1, col2, col3 = st.columns(3)

total_orders = len(df)
avg_time = df["delivery_time_min"].mean()
avg_dist = df["distance_km"].mean()

with col1:
    st.metric("Total Orders", f"{total_orders:,}")
with col2:
    st.metric("Avg Delivery Time (min)", f"{avg_time:.1f}")
with col3:
    st.metric("Avg Distance (km)", f"{avg_dist:.1f}")

# ---------------- VISUALISASI ----------------
st.subheader("📈 Visualisasi Utama")

# Histogram delivery time
fig, ax = plt.subplots(figsize=(6,3))
sns.histplot(df["delivery_time_min"], bins=30, kde=True, ax=ax)
ax.set_title("Distribusi Delivery Time (menit)")
st.pyplot(fig)

# Scatter distance vs time
fig2, ax2 = plt.subplots(figsize=(6,3))
sns.scatterplot(x="distance_km", y="delivery_time_min", data=df, alpha=0.5, ax=ax2)
sns.regplot(x="distance_km", y="delivery_time_min", data=df, scatter=False, ax=ax2, color="red")
ax2.set_title("Hubungan Jarak vs Waktu Pengiriman")
st.pyplot(fig2)

# Boxplot per cuaca
if "weather" in df.columns:
    fig3, ax3 = plt.subplots(figsize=(6,3))
    sns.boxplot(x="weather", y="delivery_time_min", data=df, ax=ax3)
    ax3.set_title("Delivery Time per Weather")
    st.pyplot(fig3)

# ---------------- INSIGHT OTOMATIS ----------------
st.subheader("🔍 Insight Analysis")

late_threshold = 40  # definisi terlambat (> 40 menit)
late_pct = (df["delivery_time_min"] > late_threshold).mean() * 100

# Faktor cuaca
if "weather" in df.columns:
    weather_delay = df.groupby("weather")["delivery_time_min"].mean().sort_values(ascending=False).head(1)
    worst_weather = weather_delay.index[0]
    worst_weather_time = weather_delay.values[0]
else:
    worst_weather, worst_weather_time = None, None

# Faktor jarak
long_distance_time = df[df["distance_km"] > 15]["delivery_time_min"].mean()
short_distance_time = df[df["distance_km"] <= 15]["delivery_time_min"].mean()
extra_delay = long_distance_time - short_distance_time

insight_text = f"""
1. *Ketepatan Waktu*  
   - Sekitar *{late_pct:.1f}%* pengiriman melebihi {late_threshold} menit → indikasi potensi keterlambatan.

2. *Faktor Jarak*  
   - Rata-rata pengiriman jarak jauh (>15 km) membutuhkan *{long_distance_time:.1f} menit*,  
     sedangkan jarak pendek (≤15 km) hanya *{short_distance_time:.1f} menit*.  
   - Ada tambahan keterlambatan rata-rata *{extra_delay:.1f} menit* untuk jarak jauh.

3. *Faktor Cuaca*  
"""
if worst_weather:
    insight_text += f"- Kondisi cuaca *{worst_weather}* paling berpengaruh dengan rata-rata waktu *{worst_weather_time:.1f} menit*.\n"
else:
    insight_text += "- Data cuaca tidak tersedia.\n"

st.markdown(insight_text)

# ---------------- REKOMENDASI BISNIS ----------------
st.subheader("💡 Rekomendasi Bisnis")
st.success(f"""
- Fokus perbaikan pada *{late_pct:.1f}% order yang terlambat*.  
- Optimalkan pengiriman jarak jauh dengan:  
  • Penempatan kurir/driver di lokasi strategis dekat pelanggan.  
  • Kolaborasi dengan lebih banyak restoran di area luar kota.  

- Jika cuaca buruk (misalnya {worst_weather if worst_weather else "hujan/storm"}), pertimbangkan:  
  • Notifikasi estimasi pengiriman lebih panjang ke pelanggan.  
  • Penambahan insentif driver agar tetap tersedia saat cuaca buruk.  

- Monitor terus *trend delay per segmen* (cuaca, jarak, jam sibuk).  
- Gunakan insight ini untuk meningkatkan kepuasan pelanggan & menekan biaya kompensasi.
""")

# ---------------- DATA PREVIEW ----------------
st.subheader("🔍 Data Preview")
st.dataframe(df.head(100))




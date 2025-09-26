# food_delivery_dashboard.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Food Delivery Dashboard", layout="wide")

# ======================
# LOAD DATA
# ======================
@st.cache_data
def load_data(path="food_delivery_times_clean.csv"):
    return pd.read_csv(path)

df = load_data()

st.title("🚴 Food Delivery Performance Dashboard")
st.caption("Ringkasan performa pengiriman makanan berdasarkan data historis")

# ======================
# KPI CARDS
# ======================
avg_delivery = df["delivery_time_min"].mean()
on_time_rate = (df["delivery_time_min"] <= 30).mean() * 100
peak_delay = df[df["is_peak_hour"] == 1]["delivery_time_min"].mean() - df[df["is_peak_hour"] == 0]["delivery_time_min"].mean()
weather_delay = df[df["is_bad_weather"] == 1]["delivery_time_min"].mean() - df[df["is_bad_weather"] == 0]["delivery_time_min"].mean()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Avg Delivery Time", f"{avg_delivery:.1f} min")
col2.metric("On-Time Rate (≤30 min)", f"{on_time_rate:.1f}%")
col3.metric("Extra Delay at Peak Hour", f"+{peak_delay:.1f} min")
col4.metric("Extra Delay Bad Weather", f"+{weather_delay:.1f} min")

# ======================
# CHARTS
# ======================
st.subheader("📊 Visualisasi")

# 1. Tren rata-rata waktu pengiriman
df["order_id"] = range(1, len(df) + 1)  # dummy index
df_trend = df.groupby(df["order_id"] // 50)["delivery_time_min"].mean()  # rata2 tiap 50 order

fig1, ax1 = plt.subplots(figsize=(7,3))
ax1.plot(df_trend.index, df_trend.values, marker="o")
ax1.set_title("Tren Rata-rata Delivery Time per Batch Order")
ax1.set_xlabel("Batch Order (50 order)")
ax1.set_ylabel("Avg Delivery Time (min)")
st.pyplot(fig1)

# 2. Perbandingan peak vs non-peak
fig2, ax2 = plt.subplots(figsize=(5,3))
df.groupby("is_peak_hour")["delivery_time_min"].mean().plot(kind="bar", ax=ax2, color=["skyblue","orange"])
ax2.set_title("Avg Delivery Time: Peak vs Non-Peak")
ax2.set_ylabel("Minutes")
ax2.set_xticklabels(["Non-Peak", "Peak"], rotation=0)
st.pyplot(fig2)

# 3. Perbandingan cuaca
fig3, ax3 = plt.subplots(figsize=(5,3))
df.groupby("is_bad_weather")["delivery_time_min"].mean().plot(kind="bar", ax=ax3, color=["green","red"])
ax3.set_title("Avg Delivery Time: Good vs Bad Weather")
ax3.set_ylabel("Minutes")
ax3.set_xticklabels(["Good Weather", "Bad Weather"], rotation=0)
st.pyplot(fig3)

# 4. Distribusi kendaraan
if "vehicle_type_Car" in df.columns:
    vehicle_counts = {
        "Car": df["vehicle_type_Car"].sum(),
        "Scooter": df["vehicle_type_Scooter"].sum(),
        "Bike": df["vehicle_type_Bike"].sum() if "vehicle_type_Bike" in df.columns else 0
    }
    fig4, ax4 = plt.subplots(figsize=(4,4))
    ax4.pie(vehicle_counts.values(), labels=vehicle_counts.keys(), autopct="%1.1f%%", startangle=90)
    ax4.set_title("Distribusi Kendaraan Kurir")
    st.pyplot(fig4)

# ======================
# INSIGHT & REKOMENDASI
# ======================
st.subheader("🔍 Insight & Rekomendasi Bisnis")

insight_text = f"""
1. *Waktu Pengiriman Rata-rata*  
   - Rata-rata waktu antar adalah *{avg_delivery:.1f} menit*.  
   - {on_time_rate:.1f}% order selesai dalam 30 menit → cukup baik, tapi masih ada ruang untuk perbaikan.

2. *Pengaruh Jam Sibuk (Peak Hour)*  
   - Saat jam sibuk, waktu antar bertambah rata-rata *+{peak_delay:.1f} menit*.  
   - Ini bisa menurunkan kepuasan pelanggan.

3. *Pengaruh Cuaca Buruk*  
   - Cuaca buruk menambah waktu antar rata-rata *+{weather_delay:.1f} menit*.  
   - Risiko keterlambatan meningkat signifikan pada kondisi hujan/storm.

4. *Jenis Kendaraan*  
   - Distribusi kendaraan kurir menunjukkan mayoritas menggunakan *Car/Scooter*.  
   - Pemilihan kendaraan berhubungan dengan kecepatan antar terutama di area padat lalu lintas.
"""

rekomendasi_text = """
💡 *Rekomendasi Bisnis*  
- Tambahkan insentif kurir saat *jam sibuk* untuk menjaga kecepatan antar.  
- Sediakan *backup kurir* atau fleksibilitas rute saat *cuaca buruk*.  
- Evaluasi efisiensi *jenis kendaraan*: motor/scooter mungkin lebih cepat di pusat kota padat.  
- Targetkan peningkatan on-time delivery ke *90%+* untuk meningkatkan kepuasan pelanggan.  
"""

st.info(insight_text)
st.success(rekomendasi_text)



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

# ======================
# HEADER
# ======================
st.title("🚴 Food Delivery Performance Dashboard")
st.caption("Analisis Faktor yang Mempengaruhi Keterlambatan Pengiriman")

# ======================
# KPI CARDS
# ======================
avg_delivery = df["delivery_time_min"].mean()
on_time_rate = (df["delivery_time_min"] <= 30).mean() * 100
peak_delay = df[df["is_peak_hour"] == 1]["delivery_time_min"].mean() - df[df["is_peak_hour"] == 0]["delivery_time_min"].mean()
weather_delay = df[df["is_bad_weather"] == 1]["delivery_time_min"].mean() - df[df["is_bad_weather"] == 0]["delivery_time_min"].mean()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Avg Delivery Time", f"{avg_delivery:.1f} min")

# highlight merah kalau jauh dari benchmark
target_on_time = 85
delta_on_time = on_time_rate - target_on_time
col2.metric("On-Time Rate (≤30 min)", f"{on_time_rate:.1f}%", f"{delta_on_time:.1f}%", delta_color="normal")

col3.metric("Extra Delay at Peak Hour", f"+{peak_delay:.1f} min")
col4.metric("Extra Delay Bad Weather", f"+{weather_delay:.1f} min")

# ======================
# CHARTS
# ======================
st.subheader("📊 Visualisasi")

col1, col2 = st.columns(2)

# 1. Tren rata-rata waktu pengiriman
with col1:
    df["order_id"] = range(1, len(df) + 1)
    df_trend = df.groupby(df["order_id"] // 50)["delivery_time_min"].mean()
    overall_avg = df["delivery_time_min"].mean()

    fig1, ax1 = plt.subplots(figsize=(5,3))
    ax1.plot(df_trend.index, df_trend.values, marker="o")
    ax1.axhline(overall_avg, color="red", linestyle="--", label=f"Avg {overall_avg:.1f} min")
    ax1.set_title("Tren Rata-rata Delivery Time")
    ax1.set_xlabel("Batch Order (50)")
    ax1.set_ylabel("Minutes")
    ax1.legend()
    plt.tight_layout()
    st.pyplot(fig1)

# 2. Peak vs Non-Peak
with col2:
    fig2, ax2 = plt.subplots(figsize=(5,3))
    df.groupby("is_peak_hour")["delivery_time_min"].mean().plot(
        kind="bar", ax=ax2, color=["skyblue","orange"])
    ax2.set_title("Avg Delivery: Peak vs Non-Peak")
    ax2.set_ylabel("Minutes")
    ax2.set_xticklabels(["Non-Peak", "Peak"], rotation=0)
    plt.tight_layout()
    st.pyplot(fig2)

col3, col4 = st.columns(2)

# 3. Good vs Bad Weather
with col3:
    fig3, ax3 = plt.subplots(figsize=(5,3))
    df.groupby("is_bad_weather")["delivery_time_min"].mean().plot(
        kind="bar", ax=ax3, color=["green","red"])
    ax3.set_title("Avg Delivery: Good vs Bad Weather")
    ax3.set_ylabel("Minutes")
    ax3.set_xticklabels(["Good Weather", "Bad Weather"], rotation=0)
    plt.tight_layout()
    st.pyplot(fig3)

# 4. Distribusi Kendaraan
with col4:
    vehicle_cols = [c for c in df.columns if c.startswith("vehicle_type_")]
    if vehicle_cols:
        vehicle_counts = df[vehicle_cols].sum().to_dict()
        vehicle_counts = {k.replace("vehicle_type_", ""): v for k, v in vehicle_counts.items()}

        fig4, ax4 = plt.subplots(figsize=(4,3))
        ax4.pie(vehicle_counts.values(),
                labels=vehicle_counts.keys(),
                autopct="%1.1f%%", 
                startangle=90,
                colors=["#1f77b4","#ff7f0e","#2ca02c","#d62728","#9467bd"])
        ax4.set_title("Distribusi Kendaraan")
        plt.tight_layout()
        st.pyplot(fig4)

        # insight singkat
        dom_vehicle = max(vehicle_counts, key=vehicle_counts.get)
        dom_pct = (vehicle_counts[dom_vehicle] / sum(vehicle_counts.values())) * 100
        st.caption(f"ℹ {dom_vehicle} dominan ({dom_pct:.1f}%), cocok untuk area padat.")
    else:
        st.info("Kolom jenis kendaraan tidak tersedia di dataset.")

# ======================
# INSIGHT & REKOMENDASI
# ======================
st.subheader("🔍 Insight & Rekomendasi Bisnis")

insight_text = f"""
1. Waktu Pengiriman Rata-rata  
   - Rata-rata waktu antar adalah {avg_delivery:.1f} menit.  
   - On-time delivery hanya {on_time_rate:.1f}% (target industri >{target_on_time}%).  
   - ⚠ Kinerja jauh di bawah benchmark, perlu prioritas perbaikan.

2. Pengaruh Jam Sibuk (Peak Hour)  
   - Saat jam sibuk, waktu antar bertambah rata-rata +{peak_delay:.1f} menit.  
   - Ini bisa menurunkan kepuasan pelanggan terutama di kota besar.

3. Pengaruh Cuaca Buruk  
   - Cuaca buruk menambah waktu antar rata-rata +{weather_delay:.1f} menit.  
   - Risiko keterlambatan meningkat signifikan pada kondisi hujan/storm.

4. Jenis Kendaraan  
   - Distribusi kendaraan menunjukkan dominasi kendaraan tertentu.  
   - Hal ini berhubungan dengan efisiensi di area padat lalu lintas.
"""

rekomendasi_text = """
💡 Rekomendasi Bisnis  
- Tambahkan insentif kurir saat jam sibuk untuk menjaga kecepatan antar.  
- Sediakan backup kurir atau fleksibilitas rute saat cuaca buruk.  
- Evaluasi efisiensi jenis kendaraan: motor/scooter mungkin lebih cepat di pusat kota padat.  
- Tetapkan program peningkatan on-time delivery ke 90%+ sebagai target KPI utama.  
"""

st.info(insight_text)
st.success(rekomendasi_text)

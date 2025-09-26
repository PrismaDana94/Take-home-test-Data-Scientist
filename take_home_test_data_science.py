# =========================================
# Food Delivery –  Dashboard
# =========================================
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# =========================================
# Load Data
# =========================================
st.set_page_config(page_title="🚴 Food Delivery Dashboard", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("food_delivery_times_clean.csv")
    return df

df = load_data()

# =========================================
# Judul
# =========================================
st.title("🚴 Food Delivery – Exploratory Dashboard")
st.markdown("""
Dashboard ini menampilkan analisis data pengiriman makanan berdasarkan faktor jarak, waktu persiapan,
pengalaman kurir, kondisi cuaca, jam sibuk, dan tipe kendaraan.
""")

# =========================================
# Data Preview
# =========================================
st.subheader("📌 Data Preview")
st.dataframe(df.head())

st.markdown(f"*Jumlah baris:* {df.shape[0]} | *Jumlah kolom:* {df.shape[1]}")

# =========================================
# Statistik Deskriptif
# =========================================
st.subheader("📊 Statistik Deskriptif")
st.write(df[['distance_km','preparation_time_min','courier_experience_yrs','delivery_time_min']].describe())

# =========================================
# Korelasi Heatmap
# =========================================
st.subheader("🔗 Korelasi Antar Fitur Numerik")

num_cols = ['distance_km','preparation_time_min','courier_experience_yrs',
            'delivery_time_min','prep_per_km','delivery_speed','effective_distance']

corr = df[num_cols].corr()

fig, ax = plt.subplots(figsize=(8,6))
sns.heatmap(corr, annot=True, cmap="YlGnBu", fmt=".2f", ax=ax)
ax.set_title("Correlation Heatmap", fontsize=14, fontweight="bold")
st.pyplot(fig)

st.markdown("""
*Insight Korelasi:*
- distance_km berkorelasi positif cukup kuat dengan delivery_time_min → semakin jauh jarak, makin lama waktu antar.  
- delivery_speed berkorelasi negatif dengan delivery_time_min → semakin cepat kurir, makin singkat waktu antar.  
- preparation_time_min juga berkontribusi signifikan terhadap total waktu antar.
""")

# =========================================
# Boxplot – Peak Hour
# =========================================
st.subheader("⏰ Analisis Peak Hour vs Delivery Time")

fig1, ax1 = plt.subplots(figsize=(5,4))
sns.boxplot(x="is_peak_hour", y="delivery_time_min", data=df, palette="Set2", ax=ax1)
ax1.set_xticklabels(["Non-Peak", "Peak"])
ax1.set_xlabel("Peak Hour")
ax1.set_ylabel("Delivery Time (min)")
ax1.set_title("Delivery Time by Peak Hour")
st.pyplot(fig1)

st.info("""
📌 *Insight:* Waktu pengantaran saat peak hour cenderung lebih lama (median lebih tinggi).
👉 *Rekomendasi:* Tambah jumlah kurir atau batasi order di jam sibuk untuk menekan delay.
""")

# =========================================
# Boxplot – Cuaca
# =========================================
st.subheader("🌦 Analisis Cuaca vs Delivery Time")

fig2, ax2 = plt.subplots(figsize=(5,4))
sns.boxplot(x="is_bad_weather", y="delivery_time_min", data=df, palette="coolwarm", ax=ax2)
ax2.set_xticklabels(["Good Weather","Bad Weather"])
ax2.set_xlabel("Weather")
ax2.set_ylabel("Delivery Time (min)")
ax2.set_title("Delivery Time by Weather Condition")
st.pyplot(fig2)

st.info("""
📌 *Insight:* Kondisi cuaca buruk meningkatkan variasi dan median waktu antar.  
👉 *Rekomendasi:* Berikan estimasi waktu lebih panjang ke pelanggan saat cuaca buruk, 
atau insentif ekstra ke kurir agar lebih termotivasi.
""")

# =========================================
# Boxplot – Vehicle Type
# =========================================
st.subheader("🚗 Analisis Tipe Kendaraan vs Delivery Time")

if "vehicle_type_Car" in df.columns:
    df['vehicle_type'] = df[['vehicle_type_Car','vehicle_type_Scooter']].idxmax(axis=1)
    df['vehicle_type'] = df['vehicle_type'].str.replace("vehicle_type_", "")
else:
    df['vehicle_type'] = "Unknown"

fig3, ax3 = plt.subplots(figsize=(5,4))
sns.boxplot(x="vehicle_type", y="delivery_time_min", data=df, palette="pastel", ax=ax3)
ax3.set_xlabel("Vehicle Type")
ax3.set_ylabel("Delivery Time (min)")
ax3.set_title("Delivery Time by Vehicle Type")
st.pyplot(fig3)

st.info("""
📌 *Insight:* Scooter umumnya lebih cepat daripada mobil untuk jarak dekat.  
*Rekomendasi:* Gunakan scooter di area padat lalu lintas, dan mobil untuk order besar/jarak jauh.
""")

# =========================================
# Kesimpulan
# =========================================
st.subheader("📌 Insights & Rekomendasi Akhir")
st.success("""
1. *Jarak & Kecepatan* → Faktor utama memengaruhi waktu pengiriman.  
    Atur alokasi kurir berdasarkan jarak order untuk optimasi waktu.  

2. *Jam Sibuk (Peak Hour)* → Membuat delivery lebih lama.  
    Tambah kapasitas kurir atau berikan estimasi lebih panjang saat peak hour.  

3. *Cuaca Buruk* → Menambah keterlambatan signifikan.  
    Terapkan dynamic ETA (perkiraan waktu) & insentif ke kurir.  

4. *Tipe Kendaraan* → Scooter lebih efisien di area perkotaan.  
    Optimalkan kombinasi scooter & mobil sesuai area dan jarak.
""")




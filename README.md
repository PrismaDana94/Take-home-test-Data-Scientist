# Take-home Test – Data Scientist (Food Delivery Times)

[![Streamlit App](https://img.shields.io/badge/Streamlit-Live%20Demo-brightgreen)](https://take-home-test-data-scientist.streamlit.app/)

## 📌 Project Overview

Proyek ini berfokus pada **analisis keterlambatan pengiriman makanan** serta pembuatan **dashboard interaktif dengan Streamlit** untuk memprediksi risiko keterlambatan.  
Tujuan utama adalah memahami faktor-faktor yang memengaruhi ketepatan waktu pengiriman dan memberikan rekomendasi bisnis untuk meningkatkan kepuasan pelanggan sekaligus efisiensi operasional.

---

## 📊 Dataset
Dataset yang digunakan:  
[`food_delivery_times_clean.csv`](./food_delivery_times_clean.csv)

Beberapa kolom penting:
- `distance_km` → jarak pengiriman  
- `delivery_speed` → kecepatan kurir  
- `effective_distance` → kombinasi rute/efektivitas jarak  
- `preparation_time_min` → waktu persiapan vendor  
- `weather_condition` → kondisi cuaca (Clear, Rainy, Snowy, dll.)  

---

## 🚀 Dashboard Workflow
1. **Data Loading** → membaca dataset pengiriman makanan.  
2. **EDA (Exploratory Data Analysis)** → analisis faktor utama penyebab keterlambatan.  
3. **Modeling** → membangun model prediktif menggunakan **XGBoost**.  
4. **Prediction & Risk Scoring** → menghitung probabilitas risiko keterlambatan.  
5. **Dashboard Output** → visualisasi interaktif (tabel, grafik, metrik) serta ringkasan insights.  

---

## 📈 Key Insights
- Faktor paling berpengaruh: **jarak pengiriman, kecepatan kurir, rute efektif, dan persiapan vendor**.  
- **Cuaca buruk** terbukti meningkatkan risiko keterlambatan.  
- Model **XGBoost** terbukti akurat dalam memprediksi risiko keterlambatan.  

---

## 💡 Business Impact
- **Reduksi Delay**: signifikan dengan optimasi rute, insentif kurir, dan monitoring vendor.  
- **Kepuasan Pelanggan**: meningkat dengan estimasi waktu pengiriman yang lebih akurat.  
- **Efisiensi Biaya**: melalui strategi zonasi gudang dan kurir berpengalaman.  

---

## ✅ Business Recommendations
- Terapkan **zonasi tarif/gudang baru** di area dengan permintaan tinggi.  
- Gunakan **optimasi rute & tracking berbasis teknologi maps**.  
- Buat aturan jelas untuk **vendor** (misalnya batas maksimal waktu persiapan).  
- Adakan **pelatihan rutin untuk kurir** agar lebih cepat & konsisten.  
- Implementasikan **notifikasi real-time** ke pelanggan saat cuaca buruk.  

---

## 🛠️ Tech Stack
- Python (Pandas, NumPy, Matplotlib, Seaborn, Scikit-learn, XGBoost)  
- Streamlit – dashboard interaktif  
- GitHub – version control & deployment  

---

## 📂 Main Files
- `food_delivery_times_clean.csv` – dataset yang digunakan  
- `take_home_test_data_science.py` – script analisis & Streamlit dashboard  
- `requirements.txt` – daftar library yang digunakan  

---

## 📬 Author
👤 **Prisma Dana**  
- 💼 LinkedIn: [my_linkedin](https://www.linkedin.com/in/prisma-dana/)  
- 🐙 GitHub: [PrismaDana94](https://github.com/PrismaDana94)

---

✨ Feel free to fork & explore this repo!  
Jika ada pertanyaan atau saran, silakan open issue di repo ini.  

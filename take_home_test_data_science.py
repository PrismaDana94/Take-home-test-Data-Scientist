# take_home_test_data_science_safe.py
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="whitegrid")
st.set_page_config(page_title="Food Delivery Times Dashboard", layout="wide")

@st.cache_data
def load_data(path="food_delivery_times_clean.csv"):
    try:
        return pd.read_csv(path)
    except FileNotFoundError:
        st.error(f"File not found: {path}")
        return None

# ---------------- Load ----------------
st.title("🍽 Food Delivery Times — Dashboard")
st.caption("Interactive dashboard untuk eksplorasi data pengiriman dan identifikasi risiko keterlambatan")

df = load_data()
if df is None:
    st.stop()

# --- Quick debug (hapus kalau sudah oke) ---
with st.expander("DEBUG: Dataset info (hapus jika sudah oke)"):
    st.write("Jumlah baris:", len(df))
    st.write("Columns:", df.columns.tolist())
    st.write(df.dtypes)
    st.dataframe(df.head(5))

# ---------------- helpers ----------------
def find_column(df, candidates):
    cols = list(df.columns)
    for c in candidates:
        if c in cols:
            return c
    cols_lower = {col.lower(): col for col in cols}
    for c in candidates:
        if c.lower() in cols_lower:
            return cols_lower[c.lower()]
    return None

# candidate lists (sesuaikan kalau perlu)
candidates = {
    'distance_km': ['distance_km','distance (km)','distance','dist_km'],
    'delivery_time_min': ['delivery_time_min','delivery_time','delivery_minutes','delivery_min','time_min'],
    'distance_category': ['distance_category','distance_cat','dist_cat','distance_bucket'],
    'weather': ['weather','weather_condition','weather_main'],
    'time_of_day': ['time_of_day','timeofday','period','shift'],
    'vehicle_type': ['vehicle_type','vehicle','transport_mode','vehicle_mode'],
    'prep_per_km': ['prep_per_km','prep_per_km_value'],
    'is_bad_weather': ['is_bad_weather','bad_weather','is_bad']
}

# detect & rename
found = {}
for std_name, cand_list in candidates.items():
    found[std_name] = find_column(df, cand_list)

rename_map = {found[k]: k for k in found if found[k] is not None}
if rename_map:
    df = df.rename(columns=rename_map)

# Check essential columns
essential = ['distance_km', 'delivery_time_min']
missing_essential = [c for c in essential if c not in df.columns]
if missing_essential:
    st.error(f"Missing essential column(s): {missing_essential}. "
             "Silakan rename kolom CSV atau tambahkan mapping kandidat.")
    st.stop()

# If weather exists but not is_bad_weather, create simple flag
if ('weather' in df.columns) and ('is_bad_weather' not in df.columns):
    df['is_bad_weather'] = df['weather'].astype(str).str.contains(
        'rain|storm|snow|thunder|hail', case=False, na=False
    ).astype(int)

# ---------------- Sidebar filters ----------------
st.sidebar.header("Filter Data")

# safe selectbox factory
def safe_selectbox(label, colname):
    if colname in df.columns:
        opts = ["All"] + sorted(df[colname].astype(str).unique().tolist())
        return st.sidebar.selectbox(label, opts, index=0)
    else:
        return "All"

weather_sel = safe_selectbox("Weather", "weather")
dist_cat_sel = safe_selectbox("Distance category", "distance_category")
time_sel = safe_selectbox("Time of day", "time_of_day")
vehicle_sel = safe_selectbox("Vehicle type", "vehicle_type")

min_dist, max_dist = float(df['distance_km'].min()), float(df['distance_km'].max())
dist_range = st.sidebar.slider(
    "Distance (km) range",
    min_value=0.0,
    max_value=float(max_dist),
    value=(min_dist, max_dist),
    step=0.5
)

# ---------------- Apply filters ----------------
df_filtered = df.copy()
if weather_sel != "All" and 'weather' in df.columns:
    df_filtered = df_filtered[df_filtered['weather'].astype(str) == weather_sel]
if dist_cat_sel != "All" and 'distance_category' in df.columns:
    df_filtered = df_filtered[df_filtered['distance_category'].astype(str) == dist_cat_sel]
if time_sel != "All" and 'time_of_day' in df.columns:
    df_filtered = df_filtered[df_filtered['time_of_day'].astype(str) == time_sel]
if vehicle_sel != "All" and 'vehicle_type' in df.columns:
    df_filtered = df_filtered[df_filtered['vehicle_type'].astype(str) == vehicle_sel]

df_filtered = df_filtered[
    (df_filtered['distance_km'] >= dist_range[0]) &
    (df_filtered['distance_km'] <= dist_range[1])
].copy()

# ---------------- KPIs ----------------
st.subheader("Overview")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Orders (filtered)", f"{len(df_filtered):,}")

with col2:
    avg_dt = df_filtered['delivery_time_min'].mean() if not df_filtered.empty else np.nan
    st.metric("Avg Delivery Time (min)", f"{avg_dt:.1f}" if not np.isnan(avg_dt) else "—")

with col3:
    if 'prep_per_km' in df_filtered.columns:
        avg_ppk = df_filtered['prep_per_km'].mean()
        st.metric("Avg Prep per Km", f"{avg_ppk:.2f}")
    else:
        st.write("")

with col4:
    if 'is_bad_weather' in df_filtered.columns:
        pct_bad = (df_filtered['is_bad_weather'].sum() / max(len(df_filtered), 1)) * 100
        st.metric("% Bad Weather", f"{pct_bad:.1f}%")
    else:
        st.write("")

# ---------------- Simple segmentation ----------------
st.subheader("Segmentation: High vs Low Delay Risk (contoh rule-based)")
if 'is_bad_weather' in df_filtered.columns:
    df_filtered.loc[:, 'risk'] = np.where(
        (df_filtered['distance_km'] > 15) | (df_filtered['is_bad_weather'] == 1),
        'High', 'Low'
    )
else:
    df_filtered.loc[:, 'risk'] = np.where(df_filtered['distance_km'] > 15, 'High', 'Low')

if not df_filtered.empty:
    risk_count = df_filtered['risk'].value_counts(normalize=True).mul(100).round(1)
    colA, colB = st.columns(2)
    with colA:
        st.write("Risk distribution (%)")
        st.bar_chart(risk_count)
    with colB:
        high_mean = df_filtered[df_filtered['risk'] == 'High']['delivery_time_min'].mean()
        low_mean = df_filtered[df_filtered['risk'] == 'Low']['delivery_time_min'].mean()
        st.write(f"Avg delivery time — High risk: {high_mean:.1f} min")
        st.write(f"Avg delivery time — Low risk: {low_mean:.1f} min")
        st.write(f"Avg extra delay (High - Low): {high_mean - low_mean:.1f} min")

# ---------------- Visualisasi ----------------
st.subheader("Visualisasi")
if not df_filtered.empty:
    st.markdown("*Distribusi Delivery Time*")
    fig1, ax1 = plt.subplots(figsize=(8, 3))
    sns.histplot(df_filtered['delivery_time_min'].dropna(), bins=30, kde=True, ax=ax1)
    ax1.set_xlabel("Delivery time (min)")
    st.pyplot(fig1)

    if 'weather' in df_filtered.columns:
        st.markdown("*Boxplot: Delivery Time per Weather*")
        fig2, ax2 = plt.subplots(figsize=(8, 3))
        sns.boxplot(x='weather', y='delivery_time_min', data=df_filtered, ax=ax2)
        st.pyplot(fig2)

    if 'distance_category' in df_filtered.columns:
        st.markdown("*Rata-rata Delivery Time per Distance Category*")
        avg_by_cat = df_filtered.groupby('distance_category')['delivery_time_min'].mean().sort_index()
        fig3, ax3 = plt.subplots(figsize=(6, 3))
        avg_by_cat.plot(kind='bar', ax=ax3)
        ax3.set_ylabel("Avg delivery time (min)")
        st.pyplot(fig3)

    st.markdown("*Distance vs Delivery Time (Trend)*")
    if len(df_filtered) > 1:
        sample_n = min(800, len(df_filtered))
        fig4, ax4 = plt.subplots(figsize=(7, 4))
        sns.regplot(
            x='distance_km',
            y='delivery_time_min',
            data=df_filtered.sample(sample_n),
            scatter_kws={'s': 20, 'alpha': 0.5},
            line_kws={'color': 'red'},
            ci=None,
            ax=ax4
        )
        st.pyplot(fig4)
    else:
        st.write("Data terlalu sedikit untuk scatter/regression plot.")

# ---------------- Preview & download ----------------
st.subheader("Preview Data (filtered)")
st.dataframe(df_filtered.reset_index(drop=True).head(200))

csv_bytes = df_filtered.to_csv(index=False).encode('utf-8')
st.download_button(
    label="Download filtered data as CSV",
    data=csv_bytes,
    file_name="food_delivery_times_filtered.csv",
    mime="text/csv"
)

st.markdown("---")
st.markdown("*Notes:*")
st.markdown("- Filter aman meski beberapa kolom tidak ada.")
st.markdown("- Hapus Expander DEBUG setelah konfirmasi kolom.")
st.info("Ready — Jalankan `streamlit run take_home_test_data_science_safe.py`")




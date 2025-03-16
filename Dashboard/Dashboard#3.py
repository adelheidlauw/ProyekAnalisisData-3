import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os 

# ------------------------------
# 📌 Judul Aplikasi
st.title("🌤️ Analisis Polusi Udara - Kota Wanliu 🌧️")

# ------------------------------
# Membaca File
@st.cache_data
def load_data():
    file_path = os.path.join(os.path.dirname(__file__), "PRSA_Data_Wanliu_20130301-20170228.csv")
    Wanliu_df = pd.read_csv(file_path)
    return Wanliu_df

Wanliu_df = load_data()

# ------------------------------
# Sidebar Filter
st.sidebar.header("🔍 Filter Data")
bulan = Wanliu_df['month'].unique()
bulan_dipilih = st.sidebar.multiselect("Pilih Bulan", bulan, default=bulan)
filtered_Wanliu = Wanliu_df[Wanliu_df['month'].isin(bulan_dipilih)]

# ------------------------------
# Menampilkan DataFrame
st.subheader("📌 Dataframe yang Dipilih")

# Membuat expander untuk menampilkan data
with st.expander(" **Dataframe**", expanded=False):
    st.dataframe(filtered_Wanliu)

# Statistik Deskriptif
st.subheader("📌 Statistik Deskriptif")

# Membuat expander
with st.expander("**Rangkuman Parameter Statistik**", expanded=False):
    st.write(filtered_Wanliu.describe())


# ------------------------------
# Exploratory Data Analysis (EDA)
st.subheader("📌 Exploratory Data Analysis (EDA)")

# Visualisasi Distribusi Data
st.write("### Distribusi Data")
fig, axes = plt.subplots(2, 3, figsize=(15, 10))
cols = ['PM2.5', 'PM10', 'TEMP', 'PRES', 'DEWP', 'WSPM']
for ax, col in zip(axes.flatten(), cols):
    sns.histplot(filtered_Wanliu[col], bins=30, kde=True, ax=ax)
    ax.set_title(f'Distribusi {col}')
plt.tight_layout()
st.pyplot(fig)

# Boxplot untuk Outlier
st.write("### Deteksi Outlier dengan Boxplot")
fig, ax = plt.subplots(figsize=(10, 6))
sns.boxplot(data=filtered_Wanliu[cols])
plt.xticks(rotation=45)
plt.title('Boxplot untuk Mendeteksi Outlier')
st.pyplot(fig)

# ------------------------------
# Visualization dan Explanatory Analysis
st.subheader("📌 Visualization dan Explanatory Analysis")

# Analisis Tren Data
st.subheader("📈 Tren Polusi Udara")
st.write("Visualisasi tren rata-rata polusi udara berdasarkan waktu")
fig, ax = plt.subplots(figsize=(12, 6))
pd.to_datetime(filtered_Wanliu['year'].astype(str) + '-' + filtered_Wanliu['month'].astype(str), errors='coerce')
trend_data = filtered_Wanliu.groupby(['year', 'month'])[['PM2.5', 'PM10']].mean().reset_index()
for col in ['PM2.5', 'PM10']:
    ax.plot(trend_data.index, trend_data[col], marker='o', label=col)
ax.set_title("Tren Rata-rata PM2.5 dan PM10")
ax.set_xlabel("Waktu")
ax.set_ylabel("Konsentrasi")
ax.legend()
st.pyplot(fig)

# Membuat expander untuk menampilkan data
with st.expander(" **Kesimpulan**", expanded=False):
    st.write("Terjadinya perubahan musim yang tidak menentu "
    "sepanjang tahun yang disebabkan oleh banyak faktor. PM merupakan "
    "Particulate Matter yang artinya semakin kecil nilainya (partikel "
    "udaranya) semakin berbahaya bagi kesehatan. Tren musiman PM10 "
    "cenderung lebih tinggi dibandingkan dengan PM2.5. "
    "Dengan asumsi musim panas terjadi pada bulan Juni-Agustus, "
    "maka pada musim panas tingkat polusi udara cenderung lebih rendah "
    "dibandingkan pada musim panas, begitu juga sebaliknya ketika musim hujan "
    "tingkat polutannya bertambah.")

# ------------------------------
# Heatmap Korelasi
st.subheader("🔥 Heatmap Korelasi")
st.write("Visualisasi hubungan antar variabel dengan heatmap korelasi")
fig, ax = plt.subplots(figsize=(10, 6))
corr = filtered_Wanliu[cols].corr()
sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5, ax=ax)
st.pyplot(fig)

# Membuat expander untuk menampilkan data
with st.expander(" **Kesimpulan**", expanded=False):
    st.write("""Pengguna dapat menyesuaikan bulan untuk melihat pola polusi berdasarkan musim.
    Berdasarkan heatmap yang dihasilkan dari perhitungan, variabel TEMP (suhu udara) 
    memberikan nilai korelasi negatif yang artinya ketika suhu meningkat, 
    kadar PM2.5 cenderung menurun. Variabel PRES (tekanan udara) dan DEWP (titik embun) 
    tidak memberikan pengaruh besar karena nilainya yang sangat kecil. 
    Variabel RAIN(hujan), memiliki nilai korelasi negatif , sehingga ketika terjadi 
    hujan polusi udara akan menurun. Variabel WSPM(kecepatan angin) memiliki pengaruh 
    terhadap penyebaran polutan PM2.5 ini, semakin besar nilainya atau tinggi kecepatan 
    anginnya konsentrasi PM2.5 semakin rendah polutan akan tersebar luas.Heatmap korelasi 
    memperlihatkan hubungan antara PM2.5, PM10, dan faktor lainnya secara lebih interaktif.
""")
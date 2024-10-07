import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

@st.cache_data
def load_data(dir):
    df = pd.read_csv(dir)
    return df

script_dir = os.path.dirname(os.path.realpath(__file__))
hour_in_day_df = load_data(f'{script_dir}/hour_in_day_df.csv')
monthly_df = load_data(f'{script_dir}/monthly_df.csv')
seasonal_df = load_data(f'{script_dir}/seasonal_df.csv')
weather_cnt = load_data(f'{script_dir}/weather_cnt.csv')
weekly_df = load_data(f'{script_dir}/weekly_df.csv')

seasonal_df['season_'] = seasonal_df['season_'].replace({
    1: "Springer",
    2: "Summer",
    3: "Fall",
    4: "Winter"
})
weather_cnt["weathersit_"] = weather_cnt['weathersit_'].replace({
    1: "Cerah",
    2: "Berawan",
    3: "Hujan Ringan",
    4: "Hujan Lebat"
})

def exponential_smoothing(data, alpha):
    smoothed_data = np.zeros(len(data) + 7)  # Ditambahkan 7 agar memberikan prediksi untuk 7 minggu ke depan
    data = data.tolist() + np.zeros(7).tolist()  # Menggabungkan data asli dengan nol untuk prediksi
    smoothed_data[0] = data[0]  # Nilai pertama menggunakan nilai dari data asli
    for t in range(1, len(data)):
        smoothed_data[t] = (alpha * data[t]) + ((1 - alpha) * smoothed_data[t - 1])
        data[t] = smoothed_data[t]
    return smoothed_data

st.title("Dashboard Analisis Dataset Bike-Sharing")


tab1, tab2, tab3 = st.tabs(["Tren Jumlah Rental Sepeda", "Faktor yang Mempengaruhi Jumlah Rental Sepeda", "Hubungan Cuaca dengan Jumlah Rental Sepeda"])

with tab1:
    st.subheader("Tren Jumlah Rental Sepeda tiap Bulan Periode 2011-2012")
    plt.figure(figsize=(8, 6))
    sns.regplot(x=monthly_df.index, y=monthly_df['cnt_sum'], marker='o', color='b', line_kws={"color": "red"})
    sns.lineplot(x=monthly_df.index, y=monthly_df['cnt_sum'], marker='o', label='Cnt Sum')

    plt.title('Count per Month')
    plt.xlabel('Month')
    plt.ylabel('Count')
    plt.xticks(ticks=monthly_df.index)

    st.pyplot(plt)
    
    st.write("Grafik diatas adalah Jumlah Rental Sepeda Tiap Bulan, sumbu X menunjukkan bulan dan sumbu Y menunjukkan jumlah rental. Terlihat bahwa jumlah penggunaan sepeda meningkat dari awal tahun 2011 hingga pada akhir 2012")
    st.markdown("<br>", unsafe_allow_html=True)  # Jarak antar grafik


    # Diagram eksponensial smoothing
    alpha = 0.1
    smoothed_data = exponential_smoothing(np.array(weekly_df['cnt_mean']), alpha)
    
    plt.figure(figsize=(10, 6))
    plt.plot(weekly_df['cnt_mean'], label='Data Asli')
    plt.plot(smoothed_data, label=f'Exponential Smoothing (Alpha = {alpha})', color='orange')
    plt.title('Exponential Smoothing pada Data Time Series')
    plt.xlabel('Waktu')
    plt.ylabel('Nilai')
    plt.legend()
    plt.tight_layout()
    st.pyplot(plt)  # Menampilkan plot di Streamlit
    st.write("Grafik di atas menunjukkan penerapan metode smoothing eksponensial pada data rental sepeda, dengan alpha = 0.1.")


with tab2: 
    st.subheader("Jumlah Rental Sepeda Pada Hari Kerja dan Non Hari Kerja dalam Rentang 2 Bulanan")

    Bulan = st.selectbox(
        "Rentang Bulan:",
        (
            "Januari - Februari 2011",
            "Maret - April 2011",
            "Mei - Juni 2011",
            "Juli - Agustus 2011",
            "September - Oktober 2011",
            "November - Desember 2011",
            "Januari - Februari 2012",
            "Maret - April 2012",
            "Mei - Juni 2012",
            "Juli - Agustus 2012",
            "September - Oktober 2012",
            "November - Desember 2012",
        )
    )

    multiplier = {
        "Januari - Februari 2011": 1,
        "Maret - April 2011": 2,
        "Mei - Juni 2011": 3,
        "Juli - Agustus 2011": 4,
        "September - Oktober 2011": 5,
        "November - Desember 2011": 6,
        "Januari - Februari 2012": 7,
        "Maret - April 2012": 8,
        "Mei - Juni 2012": 9,
        "Juli - Agustus 2012": 10,
        "September - Oktober 2012": 11,
        "November - Desember 2012": 12,
    }
    x = multiplier[Bulan]

    upperbone = 16 * x
    lowerbone = upperbone - 16

    plt.figure(figsize=(10, 6))
    sns.barplot(x="dteday_", y='cnt_mean', hue='workingday_', data=weekly_df[lowerbone: upperbone])

    plt.title('Average Count per Date Grouped by Working Day')
    plt.xlabel('Date')
    plt.ylabel('Average Count')

    plt.xticks(rotation=45)

    plt.tight_layout()

    st.pyplot(plt)

    st.write("Grafik di atas menunjukkan rata-rata jumlah rental sepeda tiap bulan, sumbu x menunjukkan bulan sedangkan sumbu y menunjukkan rata-rata jumlah rental.")
    st.markdown("<br>", unsafe_allow_html=True)  # Jarak antar grafik

    #============Diagram Kedua======================================

    st.subheader("Jumlah Rental Sepeda Pada Jam-Jam Tertentu di Hari Kerja dan Non Hari Kerja")

    workingday_1 = hour_in_day_df[hour_in_day_df["workingday_"] == 1]
    workingday_0 = hour_in_day_df[hour_in_day_df["workingday_"] == 0]

    plt.figure(figsize=(12, 6))

    sns.barplot(x=workingday_1["hr_"], y=workingday_1["cnt_mean"], color="blue", label="Working Day")
    sns.barplot(x=workingday_0["hr_"], y=-workingday_0["cnt_mean"], color="red", label="Non Working Day")

    plt.title('Average Count per Hour Grouped by Working Day')
    plt.xlabel('Average Count (cnt_mean)')
    plt.ylabel('Hour of Day (hr)')
    plt.axhline(0, color='black', linewidth=3)  
    plt.legend()  
    plt.tight_layout()
    
    st.pyplot(plt)
    
    st.write("Sumbu x pada diagram diatas menunjukkan jam rental dan sumbu Y menunjukkan rerata jumlah rental. Dapat dilihat bahwa pada hari kerja terjadi kenaikan jumlah rental pada pagi hari dan sore hari. Sedangkan pada hari non kerja, jumlah rental tertinggi terjadi pada siang hari")
    st.markdown("<br>", unsafe_allow_html=True)  

    #============Diagram Ketiga======================================

    st.subheader("Jumlah Rental Sepeda Berdasarkan Musim")
    plt.figure(figsize=(10, 6))
    sns.barplot(x="season_", y='cnt_mean', hue='yr_', data=seasonal_df, palette='dark')
    plt.title('Average Count Grouped by Season')
    plt.xlabel('Season')
    plt.ylabel('Average Count')
    plt.tight_layout()
    
    st.pyplot(plt)

    st.write("Terlihat bahwa merental sepeda bukan hal yang menarik pada springer season. (1:springer, 2:summer, 3:fall, 4:winter)")

with tab3:
    st.subheader("Jumlah Rental Sepeda Berdasarkan Cuaca")

    plt.figure(figsize=(10, 6))
    sns.barplot(x='weathersit_', y='cnt_mean', data=weather_cnt)

    plt.title('Average Count Mean by Weather Situation')
    plt.xlabel('Weather Situation')
    plt.ylabel('Count Mean')

    plt.tight_layout()
    st.pyplot(plt)

    st.write("Dapat dilihat bahwa cuaca berdampak pada jumlah pengguna sepeda. orang-orang menggunakan sepeda paling banyak pada cuaca cerah (1), sedangkan paling sedikit menggunakan sepeda pada cuaca hujan lebat(4). (1 = cerah, 2 = berkabut + berawan, 3 = Hujan ringan, 4 = Hujan lebat)")

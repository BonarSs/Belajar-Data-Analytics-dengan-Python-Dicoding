import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
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

st.title("Dashboard Analisis Dataset Bike-Sharing")


tab1, tab2, tab3 = st.tabs(["Tren Jumlah Rental Sepeda", "Faktor yang Mempengaruhi Jumlah Rental Sepeda", "Hubungan Cuaca dengan Jumlah Rental Sepeda"])

with tab1:
    st.subheader("Tren Jumlah Rental Sepeda tiap Bulan Periode 2011-2012")
    # Membuat diagram garis
    plt.figure(figsize=(8, 6))
    sns.regplot(x=monthly_df.index, y=monthly_df['cnt_sum'], marker='o', color='b', line_kws={"color": "red"})
    sns.lineplot(x=monthly_df.index, y=monthly_df['cnt_sum'], marker='o', label='Cnt Sum')

    plt.title('Count per Month')
    plt.xlabel('Month')
    plt.ylabel('Count')
    plt.xticks(ticks=monthly_df.index)

    # Menampilkan grafik di Streamlit
    st.pyplot(plt)
    
    st.write("Grafik diatas adalah Jumlah Rental Sepeda Tiap Bulan, sumbu X menunjukkan bulan dan sumbu Y menunjukkan jumlah rental. Terlihat bahwa jumlah penggunaan sepeda meningkat dari awal tahun 2011 hingga pada akhir 2012")


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

    # Membuat diagram batang
    plt.figure(figsize=(10, 6))
    sns.barplot(x="dteday_", y='cnt_mean', hue='workingday_', data=weekly_df[lowerbone: upperbone])

    plt.title('Average Count per Date Grouped by Working Day')
    plt.xlabel('Date')
    plt.ylabel('Average Count')

    plt.xticks(rotation=45)

    plt.tight_layout()

    # Menampilkan grafik di Streamlit
    st.pyplot(plt)

    st.write("Grafik di atas menunjukkan rata-rata jumlah rental sepeda tiap bulan, sumbu x menunjukkan bulan sedangkan sumbu y menunjukkan rata-rata jumlah rental.")
    st.markdown("<br>", unsafe_allow_html=True)  # Jarak antar grafik

    #============Diagram Kedua======================================

    st.subheader("Jumlah Rental Sepeda Pada Jam-Jam Tertentu di Hari Kerja dan Non Hari Kerja")

    # Menambahkan diagram kedua
    workingday_1 = hour_in_day_df[hour_in_day_df["workingday_"] == 1]
    workingday_0 = hour_in_day_df[hour_in_day_df["workingday_"] == 0]

    plt.figure(figsize=(12, 6))

    sns.barplot(x=workingday_1["hr_"], y=workingday_1["cnt_mean"], color="blue", label="Working Day")
    sns.barplot(x=workingday_0["hr_"], y=-workingday_0["cnt_mean"], color="red", label="Non Working Day")

    plt.title('Average Count per Hour Grouped by Working Day')
    plt.xlabel('Average Count (cnt_mean)')
    plt.ylabel('Hour of Day (hr)')
    plt.axhline(0, color='black', linewidth=3)  # Garis tengah
    plt.legend()  # Menampilkan legenda
    plt.tight_layout()
    
    # Menampilkan grafik kedua di Streamlit
    st.pyplot(plt)
    
    st.write("Sumbu x pada diagram diatas menunjukkan jam rental dan sumbu Y menunjukkan rerata jumlah rental. Dapat dilihat bahwa pada hari kerja terjadi kenaikan jumlah rental pada pagi hari dan sore hari. Sedangkan pada hari non kerja, jumlah rental tertinggi terjadi pada siang hari")
    st.markdown("<br>", unsafe_allow_html=True)  # Jarak antar grafik

    #============Diagram Ketiga======================================

    st.subheader("Jumlah Rental Sepeda Berdasarkan Musim")
    # Menambahkan diagram ketiga
    plt.figure(figsize=(10, 6))
    sns.barplot(x="season_", y='cnt_mean', hue='yr_', data=seasonal_df, palette='dark')
    plt.title('Average Count Grouped by Season')
    plt.xlabel('Season')
    plt.ylabel('Average Count')
    plt.tight_layout()
    
    # Menampilkan grafik ketiga di Streamlit
    st.pyplot(plt)

    st.write("Terlihat bahwa merental sepeda bukan hal yang menarik pada springer season. (1:springer, 2:summer, 3:fall, 4:winter)")

with tab3:
    st.subheader("Jumlah Rental Sepeda Berdasarkan Cuaca")

    # Menambahkan diagram baru ke dalam tab 2
    plt.figure(figsize=(10, 6))
    sns.barplot(x='weathersit_', y='cnt_mean', data=weather_cnt)

    plt.title('Average Count Mean by Weather Situation')
    plt.xlabel('Weather Situation')
    plt.ylabel('Count Mean')

    plt.tight_layout()
    st.pyplot(plt)

    st.write("Dapat dilihat bahwa cuaca berdampak pada jumlah pengguna sepeda. orang-orang menggunakan sepeda paling banyak pada cuaca cerah (1), sedangkan paling sedikit menggunakan sepeda pada cuaca hujan lebat(4). (1 = cerah, 2 = berkabut + berawan, 3 = Hujan ringan, 4 = Hujan lebat)")

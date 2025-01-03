import streamlit as st
import pandas as pd
import altair as alt

# Load datasets
hour_data = pd.read_csv('./hour_cleaned.csv') 
day_data = pd.read_csv('./day_cleaned.csv') 

# Sidebar untuk navigasi
st.sidebar.title("Navigasi")
menu = st.sidebar.radio(
    "Pilih Halaman:",
    ["Pengenalan", "Halaman 1: Musim & Cuaca", "Halaman 2: Kasual vs Terdaftar", 
     "Halaman 3: Pola Jam & Bulan", "Halaman 4: Clustering Manual"]
)

# Pengenalan
if menu == "Pengenalan":
    st.title("Dashboard Analisis Data: Bike Sharing")
    st.write("""
    Dashboard ini memberikan analisis berdasarkan musim, cuaca, tipe pengguna, pola waktu, 
    serta clustering manual untuk mengidentifikasi kelompok tertentu dengan permintaan penyewaan tinggi.
    Anda dapat memfilter data sesuai kebutuhan menggunakan kontrol interaktif.
    """)

# Halaman 1: Musim & Cuaca
elif menu == "Halaman 1: Musim & Cuaca":
    st.title("Analisis Berdasarkan Musim & Cuaca")
    filter_type = st.radio("Filter berdasarkan:", ["Musim", "Cuaca"])
    
    if filter_type == "Musim":
        season_avg = day_data.groupby('season')['cnt'].mean().reset_index()
        season_avg['season'] = season_avg['season'].replace({1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'})
        st.subheader("Rata-rata Penyewaan Berdasarkan Musim")
        chart = alt.Chart(season_avg).mark_bar().encode(
            x=alt.X('season', title='Musim'),
            y=alt.Y('cnt', title='Rata-rata Penyewaan'),
            color='season'
        ).properties(title="Penyewaan Berdasarkan Musim")
        st.altair_chart(chart, use_container_width=True)
        
    elif filter_type == "Cuaca":
        weather_avg = day_data.groupby('weathersit')['cnt'].mean().reset_index()
        weather_avg['weathersit'] = weather_avg['weathersit'].replace({
            1: 'Clear', 2: 'Mist + Cloudy', 3: 'Light Rain/Snow', 4: 'Heavy Rain'
        })
        st.subheader("Rata-rata Penyewaan Berdasarkan Cuaca")
        chart = alt.Chart(weather_avg).mark_bar().encode(
            x=alt.X('weathersit', title='Cuaca'),
            y=alt.Y('cnt', title='Rata-rata Penyewaan'),
            color='weathersit'
        ).properties(title="Penyewaan Berdasarkan Cuaca")
        st.altair_chart(chart, use_container_width=True)

# Halaman 2: Kasual vs Terdaftar
elif menu == "Halaman 2: Kasual vs Terdaftar":
    st.title("Analisis Penggunaan Kasual vs Terdaftar")
    start_hour, end_hour = st.slider("Pilih Waktu (Jam):", min_value=0, max_value=23, value=(0, 23))
    filtered_data = hour_data[(hour_data['hr'] >= start_hour) & (hour_data['hr'] <= end_hour)]
    user_avg = filtered_data.groupby(['workingday']).agg({'casual': 'mean', 'registered': 'mean'}).reset_index()
    user_avg['workingday'] = user_avg['workingday'].replace({0: 'Akhir Pekan', 1: 'Hari Kerja'})
    st.subheader("Pola Penggunaan Berdasarkan Hari Kerja")
    chart = alt.Chart(user_avg).transform_fold(
        ['casual', 'registered'],
        as_=['Tipe Pengguna', 'Rata-rata Penyewaan']
    ).mark_bar().encode(
        x=alt.X('workingday', title='Hari'),
        y=alt.Y('Rata-rata Penyewaan:Q', title='Rata-rata Penyewaan'),
        color='Tipe Pengguna:N'
    ).properties(title="Pola Penggunaan Kasual vs Terdaftar")
    st.altair_chart(chart, use_container_width=True)

# Halaman 3: Pola Jam & Bulan
elif menu == "Halaman 3: Pola Jam & Bulan":
    st.title("Pola Penyewaan Berdasarkan Jam & Bulan")
    start_hour, end_hour = st.slider("Pilih Waktu (Jam):", min_value=0, max_value=23, value=(0, 23))
    filtered_data = hour_data[(hour_data['hr'] >= start_hour) & (hour_data['hr'] <= end_hour)]
    
    hour_avg = filtered_data.groupby('hr')['cnt'].mean().reset_index()
    st.subheader("Distribusi Penyewaan Berdasarkan Jam")
    chart = alt.Chart(hour_avg).mark_line(point=True).encode(
        x=alt.X('hr', title='Jam'),
        y=alt.Y('cnt', title='Rata-rata Penyewaan')
    ).properties(title="Distribusi Penyewaan Berdasarkan Jam")
    st.altair_chart(chart, use_container_width=True)

    month_avg = filtered_data.groupby('mnth')['cnt'].mean().reset_index()
    month_avg['mnth'] = month_avg['mnth'].replace({1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 
                                                    7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'})
    st.subheader("Distribusi Penyewaan Berdasarkan Bulan")
    chart = alt.Chart(month_avg).mark_line(point=True).encode(
        x=alt.X('mnth', title='Bulan'),
        y=alt.Y('cnt', title='Rata-rata Penyewaan')
    ).properties(title="Distribusi Penyewaan Berdasarkan Bulan")
    st.altair_chart(chart, use_container_width=True)

# Halaman 4: Clustering Manual
elif menu == "Halaman 4: Clustering Manual":
    st.title("Analisis Clustering Manual")
    
    # Pilihan cluster jam
    hour_cluster = st.selectbox("Pilih Cluster Jam:", hour_data['hour_cluster'].unique())
    filtered_hour_cluster = hour_data[hour_data['hour_cluster'] == hour_cluster]
    st.subheader(f"Tabel Transaksi untuk Cluster Jam: {hour_cluster}")
    st.write(filtered_hour_cluster[['casual', 'registered', 'cnt']])  # Hanya menampilkan kolom kasual, terdaftar, dan total

    # Pilihan cluster bulan
    month_cluster = st.selectbox("Pilih Cluster Bulan:", day_data['month_cluster'].unique())
    filtered_month_cluster = day_data[day_data['month_cluster'] == month_cluster]
    st.subheader(f"Tabel Transaksi untuk Cluster Bulan: {month_cluster}")
    st.write(filtered_month_cluster[['casual', 'registered', 'cnt']])  # Hanya menampilkan kolom kasual, terdaftar, dan total

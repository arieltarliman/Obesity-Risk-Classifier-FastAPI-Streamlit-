import streamlit as st
import requests
import json

# Konfigurasi halaman
st.set_page_config(
    page_title="Prediksi Tingkat Obesitas",
    page_icon="🤖",
    layout="centered"
)

# Judul aplikasi
st.title("🤖 Prediksi Tingkat Obesitas")

# URL dari backend FastAPI 
API_URL = "http://127.0.0.1:8000/predict"

# Membuat form untuk input pengguna
with st.form("prediction_form"):
    st.header("Masukkan data Anda:")

    # Buat 2 kolom agar lebih rapi
    col1, col2 = st.columns(2)

    with col1:
        # Input untuk 8 fitur yang dipilih oleh model 'lite'
        Age = st.number_input("Usia (Tahun)", min_value=1, max_value=100, value=25)
        
        # Minta input Tinggi dalam cm untuk kemudahan pengguna
        Height_cm = st.number_input("Tinggi Badan (cm)", min_value=100, max_value=300, value=170)
        
        Weight = st.number_input("Berat Badan (kg)", min_value=20.0, max_value=500.0, value=70.0, step=0.1)
        TUE = st.number_input("Waktu Penggunaan Teknologi (jam/hari)", min_value=0.0, max_value=24.0, value=2.0, step=0.5)
        
    with col2:
        Gender = st.selectbox("Jenis Kelamin", ("Male", "Female"))
        FAVC = st.selectbox("Sering Konsumsi Makanan Kalori Tinggi?", ("Yes", "No"))
        SMOKE = st.selectbox("Apakah Anda Merokok?", ("Yes", "No"))
        MTRANS = st.selectbox("Transportasi Utama", ('Public_Transportation', 'Automobile', 'Walking', 'Motorbike', 'Bike'))

    # Tombol submit form
    submitted = st.form_submit_button("Prediksi Sekarang")


# Logika setelah tombol submit ditekan
if submitted:
    # 1. Konversi tinggi dari cm ke meter
    if Height_cm > 0:
        Height_m = Height_cm / 100
        
        # 2. Lakukan kalkulasi BMI
        bmi_calculated = Weight / (Height_m ** 2)
        
        # 3. Tampilkan BMI yang dihitung kepada pengguna
        st.info(f"BMI Anda yang dihitung: **{bmi_calculated:.2f}**")
        
        # 4. Siapkan data input untuk dikirim ke API, gunakan BMI yang sudah dihitung
        input_data = {
            "Age": Age,
            "Gender": Gender,
            "Weight": Weight,
            "BMI": bmi_calculated, 
            "FAVC": FAVC,
            "TUE": TUE,
            "SMOKE": SMOKE,
            "MTRANS": MTRANS
        }

        # Kirim request POST ke API
        try:
            with st.spinner('Memproses prediksi...'):
                response = requests.post(API_URL, json=input_data)
            
            # Cek apakah request berhasil
            if response.status_code == 200:
                result = response.json()
                prediction = result['prediction']
                
                st.success(f"**Hasil Prediksi: Anda tergolong dalam kategori `{prediction}`**")
                st.balloons()
            else:
                st.error(f"Error: Gagal mendapatkan prediksi. Status code: {response.status_code}")
                st.json(response.json())
                
        except requests.exceptions.RequestException as e:
            st.error(f"Gagal terhubung ke server backend. Pastikan server FastAPI (main.py) sudah berjalan. Detail: {e}")
    else:
        st.error("Tinggi badan harus lebih dari 0 cm.")
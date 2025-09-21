import pickle
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

# Inisialisasi aplikasi FastAPI
app = FastAPI()

# 1. Muat model 'lite' yang sudah dilatih
# Pastikan file .pkl berada di direktori yang sama
with open('obesity_model_lite.pkl', 'rb') as f:
    model = pickle.load(f)

# 2. Definisikan struktur input menggunakan Pydantic
# Ini adalah input yang akan diisi oleh pengguna di frontend.
# Tipe datanya harus sesuai dengan apa yang akan dikirim dari Streamlit.
class ObesityInput(BaseModel):
    Age: int
    Gender: str  # "Male" atau "Female"
    Weight: float
    BMI: float
    FAVC: str    # "Yes" atau "No"
    TUE: float   # Waktu penggunaan teknologi (0-2)
    SMOKE: str   # "Yes" atau "No"
    MTRANS: str  # Transportasi utama

# 3. Definisikan mapping untuk mengubah input teks menjadi angka
# Ini harus SAMA PERSIS dengan mapping saat Anda melatih model
gender_map = {'Female': 0, 'Male': 1}
yes_no_map = {'Yes': 1, 'No': 0}

# Mapping untuk hasil prediksi (angka -> teks)
inverse_target_map = {
    0: 'Insufficient_Weight', 1: 'Normal_Weight', 2: 'Overweight_Level_I',
    3: 'Overweight_Level_II', 4: 'Obesity_Type_I', 5: 'Obesity_Type_II',
    6: 'Obesity_Type_III'
}

# 4. Buat endpoint untuk prediksi
@app.post("/predict")
def predict_obesity(data: ObesityInput):
    # Buat dictionary dari data input
    input_data = data.dict()

    # --- Lakukan transformasi/encoding seperti saat training ---
    # Ubah input teks menjadi angka
    gender_numeric = gender_map[input_data['Gender']]
    favc_numeric = yes_no_map[input_data['FAVC']]
    smoke_numeric = yes_no_map[input_data['SMOKE']]
    
    # Handle One-Hot Encoding untuk MTRANS
    # Model 'lite' Anda hanya butuh 'MTRANS_Public_Transportation'
    mtrans_public_transport_numeric = 1 if input_data['MTRANS'] == 'Public_Transportation' else 0

    # Susun fitur dalam bentuk DataFrame SESUAI URUTAN saat training model lite
    feature_order = ['BMI', 'Gender', 'Age', 'Weight', 'TUE', 'FAVC', 'SMOKE', 'MTRANS_Public_Transportation']
    
    df = pd.DataFrame([{
        'BMI': input_data['BMI'],
        'Gender': gender_numeric,
        'Age': input_data['Age'],
        'Weight': input_data['Weight'],
        'TUE': input_data['TUE'],
        'FAVC': favc_numeric,
        'SMOKE': smoke_numeric,
        'MTRANS_Public_Transportation': mtrans_public_transport_numeric
    }])[feature_order] # Pastikan urutan kolomnya benar

    # Lakukan prediksi
    prediction_numeric = model.predict(df)[0]
    
    # Ubah hasil prediksi numerik kembali ke label teks
    prediction_label = inverse_target_map.get(prediction_numeric, "Unknown")

    # Kembalikan hasil prediksi
    return {"prediction": prediction_label}

# Perintah untuk menjalankan server (opsional, untuk kemudahan)
if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
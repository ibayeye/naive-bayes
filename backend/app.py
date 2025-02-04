from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
import joblib


app = Flask(__name__)

# Load model dan scaler yang sudah dilatih sebelumnya
try:
    model = joblib.load("model_naive_bayes_enhanced.pkl")
    scaler = joblib.load("scaler_enhanced.pkl")
except:
    print("Error: Model atau scaler tidak ditemukan. Pastikan file .pkl sudah ada.")

# Mapping untuk nilai kategorikal
mappings = {
    "penghasilan": {"Rendah": 0, "Sedang": 1, "Tinggi": 2},
    "jarak": {"Dekat": 0, "Jauh": 1},
    "organisasi": {"Tidak": 0, "Ikut": 1},
    "ukm": {"Tidak": 0, "Ikut": 1},
    "gender": {"L": 0, "P": 1}
}
cors = CORS(app)
@cross_origin()
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Ambil data dari request
        data = request.get_json()

        # Validasi input yang diperlukan
        required_fields = [
            "IPK", "Penghasilan", "Tanggungan", 
            "Jarak", "Organisasi", "UKM", 
            "JenisKelamin", "SKS"
        ]
        
        for field in required_fields:
            if field not in data:
                return jsonify({
                    "error": f"Missing required field: {field}",
                    "required_fields": required_fields
                }), 400

        # Konversi data ke format yang sesuai
        processed_data = {
            "IPK": float(data["IPK"]),
            "Penghasilan": mappings["penghasilan"].get(data["Penghasilan"]),
            "Tanggungan": int(data["Tanggungan"]),
            "Jarak Tempat Tinggal kekampus (Km)": mappings["jarak"].get(data["Jarak"]),
            "Ikut Organisasi": mappings["organisasi"].get(data["Organisasi"]),
            "Ikut UKM": mappings["ukm"].get(data["UKM"]),
            "Jenis Kelamin": mappings["gender"].get(data["JenisKelamin"]),
            "SKS": int(data["SKS"])
        }

        # Validasi nilai-nilai yang dikonversi
        if None in processed_data.values():
            invalid_fields = [k for k, v in processed_data.items() if v is None]
            return jsonify({
                "error": "Invalid value(s) in input",
                "invalid_fields": invalid_fields,
                "valid_values": {
                    "Penghasilan": list(mappings["penghasilan"].keys()),
                    "Jarak": list(mappings["jarak"].keys()),
                    "Organisasi": list(mappings["organisasi"].keys()),
                    "UKM": list(mappings["ukm"].keys()),
                    "JenisKelamin": list(mappings["gender"].keys())
                }
            }), 400

        # Konversi ke DataFrame dengan urutan kolom yang sama seperti training
        df = pd.DataFrame([processed_data])

        # Skalakan fitur menggunakan scaler yang sama dengan training
        X_scaled = scaler.transform(df)

        # Lakukan prediksi
        prediction = model.predict(X_scaled)
        probabilities = model.predict_proba(X_scaled)

        # Format hasil prediksi
        result = {
            "prediction": "Menerima Beasiswa" if prediction[0] == 1 else "Tidak Menerima Beasiswa",
            "prediction_code": int(prediction[0]),
            "probability": {
                "Tidak Menerima Beasiswa": float(probabilities[0][0]),
                "Menerima Beasiswa": float(probabilities[0][1])
            },
            "input_data": {
                "IPK": data["IPK"],
                "Penghasilan": data["Penghasilan"],
                "Tanggungan": data["Tanggungan"],
                "Jarak": data["Jarak"],
                "Organisasi": data["Organisasi"],
                "UKM": data["UKM"],
                "Jenis Kelamin": data["JenisKelamin"],
                "SKS": data["SKS"]
            }
        }

        return jsonify(result)

    except Exception as e:
        return jsonify({
            "error": str(e),
            "message": "Terjadi kesalahan dalam pemrosesan data"
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
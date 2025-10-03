import os
import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS # Pastikan Anda sudah install: pip install Flask-Cors
from dotenv import load_dotenv
import replicate

# --- Konfigurasi Awal ---
load_dotenv()
app = Flask(__name__)
CORS(app)
# Mengizinkan permintaan dari frontend Next.js Anda
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

# --- Memproses Data Latihan ---
try:
    df_latihan = pd.read_csv('cleaned_megaGymDataset.csv')
    # Membersihkan nilai kosong (NaN) dan menggantinya dengan string kosong
    df_latihan.fillna('', inplace=True)
    workouts_list = df_latihan.to_dict(orient='records')
    print("✅ Dataset latihan berhasil dimuat dan dibersihkan.")
except FileNotFoundError:
    df_latihan = None
    workouts_list = []
    print("❌ ERROR: cleaned_megaGymDataset.csv not found.")

# --- Memproses Data Makanan ---
try:
    df_makanan = pd.read_csv('daily_food_nutrition_dataset.csv')
    df_makanan.columns = df_makanan.columns.str.strip()
    # Membersihkan nilai kosong (NaN) dan menggantinya dengan 0 untuk data numerik
    df_makanan.fillna(0, inplace=True)
    
    unique_foods = df_makanan.groupby('Food_Item').agg({
        'Calories (kcal)': 'mean', 'Protein (g)': 'mean',
        'Carbohydrates (g)': 'mean', 'Fat (g)': 'mean', 'Category': 'first'
    }).reset_index().round(1)
    foods_list = unique_foods.to_dict(orient='records')
    print(f"✅ Dataset makanan berhasil diproses. Ditemukan {len(foods_list)} item unik.")
except FileNotFoundError:
    df_makanan = None
    unique_foods = None
    foods_list = []
    print("❌ ERROR: daily_food_nutrition_dataset.csv not found.")


# --- Fungsi Pencarian (RAG) ---
def cari_info_latihan(pertanyaan_user: str) -> str:
    if df_latihan is None: return ""
    kata_kunci = pertanyaan_user.lower()
    hasil = df_latihan[df_latihan['Title'].str.lower().str.contains(kata_kunci)]
    if hasil.empty: return ""
    
    konteks = "Info Latihan:\n"
    for _, baris in hasil.head(2).iterrows():
        konteks += f"- {baris['combined_text']}\n"
    return konteks

def cari_info_makanan(pertanyaan_user: str) -> str:
    if unique_foods is None: return ""
    kata_kunci = pertanyaan_user.lower()
    hasil = unique_foods[unique_foods['Food_Item'].str.lower().str.contains(kata_kunci)]
    if hasil.empty: return ""

    konteks = "Info Nutrisi:\n"
    for _, baris in hasil.head(2).iterrows():
        konteks += f"- {baris['Food_Item']}: Kalori ~{baris['Calories (kcal)']} kcal, Protein ~{baris['Protein (g)']}g.\n"
    return konteks

# --- API Endpoints ---
@app.route('/api/workouts')
def get_workouts_data():
    if df_latihan is not None:
        body_parts = sorted(df_latihan['BodyPart'].unique())
        levels = sorted(df_latihan['Level'].unique())
        return jsonify({'workouts': workouts_list, 'filters': {'body_parts': body_parts, 'levels': levels}})
    return jsonify({'error': 'Workout data not found'}), 404

@app.route('/api/nutrition')
def get_nutrition_data():
    if unique_foods is not None:
        categories = sorted(unique_foods['Category'].unique())
        return jsonify({'foods': foods_list, 'filters': {'categories': categories}})
    return jsonify({'error': 'Nutrition data not found'}), 404

@app.route('/api/ask', methods=['POST', 'OPTIONS'])
def tanya_ai():
    if request.method == 'OPTIONS':
        return '', 204
        
    pertanyaan = request.json.get("question")
    if not pertanyaan:
        return jsonify({"error": "Question is required."}), 400

    konteks_latihan = cari_info_latihan(pertanyaan)
    konteks_makanan = cari_info_makanan(pertanyaan)
    konteks_lengkap = (konteks_latihan + konteks_makanan).strip()
    if not konteks_lengkap:
        konteks_lengkap = "Tidak ada konteks spesifik yang ditemukan dari database."

    prompt = f"""
    Anda adalah 'Coach FitCare', seorang pelatih fitness dan nutrisi virtual.
    Gunakan 'Konteks dari Database' untuk menjawab 'Pertanyaan Pengguna'.
    Jika konteks tidak membantu, jawab sebaik mungkin sebagai seorang ahli.
    Jawab selalu dalam Bahasa Indonesia.

    [Konteks dari Database]
    {konteks_lengkap}

    [Pertanyaan Pengguna]
    {pertanyaan}
    
    [Jawaban Coach FitCare]
    """
    try:
        # Pastikan REPLICATE_API_TOKEN sudah di-set di file .env Anda
        # Library Replicate akan otomatis membacanya dari environment
        output_iterator = replicate.run(
            "ibm-granite/granite-3.3-8b-instruct",
            input={"prompt": prompt, "max_new_tokens": 512}
        )
        jawaban_lengkap = "".join(output_iterator)
        return jsonify({"answer": jawaban_lengkap})
    except Exception as e:
        print(f"Error saat menghubungi Replicate: {e}")
        return jsonify({"error": f"Error contacting AI service: {e}"}), 500
    
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
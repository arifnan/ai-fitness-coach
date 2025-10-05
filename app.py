import os
import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv, find_dotenv
import replicate

# --- Konfigurasi Awal ---
load_dotenv(find_dotenv())

app = Flask(__name__)


CORS(app, resources={r"/api/*": {"origins": "*"}}) # Mengizinkan semua origin untuk API

try:
    df_latihan = pd.read_csv('cleaned_megaGymDataset.csv')
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
        body_parts = sorted(list(df_latihan['BodyPart'].unique()))
        levels = sorted(list(df_latihan['Level'].unique()))
        return jsonify({'workouts': workouts_list, 'filters': {'body_parts': body_parts, 'levels': levels}})
    return jsonify({'error': 'Workout data not found'}), 404

@app.route('/api/workout/<int:workout_id>')
def get_workout_detail(workout_id):
    """Endpoint untuk mendapatkan detail satu latihan berdasarkan ID-nya."""
    if df_latihan is not None:
        try:
            workout = df_latihan.loc[df_latihan['Unnamed: 0'] == workout_id].to_dict('records')[0]
            return jsonify(workout)
        except (IndexError, KeyError):
            return jsonify({'error': 'Workout not found'}), 404
    return jsonify({'error': 'Workout data not available'}), 404


@app.route('/api/nutrition')
def get_nutrition_data():
    if unique_foods is not None:
        categories = sorted(list(unique_foods['Category'].unique()))
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
        output_iterator = replicate.run(
            "ibm-granite/granite-3.3-8b-instruct",
            input={"prompt": prompt, "max_new_tokens": 512}
        )
        jawaban_lengkap = "".join(output_iterator)
        return jsonify({"answer": jawaban_lengkap})
    except Exception as e:
        print(f"Error saat menghubungi Replicate: {e}")
        return jsonify({"error": f"Error contacting AI service: {e}"}), 500
    

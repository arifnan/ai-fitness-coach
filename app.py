import os
import pandas as pd
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import replicate

# --- Configuration and Setup ---
load_dotenv()
app = Flask(__name__)

if not os.getenv("REPLICATE_API_TOKEN"):
    raise ValueError("REPLICATE_API_TOKEN not found in .env")

try:
    df_latihan = pd.read_csv('cleaned_megaGymDataset.csv')
    # Convert dataframe to a list of dictionaries for easier use in the template
    workouts_list = df_latihan.to_dict(orient='records')
except FileNotFoundError:
    df_latihan = None
    workouts_list = []
    print("ERROR: cleaned_megaGymDataset.csv not found.")

# --- RAG Function (No Changes) ---
def cari_info_relevan(pertanyaan_user: str) -> str:
    if df_latihan is None:
        return "Database is unavailable."
    kata_kunci = pertanyaan_user.lower()
    hasil = df_latihan[df_latihan['Title'].str.lower().str.contains(kata_kunci)]
    if hasil.empty:
        return "No specific context found in the database."
    konteks = "Based on the exercise database, here is some relevant information:\n\n"
    for _, baris in hasil.head(3).iterrows():
        konteks += f"- {baris['combined_text']}\n"
    return konteks


def cari_info_makanan(pertanyaan_user: str) -> str:
    """Fungsi pencarian untuk data makanan."""
    if df_makanan is None:
        return "" # Kembalikan string kosong jika data tidak ada

    kata_kunci = pertanyaan_user.lower()
    
    # Cari makanan yang namanya mengandung kata kunci
    hasil = unique_foods[unique_foods['Food_Item'].str.lower().str.contains(kata_kunci)]

    if hasil.empty:
        return ""

    konteks = "Berdasarkan database nutrisi, ditemukan informasi berikut:\n\n"
    for _, baris in hasil.head(3).iterrows():
        konteks += (f"- {baris['Food_Item']}: "
                    f"Kalori ~{baris['Calories (kcal)']} kcal, "
                    f"Protein ~{baris['Protein (g)']}g, "
                    f"Karbohidrat ~{baris['Carbohydrates (g)']}g, "
                    f"Lemak ~{baris['Fat (g)']}g.\n")
    return konteks

# --- Web Page Routes ---
@app.route('/')
def halaman_utama():
    return render_template('home.html')

@app.route('/workouts')
def halaman_workouts():
    # Mengambil daftar unik untuk filter
    body_parts = sorted(df_latihan['BodyPart'].unique())
    levels = sorted(df_latihan['Level'].unique())
    
    # Kita kirim semua data yang dibutuhkan ke template
    return render_template('workouts.html', 
                           workouts=workouts_list, 
                           body_parts=body_parts, 
                           levels=levels)
@app.route('/nutrition')
def halaman_nutrition():
    categories = sorted(unique_foods['Category'].unique())
    return render_template('nutrition.html', 
                           foods=foods_list, 
                           categories=categories)

@app.route('/about')
def halaman_about():
    return render_template('about.html')

# --- API Endpoint for Chatbot ---
@app.route('/ask', methods=['POST'])
def tanya_ai():
    pertanyaan = request.json.get("question")
    if not pertanyaan:
        return jsonify({"error": "Question is required."}), 400

    # Panggil KEDUA fungsi pencarian
    konteks_latihan = cari_info_relevan(pertanyaan)
    konteks_makanan = cari_info_makanan(pertanyaan)

    # Gabungkan kedua konteks
    konteks_lengkap = ""
    if "Tidak ada konteks spesifik" not in konteks_latihan:
        konteks_lengkap += konteks_latihan + "\n"
    if konteks_makanan:
        konteks_lengkap += konteks_makanan

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
    
    [Coach FitCare's Answer]
    """
    try:
        output_iterator = replicate.run(
            "ibm-granite/granite-3.3-8b-instruct",
            input={"prompt": prompt, "max_new_tokens": 512}
        )
        jawaban_lengkap = "".join(output_iterator)
        return jsonify({"answer": jawaban_lengkap})
    except Exception as e:
        return jsonify({"error": f"Error contacting AI service: {e}"}), 500


try:
    df_makanan = pd.read_csv('daily_food_nutrition_dataset.csv')
    # Membersihkan nama kolom dari spasi ekstra
    df_makanan.columns = df_makanan.columns.str.strip()

    # Mengelompokkan berdasarkan nama makanan dan menghitung rata-rata gizinya
    unique_foods = df_makanan.groupby('Food_Item').agg({
        'Calories (kcal)': 'mean',
        'Protein (g)': 'mean',
        'Carbohydrates (g)': 'mean',
        'Fat (g)': 'mean',
        'Category': 'first' # Ambil kategori dari entri pertama
    }).reset_index()

    # Membulatkan nilai gizi menjadi 1 angka desimal
    unique_foods = unique_foods.round(1)

    # Mengubah dataframe menjadi list of dictionaries untuk template
    foods_list = unique_foods.to_dict(orient='records')
    print(f"✅ Dataset makanan berhasil diproses. Ditemukan {len(foods_list)} item unik.")

except FileNotFoundError:
    df_makanan = None
    foods_list = []
    print("❌ ERROR: daily_food_nutrition_dataset.csv not found.")

# --- Run the App ---
if __name__ == '__main__':
    app.run(debug=True, port=5000)
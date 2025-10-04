# ai-fitness-coach

# FitCare AI: Backend API & AI Engine

## 💡 Visi & Latar Belakang Proyek

Di era digital saat ini, informasi kesehatan seharusnya mudah diakses. Namun, kenyataannya justru sebaliknya. Calon pengguna seringkali dihadapkan pada "Tembok Informasi" yang membingungkan, mahal, dan tidak dapat diandalkan.

**Masalah yang Kami Pecahkan:**

* **Banjir Misinformasi:** Sebuah studi menunjukkan bahwa **lebih dari 87%** konten fitness di platform video populer mengandung informasi yang tidak akurat secara ilmiah. Ini menciptakan kebingungan dan risiko cedera.
* **Biaya yang Tinggi:** Jasa seorang pelatih pribadi atau ahli gizi profesional bisa mencapai jutaan rupiah per bulan, membuatnya tidak terjangkau bagi sebagian besar masyarakat.
* **Kurangnya Personalisasi:** Saran generik "satu untuk semua" dari internet seringkali tidak efektif. Setiap individu membutuhkan panduan yang disesuaikan dengan kebutuhan dan level kebugaran mereka.

**Solusi Kami:** **FitCare AI** lahir dari visi untuk mendemokratisasi akses terhadap panduan kesehatan yang andal dan terpersonalisasi. Kami membangun jembatan antara data fitness berbasis sains dan pengguna awam melalui kekuatan Kecerdasan Buatan (AI), menyediakannya secara gratis dan tersedia 24/7.

---

## 🚀 Deskripsi Proyek

Layanan ini adalah **otak dan tulang punggung** dari platform FitCare AI. Dibangun menggunakan **Python** dan **Flask**, backend ini berfungsi sebagai API (Application Programming Interface) yang tangguh dan cerdas. Tugas utamanya adalah mengelola data, melayani permintaan dari frontend, dan yang terpenting, menjalankan logika AI yang canggih untuk memberikan jawaban yang akurat dan relevan kepada pengguna.

---

## 🛠️ Teknologi yang Digunakan

| Kategori      | Teknologi                                                              |
| :------------ | :--------------------------------------------------------------------- |
| **Bahasa** | Python 3.10+                                                           |
| **Framework** | Flask                                                                  |
| **Server** | Gunicorn (Untuk Produksi)                                              |
| **Data** | Pandas                                                                 |
| **AI** | Replicate API (Model: `ibm-granite/granite-3.3-8b-instruct`)           |
| **Manajemen** | `python-dotenv` (Environment Variables), `Flask-Cors` (Konektivitas API) |

---

## ✨ Fitur Unggulan

* **API Data Terstruktur**: Menyediakan endpoint `/api/workouts` dan `/api/nutrition` yang menyajikan data latihan dan nutrisi bersih dalam format JSON.
* **Sistem Chatbot Cerdas**: Endpoint `/api/ask` yang menerima pertanyaan dalam bahasa alami.
* **Pembersihan Data Otomatis**: Secara dinamis memproses dan membersihkan dataset CSV dari nilai-nilai kosong (`NaN`) untuk memastikan integritas data API.
* **Arsitektur Siap Produksi**: Dirancang untuk dijalankan dengan Gunicorn, memastikan stabilitas dan kemampuan menangani banyak permintaan.

---

## 🧠 Penjelasan Arsitektur AI: Retrieval-Augmented Generation (RAG)

Fitur chatbot kami bukan sekadar pembungkus API biasa. Kami mengimplementasikan arsitektur **Retrieval-Augmented Generation (RAG)** untuk menghasilkan jawaban yang superior.

**Bagaimana Cara Kerjanya?**

1.  **Retrieval (Pengambilan Informasi)**: Saat pengguna bertanya (misal: "bagaimana cara melakukan crunch?"), sistem tidak langsung bertanya ke AI. Ia pertama-tama "membaca buku" dengan mencari kata kunci "crunch" di dalam dataset latihan (`cleaned_megaGymDataset.csv`).
2.  **Augmentation (Penambahan Konteks)**: Informasi relevan yang ditemukan (deskripsi, bagian tubuh, level) kemudian "distabilo" dan digabungkan dengan pertanyaan asli pengguna.
3.  **Generation (Penghasilan Jawaban)**: Prompt yang sudah diperkaya ini (`Pertanyaan Pengguna + Konteks dari Database`) dikirim ke model AI di Replicate. Dengan konteks tambahan ini, AI bisa memberikan jawaban yang jauh lebih akurat dan faktual, berdasarkan data yang kita miliki.

**Keunggulan RAG:**
* **Mengurangi Halusinasi**: Mencegah AI "mengarang" jawaban.
* **Akurasi Tinggi**: Jawaban didasarkan pada sumber data yang terverifikasi.
* **Spesifik dan Relevan**: AI dapat memberikan detail yang hanya ada di dalam dataset kita.

---

## ⚙️ Instruksi Setup & Menjalankan

1.  **Clone repositori ini** ke mesin lokal Anda.
2.  **Buat dan aktifkan virtual environment:**
    ```bash
    # Buat environment
    python -m venv venv
    # Aktifkan (Windows)
    venv\Scripts\activate
    # Aktifkan (Mac/Linux)
    # source venv/bin/activate
    ```
3.  **Install semua dependensi** yang dibutuhkan:
    ```bash
    pip install -r requirements.txt
    ```
4.  **Konfigurasi Environment Variable**: Buat file bernama `.env` di direktori utama dan tambahkan kunci API Replicate Anda:
    ```
    REPLICATE_API_TOKEN=r8_xxxxxxxxxxxxxxxxxxxxxx
    ```
5.  **Jalankan Server**:
    * **Untuk Development Lokal (mudah & cepat):**
        ```bash
        flask run
        ```
    * **Untuk Simulasi Produksi (menggunakan Gunicorn):**
        ```bash
        gunicorn app:app
        ```

Layanan backend sekarang akan berjalan dan siap menerima permintaan dari frontend.

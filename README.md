# ai-fitness-coach
FitCare AI: Backend API & AI Engine

## 1. Project Overview

### Latar Belakang & Permasalahan yang Diangkat

Di era digital saat ini, akses terhadap informasi kesehatan seharusnya menjadi hak, bukan sebuah kemewahan. Namun, ironisnya, internet justru menciptakan paradoks: semakin banyak informasi, semakin tinggi tingkat kebingungan dan misinformasi.

**Data yang Mendasari Proyek Ini:**
* **Krisis Kepercayaan:** Sebuah studi dari Universitas Alberta menemukan bahwa **lebih dari 87%** konten fitness yang paling banyak dilihat di YouTube mengandung informasi yang tidak akurat secara ilmiah dan berpotensi membahayakan.
* **Hambatan Finansial:** Biaya untuk menyewa seorang pelatih pribadi bersertifikat di kota-kota besar Indonesia dapat dengan mudah melebihi **Rp 3.000.000 per bulan**, membuatnya tidak terjangkau bagi mayoritas populasi.
* **Kebingungan Pengguna:** Pengguna pemula dihadapkan pada ribuan artikel dan video yang seringkali kontradiktif, menyebabkan frustrasi, demotivasi, dan program latihan yang tidak efektif.

**FitCare AI** hadir sebagai jawaban atas tantangan ini. **Tujuan proyek ini sangat jelas:** **mendemokratisasi akses terhadap panduan fitness dan nutrisi yang andal, terpersonalisasi, dan berbasis data, melalui sebuah platform yang gratis dan dapat diakses kapan saja.**

### Pendekatan Kami

Kami membangun sebuah layanan backend yang berfungsi sebagai "otak" terpusat. Pendekatan ini menggunakan arsitektur API modern yang memisahkan logika bisnis dan AI dari antarmuka pengguna, memastikan sistem yang lebih aman, skalabel, dan mudah dikelola.

---

## 2. Teknologi yang Digunakan

Setiap teknologi dipilih dengan tujuan spesifik untuk menciptakan backend yang efisien, tangguh, dan siap untuk masa depan.

| Teknologi         | Peran dalam Proyek                                                                                                                          | Alasan Pemilihan                                                                                                                              |
| :---------------- | :------------------------------------------------------------------------------------------------------------------------------------------ | :-------------------------------------------------------------------------------------------------------------------------------------------- |
| **Python** | Bahasa pemrograman utama.                                                                                                                   | Ekosistemnya yang matang untuk *data science* (Pandas) dan pengembangan web menjadikannya pilihan alami dan paling efisien.                |
| **Flask** | *Micro-framework* untuk membangun API.                                                                                                      | Sifatnya yang ringan dan modular sangat ideal untuk membangun layanan API yang terfokus, tanpa *overhead* dari *framework* yang lebih besar. |
| **Gunicorn** | WSGI *production server*.                                                                                                                   | Krusial untuk *deployment*. Gunicorn mampu menangani banyak permintaan secara bersamaan dan jauh lebih stabil daripada server bawaan Flask.   |
| **Pandas** | Memuat, membersihkan, dan memproses dataset `.csv`.                                                                                         | Alat standar industri untuk manipulasi data. Memungkinkan pemrosesan dataset latihan dan nutrisi secara efisien saat aplikasi dimulai.         |
| **Replicate API** | Platform untuk mengakses model AI canggih.                                                                                                  | Menyediakan akses *serverless* ke model AI seperti **IBM Granite** tanpa perlu mengelola infrastruktur AI yang kompleks.                      |
| **Flask-Cors** | Mengelola kebijakan Cross-Origin Resource Sharing.                                                                                          | Komponen keamanan esensial yang memungkinkan frontend (di domain berbeda) untuk berkomunikasi secara aman dengan backend ini.                 |
| **Dotenv** | Mengelola *environment variables*.                                                                                                          | Praktik keamanan fundamental untuk menjaga kerahasiaan kunci API dan kredensial lainnya, memisahkannya dari *source code*.                 |

---

## 3. Fitur Utama

Layanan backend ini menyediakan tiga pilar fungsionalitas utama melalui API endpoint yang terstruktur.

* **Penyedia Data Dinamis (`/api/workouts` & `/api/nutrition`)**
    * **Cara Kerja:** Saat dijalankan, server secara otomatis memuat dataset `cleaned_megaGymDataset.csv` dan `daily_food_nutrition_dataset.csv`. Data tersebut dibersihkan dari nilai-nilai kosong (`NaN`) untuk memastikan integritas JSON, lalu disajikan melalui endpoint API.
    * **Fungsi:** Menyediakan data mentah yang bersih dan terstruktur untuk ditampilkan dan difilter oleh aplikasi frontend, memungkinkan pembuatan perpustakaan latihan dan panduan nutrisi yang interaktif.

* **Mesin Percakapan AI (`/api/ask`)**
    * **Cara Kerja:** Endpoint ini menerima pertanyaan pengguna dalam bahasa alami. Ia kemudian menjalankan logika RAG (dijelaskan di bawah) untuk mencari konteks internal, menyusun prompt yang disempurnakan, dan mengirimkannya ke model AI `ibm-granite/granite-3.3-8b-instruct`.
    * **Fungsi:** Ini adalah fitur inti dari aplikasi. Ia mengubah platform dari sekadar penampil data statis menjadi seorang pelatih virtual yang dapat menjawab pertanyaan spesifik pengguna secara dinamis.

---

## 4. Penjelasan Dukungan AI

Penggunaan AI dalam proyek ini bukan sekadar gimik; ini adalah fondasi yang memberikan nilai unik dan memecahkan masalah inti dari misinformasi.

### Arsitektur: Retrieval-Augmented Generation (RAG)

Kami tidak hanya "membungkus" sebuah Large Language Model (LLM). Kami mengimplementasikan arsitektur **RAG** untuk menciptakan sistem yang lebih cerdas dan dapat dipercaya.

1.  **Retrieval (Pengambilan):** Saat sebuah pertanyaan masuk, sistem kami tidak langsung bertanya pada AI. Ia bertindak seperti seorang peneliti, dengan cepat memindai dataset internal kami (`.csv` files) untuk menemukan potongan informasi yang paling relevan dengan pertanyaan tersebut.
2.  **Augmentation (Penyempurnaan):** Informasi faktual yang ditemukan ini (misalnya, deskripsi latihan yang benar atau data kalori yang tepat) kemudian "dilampirkan" pada pertanyaan pengguna. Ini menciptakan sebuah prompt baru yang jauh lebih kaya konteks.
3.  **Generation (Penghasilan Jawaban):** Prompt yang sudah disempurnakan inilah yang dikirim ke model AI. Dengan "contekan" berbasis data ini, AI tidak perlu menebak-nebak. Ia dapat merangkai jawaban yang tidak hanya terdengar alami tetapi juga berakar pada fakta dari database kita.

**Keunggulan RAG:**
* **Mengurangi Halusinasi**: Mencegah AI "mengarang" jawaban.
* **Akurasi Tinggi**: Jawaban didasarkan pada sumber data yang terverifikasi.
* **Spesifik dan Relevan**: AI dapat memberikan detail yang hanya ada di dalam dataset kita.


### Dampak Nyata Penggunaan AI
* **Membangun Kepercayaan Pengguna:** Dampak terbesar adalah **mitigasi risiko halusinasi AI**. Dalam aplikasi kesehatan, memberikan informasi yang salah bisa berbahaya. Dengan RAG, kami memastikan jawaban AI terikat pada data yang telah kami kurasi, menjadikannya sumber yang jauh lebih aman dan dapat diandalkan dibandingkan chatbot AI generik.
* **Menciptakan Pengalaman Personal:** AI memungkinkan setiap pengguna mendapatkan jawaban yang terasa seperti percakapan satu-lawan-satu. Pengguna tidak perlu lagi menyaring ratusan artikel; mereka bisa langsung bertanya dan mendapatkan jawaban yang relevan untuk kebutuhan spesifik mereka, secara instan.
* **Skalabilitas Bimbingan:** AI memungkinkan kami untuk memberikan "bimbingan ahli" kepada ribuan pengguna secara bersamaan, sebuah tugas yang tidak mungkin dilakukan oleh pelatih manusia, sehingga benar-benar mencapai misi kami untuk mendemokratisasi pengetahuan kesehatan.

# Topic Pulse — Topic-Based Review Analysis for Indonesian Tokopedia Reviews

Proyek ini memanfaatkan Python dan BERTopic untuk melampaui analisis sentimen dengan mengidentifikasi topik utama di balik pujian maupun keluhan pelanggan pada ulasan Tokopedia menggunakan dataset PRDECT-ID.

Aplikasi ini memungkinkan pengguna untuk mempelajari metodologi pemodelan, menjelajahi dashboard Exploratory Data Analysis (EDA) yang interaktif, memprediksi tema dari sebuah ulasan secara real-time, serta mengirimkan ulasan baru yang secara otomatis diklasifikasikan ke dalam topik yang sesuai..

![App Preview](topic-pulse-logo.png)

---

## Team

| Name | Role | Job Description |
|---|---|---|
| Fauzi Maulana | Data Analyst | Exploratory Data Analysis, dashboard insight, interpretasi tema & sentimen |
| Derida Falahian | Data Engineer | Arsitektur deployment, integrasi FastAPI–Streamlit, database, CI/CD |
| Dafa Hutapea | Data Scientist | Preprocessing teks, training model BERTopic, evaluasi model |

---

## Features

- **Methodology** — penjelasan alur kerja model dari awal hingga akhir
- **EDA Dashboard** — visualisasi interaktif tema, emosi, rating, harga, dan sebaran geografis
- **Predict Theme** — prediksi tema dari teks ulasan baru secara real-time
- **Submit a Review** — input ulasan baru yang otomatis diberi tema saat masuk ke database

---

## Tech Stack

- **Modeling**: Python, BERTopic (BERT-based topic modeling), Sentence Transformers
- **Frontend**: Streamlit
- **Backend**: FastAPI (inference service)
- **Database**: PostgreSQL (Supabase)
- **Deployment**: Streamlit Community Cloud (frontend), Hugging Face Spaces (FastAPI inference API)

---

## Project Structure

```
havktiv8-final-project/
├── fastpi/                      # FastAPI inference
│   ├── utils/
│   ├── artifacts/
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
├── streamlit/                   # frontend
│   └── src/
│       ├── app.py
│       ├── eda.py
│       ├── methodology.py
│       ├── prediction.py
│       ├── utils/
│       ├── requirements.txt
│       └── .streamlit/
│           └── secrets.toml     # (local only)
└── README.md
```

---

## Running Locally

### Prerequisites

- Python 3.11+
- Git
- Akun Supabase (untuk database) — opsional jika hanya menjalankan frontend

### 1. Clone repository

```bash
git clone https://github.com/Derida21/havktiv8-final-project.git
cd havktiv8-final-project
```

### 2. Setup FastAPI (inference service)

```bash
cd fastpi
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS/Linux

pip install -r requirements.txt
```

Buat file `.env` di dalam folder `fastpi/` (jangan di-push ke Git):

```
INFERENCE_API_KEY=nilai-rahasia-kamu
```

Jalankan servernya:

```bash
uvicorn app:app --reload --port 8000
```

Cek apakah service sudah hidup: buka `http://localhost:8000/health` di browser, harus mengembalikan `{"status": "ok"}`.

### 3. Setup Streamlit (frontend)


Buat folder `.streamlit/` di dalam `streamlit/src/`, lalu buat file `.streamlit/secrets.toml`:

```toml
API_URL = "http://localhost:8000"
INFERENCE_API_KEY = "nilai-rahasia-yang-sama-dengan-di-fastpi/.env"

[connections.supabase]
dialect = "postgresql"
host = "your-supabase-host"
port = 5432
database = "postgres"
username = "your-username"
password = "your-password"
```

> ⚠️ File `secrets.toml` dan `.env` berisi kredensial rahasia — pastikan sudah masuk `.gitignore` dan **tidak pernah** di-commit ke repository.

Jalankan Streamlit:

```bash
streamlit run app.py
```

Buka `http://localhost:8501` di browser.

---

## Environment Variables Summary

| Variable | Digunakan di | Keterangan |
|---|---|---|
| `INFERENCE_API_KEY` | FastAPI & Streamlit | Harus identik di kedua sisi untuk otentikasi request |
| `API_URL` | Streamlit | URL FastAPI (local: `http://localhost:8000`, production: URL Hugging Face Spaces) |
| `connections.supabase.*` | Streamlit | Kredensial koneksi database Supabase |

---

## Deployment

- **FastAPI**: di-deploy ke [Hugging Face Spaces](https://huggingface.co/spaces) menggunakan Docker
- **Streamlit**: di-deploy ke [Streamlit Community Cloud](https://streamlit.io/cloud), dengan main file path `streamlit/src/app.py`

Secrets untuk masing-masing platform diisi lewat dashboard platform tersebut (Hugging Face Spaces → Settings → Secrets; Streamlit Cloud → App Settings → Secrets), bukan lewat file yang di-commit.
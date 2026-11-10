# TASKS.md — Roadmap Pengembangan Hermes Local Autonomous Financial Analyst

Dokumen ini memuat daftar tugas bertahap (*step-by-step roadmap*) untuk mentransformasi **hermes-local** menjadi platform *Autonomous Financial Analyst* profesional. 

> **Panduan Penggunaan**:
> Anda cukup menyebutkan nomor langkah saat ingin melanjutkan pengerjaan (contoh: *"Jalankan Step 1"* atau *"Kerjakan Step 2.1"*). Status setiap item akan diperbarui secara berkala (`[x]` untuk yang sudah diterapkan dan `[ ]` untuk yang belum).

---

## 📌 Ringkasan Status Progres

| Step | Modul / Fitur | Status |
| :--- | :--- | :---: |
| **Step 0** | **Fondasi Awal & Baseline Agent** | ✅ Selesai (Baseline) |
| **Step 1** | **Analisis Teknikal & Risiko Kuantitatif Jangka Panjang** | ⏳ Belum Diterapkan |
| **Step 2** | **Analisis Fundamental & Valuasi Historis** | ⏳ Belum Diterapkan |
| **Step 3** | **Multi-Source Sentiment & Internet Intelligence** | ⏳ Belum Diterapkan |
| **Step 4** | **Data Makroekonomi & Komoditas Sektoral** | ⏳ Belum Diterapkan |
| **Step 5** | **Standarisasi Laporan Riset & Visualisasi Chart** | ⏳ Belum Diterapkan |
| **Step 6** | **Arsitektur Multi-Agent (Specialized Analyst Team)** | ⏳ Belum Diterapkan |
| **Step 7** | **Memory, Persistence, & Antarmuka Pengguna** | ⏳ Belum Diterapkan |

---

## 📋 Rincian Tugas (Detailed Task List)

### Step 0: Baseline & Infrastruktur Awal (Sudah Selesai)
- [x] **0.1 Setup Model & Endpoint Lokal**: Integrasi Ollama dengan model `hermes3:8b`.
- [x] **0.2 Tool Data Saham Dasar**: Implementasi `get_stock_data` (harga penutupan 5 hari via `yfinance`).
- [x] **0.3 Tool Berita Dasar**: Implementasi `search_market_news` (3 berita via DuckDuckGo).
- [x] **0.4 Execution Loop Sederhana**: Mekanisme recursive tool calling hingga jawaban final.
- [x] **0.5 Dokumentasi Proyek**: Pembuatan `AGENTS.md` dan `requirements.txt`.

---

### Step 1: Analisis Teknikal & Risiko Kuantitatif Jangka Panjang
*Tujuan: Membekali Hermes dengan kemampuan membaca tren jangka panjang (1–5 tahun), indikator momentum, dan metrik risiko volatilitas.*

- [ ] **1.1 Modul Indikator Tren & Momentum**:
  - Implementasi Simple Moving Average (SMA 50, 100, 200) & deteksi Golden/Death Cross.
  - Implementasi Relative Strength Index (RSI 14) untuk zona overbought/oversold.
  - Implementasi MACD (Moving Average Convergence Divergence) & sinyal momentum.
- [ ] **1.2 Modul Volatilitas & Level Harga Kritis**:
  - Implementasi Bollinger Bands untuk mengukur pemampatan volatilitas (*squeeze*).
  - Deteksi level Support & Resistance historis serta 52-Week High / Low.
  - Average True Range (ATR) untuk kalkulasi jarak ideal *Stop Loss*.
- [ ] **1.3 Modul Metrik Risiko Kuantitatif**:
  - Kalkulasi *Maximum Drawdown* (MDD) 1–3 tahun terakhir.
  - Kalkulasi volatilitas tahunan (*Annualized Volatility*) dan *Sharpe Ratio*.
  - Kalkulasi *Beta* saham terhadap indeks acuan (IHSG `^JKSE` atau S&P 500 `^GSPC`).
- [ ] **1.4 Integrasi Tool ke Hermes**:
  - Daftarkan fungsi ke `available_tools` dan perbarui `tools_schema` di `agent.py`.

---

### Step 2: Analisis Fundamental & Valuasi Historis
*Tujuan: Membaca kesehatan finansial emiten, valuasi relatif, dan pertumbuhan laba multi-tahun.*

- [ ] **2.1 Ekstraksi Laporan Keuangan Multi-Tahun**:
  - Mengambil data Neraca (*Balance Sheet*), Laba Rugi (*Income Statement*), dan Arus Kas (*Cash Flow*) 3–5 tahun terakhir via `yfinance`.
- [ ] **2.2 Perhitungan Rasio Finansial Utama**:
  - Profitabilitas: ROE (*Return on Equity*), ROA, Gross/Net Profit Margin.
  - Solvabilitas & Likuiditas: DER (*Debt to Equity*), Current Ratio, Quick Ratio.
  - Metrik Dividen: Dividend Yield historis dan Dividend Payout Ratio (DPR).
- [ ] **2.3 Analisis Pertumbuhan & Valuasi Historis**:
  - CAGR Revenue dan Net Profit 3–5 tahun terakhir.
  - Evaluasi rasio valuasi saat ini (P/E, P/BV, EV/EBITDA) terhadap rata-rata historisnya (*PE/PBV Standard Deviation Band*).
- [ ] **2.4 Integrasi Tool Fundamental ke Hermes**:
  - Buat tool `get_fundamental_analysis` dan daftarkan ke skema tools agen.

---

### Step 3: Multi-Source Sentiment & Internet Intelligence
*Tujuan: Menggabungkan sentimen berita pasar, media sosial investor, dan anomali pencarian publik.*

- [ ] **3.1 Portal Berita Finansial Terkurasi**:
  - Agregator berita pasar saham lokal Indonesia (Kontan, Bisnis.com, CNBC Indonesia via RSS/pencarian spesifik).
  - Ekstraksi pengumuman keterbukaan informasi emiten (Dividen, RUPS, Rights Issue, Akuisisi).
- [ ] **3.2 Social Sentiment Tracking (Komunitas Ritel)**:
  - Ekstraksi komentar publik forum saham (Stockbit stream / Reddit / Twitter-X *cashtags* seperti `$BBCA`, `$BBRI`).
- [ ] **3.3 Google Trends Anomaly Detection**:
  - Integrasi `pytrends` untuk mendeteksi lonjakan volume pencarian publik terhadap nama emiten atau produknya.
- [ ] **3.4 Engine Scoring Sentimen & Katalis**:
  - Algoritma scoring sentimen terpadu (-1.0 sangat bearish s/d +1.0 sangat bullish).
  - Ekstraksi poin-poin katalis pendorong dan risiko penekan harga.

---

### Step 4: Data Makroekonomi & Komoditas Sektoral (Top-Down Analysis)
*Tujuan: Memberikan konteks makro ekonomi dan pengaruh komoditas global terhadap saham.*

- [ ] **4.1 Indikator Moneter & Makro**:
  - Data suku bunga acuan (BI-Rate, The Fed / FFR) dan tren inflasi terkini.
  - Nilai tukar mata uang asing (USD/IDR `USDIDR=X`).
- [ ] **4.2 Data Harga Komoditas Acuan**:
  - Batubara, Minyak Mentah (WTI/Brent `CL=F`), Emas (`GC=F`), Nikel, dan CPO untuk sektor tambang, energi, dan perkebunan.
- [ ] **4.3 Tool Sector Correlation Mapping**:
  - Tool yang memetakan keterkaitan emiten dengan pergerakan harga komoditas acuan secara otomatis.

---

### Step 5: Standarisasi Laporan Riset & Visualisasi Chart
*Tujuan: Mengubah respons teks polos menjadi laporan riset investasi bergaya institusi profesional.*

- [ ] **5.1 Template Standar Equity Research**:
  - Struktur laporan terstandarisasi:
    - *Executive Summary* & Rekomendasi (*Strong Buy / Buy / Hold / Sell*)
    - *12-Month Target Price* & *Risk-to-Reward Ratio*
    - *Key Investment Thesis* & Katalis Utama
    - *Risks to Target Price* (Kondisi yang membatalkan skenario rekomendasi)
- [ ] **5.2 Pembuatan Chart Visual Otomatis**:
  - Integrasi `mplfinance` untuk menghasilkan grafik Candlestick dengan overlay MA 50/200, volume, dan indikator RSI.
  - Simpan chart dalam format file gambar (PNG) sebagai lampiran analisa.
- [ ] **5.3 Export Laporan ke Dokumen Formal**:
  - Opsi ekspor laporan ke format Markdown komprehensif atau PDF siap cetak.

---

### Step 6: Arsitektur Multi-Agent (Specialized Analyst Team)
*Tujuan: Membagi beban kognitif Hermes ke dalam beberapa sub-agen spesialis yang saling melengkapi.*

- [ ] **6.1 Technical & Risk Analyst Agent**:
  - Sub-agen khusus analisis tren grafik, volatilitas, dan penentuan level *entry/exit/cut loss*.
- [ ] **6.2 Fundamental & Valuation Analyst Agent**:
  - Sub-agen khusus membedah kesehatan finansial dan valuasi wajar saham.
- [ ] **6.3 Macro & Sentiment Analyst Agent**:
  - Sub-agen khusus memetakan dinamika sentimen pasar dan iklim makroekonomi.
- [ ] **6.4 Chief Investment Officer (Lead Agent Orchestrator)**:
  - Agen pimpinan yang menerima laporan dari ketiga sub-agen, merekonsiliasi kontradiksi sinyal, dan menyusun keputusan investasi final.

---

### Step 7: Memory, Persistence, & Antarmuka Pengguna (UI)
*Tujuan: Menjadikan sistem dapat mengingat analisa masa lalu dan mudah diakses pengguna.*

- [ ] **7.1 Modul Konfigurasi Terpusat (`.env`)**:
  - Pindahkan URL endpoint, nama model, timeout, dan parameter default ke berkas konfigurasi `.env`.
- [ ] **7.2 Database Riwayat & Evaluasi Analisis**:
  - Penyimpanan SQLite untuk menyimpan histori rekomendasi saham dan mengevaluasi akurasi prediksi setelah 1/3/6 bulan.
- [ ] **7.3 Antarmuka Pengguna Interaktif**:
  - Pembuatan Web Dashboard sederhana (Streamlit atau web app) atau integrasi Bot Telegram untuk alert pasar harian.

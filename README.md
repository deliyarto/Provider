# 🏥 Direktori RS Rekanan — Managed Care Pertamedika IHC

==claude user tapahadi respati brave broser
Aplikasi Streamlit untuk mencari daftar rumah sakit rekanan asuransi, lengkap dengan fitur admin untuk update data via CSV.

## ✨ Fitur
- 🔍 Search RS berdasarkan nama, kota, provinsi, kelas, dan tipe
- 📋 Tabel semua RS dengan export CSV
- ⚙️ Admin panel dengan upload CSV untuk update data RS
- 🔐 Login admin dengan password (via Streamlit Secrets)

## 🚀 Deploy ke Streamlit Cloud

### 1. Push ke GitHub
```bash
git init
git add .
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/USERNAME/REPO_NAME.git
git push -u origin main
```

### 2. Deploy di Streamlit Cloud
1. Buka [share.streamlit.io](https://share.streamlit.io)
2. Klik **New app**
3. Pilih repo GitHub Anda
4. Set **Main file path**: `mcprov.py`
5. Klik **Deploy**

### 3. Set Admin Password (WAJIB)
Di Streamlit Cloud, buka **Settings > Secrets**, lalu isi:
```toml
ADMIN_PASSWORD = "password_rahasia_anda"
```

> ⚠️ Jangan pernah commit file `.streamlit/secrets.toml` ke GitHub!

## 📁 Struktur File
```
├── mcprov.py                  # Aplikasi utama
├── requirements.txt        # Dependensi Python
├── template_data_rs.csv    # Template CSV untuk admin
├── .gitignore
├── .streamlit/
│   └── secrets.toml        # Password admin (lokal, jangan di-commit)
└── README.md
```

## 📋 Format CSV
File CSV harus memiliki kolom berikut:

| Kolom | Keterangan | Contoh |
|-------|-----------|--------|
| `nama_rs` | Nama rumah sakit | RS Cipto Mangunkusumo |
| `kota` | Nama kota | Jakarta Pusat |
| `provinsi` | Nama provinsi | DKI Jakarta |
| `kelas` | Kelas RS (A/B/C/D) | A |
| `tipe` | Pemerintah atau Swasta | Pemerintah |
| `alamat` | Alamat lengkap | Jl. Diponegoro No.71 |
| `telepon` | Nomor telepon | (021) 500135 |
| `jam_operasional` | Jam buka | 24 Jam |

## 🔧 Menjalankan Lokal
```bash
pip install -r requirements.txt
streamlit run mcprov.py
```

---
Made with ❤️ using [Streamlit](https://streamlit.io)

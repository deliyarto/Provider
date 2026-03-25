import streamlit as st
import pandas as pd
import os
import io

# ─────────────────────────────────────────────
# KONFIGURASI HALAMAN
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Direktori Rumah Sakit | Managed Care Pertamedika IHC",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Force sidebar selalu terbuka
st.markdown("""
<style>
    [data-testid="collapsedControl"] { display: none !important; }
    section[data-testid="stSidebar"] { display: block !important; min-width: 250px !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    .stApp {
        background: linear-gradient(135deg, #f0f4ff 0%, #fafaff 50%, #f0f8ff 100%);
    }

    .hero-banner {
        background: linear-gradient(135deg, #1a3a6b 0%, #2563eb 60%, #0ea5e9 100%);
        border-radius: 16px;
        padding: 32px 40px;
        margin-bottom: 28px;
        color: white;
        box-shadow: 0 8px 32px rgba(37, 99, 235, 0.25);
    }
    .hero-banner h1 {
        font-size: 2rem;
        font-weight: 800;
        margin: 0 0 6px 0;
        letter-spacing: -0.5px;
    }
    .hero-banner p {
        font-size: 1rem;
        opacity: 0.85;
        margin: 0;
    }

    .stat-card {
        background: white;
        border-radius: 12px;
        padding: 18px 24px;
        text-align: center;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
        border: 1px solid #e8edf5;
    }
    .stat-number {
        font-size: 2rem;
        font-weight: 800;
        color: #2563eb;
        line-height: 1;
    }
    .stat-label {
        font-size: 0.8rem;
        color: #64748b;
        font-weight: 500;
        margin-top: 4px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .search-container {
        background: white;
        border-radius: 14px;
        padding: 24px 28px;
        margin-bottom: 24px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
        border: 1px solid #e8edf5;
    }
    .search-title {
        font-size: 0.85rem;
        font-weight: 700;
        color: #374151;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-bottom: 14px;
    }

    .rs-card {
        background: white;
        border-radius: 12px;
        padding: 20px 22px;
        margin-bottom: 14px;
        border: 1px solid #e8edf5;
        border-left: 4px solid #2563eb;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        transition: all 0.2s ease;
    }
    .rs-card:hover {
        box-shadow: 0 4px 20px rgba(37, 99, 235, 0.12);
        border-left-color: #0ea5e9;
        transform: translateY(-1px);
    }
    .rs-name {
        font-size: 1.05rem;
        font-weight: 700;
        color: #1e3a5f;
        margin-bottom: 6px;
    }
    .rs-meta {
        display: flex;
        gap: 16px;
        flex-wrap: wrap;
        font-size: 0.82rem;
        color: #64748b;
    }
    .rs-meta span {
        display: flex;
        align-items: center;
        gap: 4px;
    }
    .badge {
        display: inline-block;
        padding: 2px 10px;
        border-radius: 20px;
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.3px;
    }
    .badge-a { background: #dbeafe; color: #1d4ed8; }
    .badge-b { background: #dcfce7; color: #15803d; }
    .badge-c { background: #fef9c3; color: #a16207; }
    .badge-d { background: #fee2e2; color: #b91c1c; }
    .badge-utama { background: #f3e8ff; color: #7c3aed; }

    .admin-box {
        background: #fff7ed;
        border: 1px solid #fed7aa;
        border-radius: 12px;
        padding: 20px 24px;
        margin-top: 8px;
    }

    .no-result {
        text-align: center;
        padding: 48px 24px;
        color: #94a3b8;
    }
    .no-result-icon { font-size: 3rem; }
    .no-result-text { font-size: 1rem; font-weight: 500; margin-top: 12px; }

    .css-1d391kg, [data-testid="stSidebar"] {
        background: #1a3a6b !important;
    }
    [data-testid="stSidebar"] * {
        color: white !important;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# KOLOM TEMPLATE CSV
# ─────────────────────────────────────────────
TEMPLATE_COLS = ["nama_rs", "kota", "provinsi", "kelas", "tipe", "alamat", "telepon", "jam_operasional"]
CSV_PATH = "template_data_rs.csv"

# ⬇️ Ganti dengan URL raw GitHub CSV Anda
# Format: https://raw.githubusercontent.com/USERNAME/REPO/main/NAMA_FILE.csv
GITHUB_CSV_URL = "https://raw.githubusercontent.com/deliyarto/Provider/main/template_data_rs.csv"

# ─────────────────────────────────────────────
# FUNGSI LOAD DATA — prioritas: GitHub → lokal
# ─────────────────────────────────────────────
@st.cache_data(ttl=300)  # cache 5 menit, lalu fetch ulang dari GitHub
def load_data():
    # 1. Coba ambil dari GitHub (selalu up-to-date)
    try:
        import urllib.request
        with urllib.request.urlopen(GITHUB_CSV_URL, timeout=10) as response:
            raw = response.read()
        for enc in ["utf-8", "utf-8-sig", "latin-1", "cp1252"]:
            try:
                df = pd.read_csv(io.BytesIO(raw), encoding=enc)
                for col in TEMPLATE_COLS:
                    if col not in df.columns:
                        df[col] = "-"
                return df
            except (UnicodeDecodeError, Exception):
                continue
    except Exception:
        pass

    # 2. Fallback: baca dari file lokal (hasil upload via Admin Panel)
    if os.path.exists(CSV_PATH):
        try:
            df = pd.read_csv(CSV_PATH)
            for col in TEMPLATE_COLS:
                if col not in df.columns:
                    df[col] = "-"
            return df
        except Exception:
            pass

    return None  # tidak ada data sama sekali

def refresh_data():
    st.cache_data.clear()

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🏥 Managed Care Pertamedika IHC")
    st.markdown("---")
    st.markdown("**Bantuan**")
    st.markdown("📞 Call Center: **1500-123**")
    st.markdown("✉️ cs@medicare-ins.co.id")
    st.markdown("---")
    st.caption("v1.0.0 © 2025 Managed Care Pertamedika IHC")

# ─────────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────────
df = load_data()

# ─────────────────────────────────────────────
# HELPER: Badge
# ─────────────────────────────────────────────
def badge_kelas(kelas):
    kelas = str(kelas).strip().upper()
    mapping = {
        "A": ("A", "badge-a"),
        "B": ("B", "badge-b"),
        "C": ("C", "badge-c"),
        "D": ("D", "badge-d"),
        "UTAMA": ("Utama", "badge-utama"),
    }
    label, css = mapping.get(kelas, (kelas, "badge-b"))
    return f'<span class="badge {css}">Kelas {label}</span>'

def badge_tipe(tipe):
    css = "badge-a" if str(tipe).strip().lower() == "pemerintah" else "badge-utama"
    return f'<span class="badge {css}">{tipe}</span>'

def render_rs_card(row):
    kelas_html = badge_kelas(row.get("kelas", "-"))
    tipe_html = badge_tipe(row.get("tipe", "-"))
    st.markdown(f"""
    <div class="rs-card">
        <div class="rs-name">🏥 {row.get('nama_rs', '-')}</div>
        <div class="rs-meta">
            <span>📍 {row.get('alamat', '-')}, {row.get('kota', '-')}, {row.get('provinsi', '-')}</span>
        </div>
        <div class="rs-meta" style="margin-top:8px;">
            <span>📞 {row.get('telepon', '-')}</span>
            <span>🕐 {row.get('jam_operasional', '-')}</span>
            <span>{kelas_html}</span>
            <span>{tipe_html}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# HERO BANNER
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero-banner">
    <h1>🏥 Direktori Rumah Sakit Rekanan</h1>
    <p>Temukan rumah sakit rekanan Managed Care Pertamedika IHC di seluruh Indonesia — cashless & terpercaya</p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# STATS — hanya tampil jika data ada
# ─────────────────────────────────────────────
if df is not None:
    total_rs = len(df)
    total_kota = df["kota"].nunique()
    total_provinsi = df["provinsi"].nunique()
    total_kelas_a = len(df[df["kelas"].str.strip().str.upper() == "A"])

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f'<div class="stat-card"><div class="stat-number">{total_rs}</div><div class="stat-label">Total RS Rekanan</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="stat-card"><div class="stat-number">{total_kota}</div><div class="stat-label">Kota Terjangkau</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="stat-card"><div class="stat-number">{total_provinsi}</div><div class="stat-label">Provinsi</div></div>', unsafe_allow_html=True)
    with c4:
        st.markdown(f'<div class="stat-card"><div class="stat-number">{total_kelas_a}</div><div class="stat-label">RS Kelas A</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# NAVIGASI TABS
# ─────────────────────────────────────────────
tab2, tab1, tab3 = st.tabs(["📋 Semua RS", "🔍 Cari Rumah Sakit", "⚙️ Admin Panel"])

# ─────────────────────────────────────────────
# TAB 1: CARI RUMAH SAKIT
# ─────────────────────────────────────────────
with tab1:
    if df is None:
        st.warning("⚠️ Data rumah sakit belum tersedia. Silakan upload file CSV melalui tab **⚙️ Admin Panel**.")
    else:
        st.markdown('<div class="search-container">', unsafe_allow_html=True)
        st.markdown('<div class="search-title">🔎 Cari Rumah Sakit</div>', unsafe_allow_html=True)
        keyword = st.text_input(
            "",
            placeholder="Ketik nama RS, kota, provinsi, kelas, atau tipe... (contoh: RS Pusat Pertamina, Bandung, Swasta, Kelas A)",
            label_visibility="collapsed"
        )
        st.markdown('</div>', unsafe_allow_html=True)

        result = df.copy()
        if keyword:
            mask = df.apply(
                lambda col: col.astype(str).str.contains(keyword, case=False, na=False)
            ).any(axis=1)
            result = df[mask]

        st.markdown(f"**Menampilkan {len(result)} dari {total_rs} rumah sakit**")
        st.markdown("---")

        if len(result) == 0:
            st.markdown("""
            <div class="no-result">
                <div class="no-result-icon">🔍</div>
                <div class="no-result-text">Rumah sakit tidak ditemukan.<br>Coba kata kunci lain.</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            for _, row in result.iterrows():
                render_rs_card(row)

# ─────────────────────────────────────────────
# TAB 2: SEMUA RS
# ─────────────────────────────────────────────
with tab2:
    if df is None:
        st.warning("⚠️ Data rumah sakit belum tersedia. Silakan upload file CSV melalui tab **⚙️ Admin Panel**.")
    else:
        st.subheader("📋 Daftar Semua Rumah Sakit Rekanan")
        st.dataframe(
            df[["nama_rs", "kota", "provinsi", "kelas", "tipe", "telepon", "jam_operasional"]].rename(columns={
                "nama_rs": "Nama RS",
                "kota": "Kota",
                "provinsi": "Provinsi",
                "kelas": "Kelas",
                "tipe": "Tipe",
                "telepon": "Telepon",
                "jam_operasional": "Jam Operasional",
            }),
            use_container_width=True,
            hide_index=True,
            height=600,
        )
        csv_export = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇️ Download Data CSV",
            data=csv_export,
            file_name="data_rumah_sakit_rekanan.csv",
            mime="text/csv",
        )

# ─────────────────────────────────────────────
# TAB 3: ADMIN PANEL
# ─────────────────────────────────────────────
with tab3:
    st.subheader("⚙️ Admin Panel — Update Data Rumah Sakit")

    if "admin_logged_in" not in st.session_state:
        st.session_state.admin_logged_in = False

    if not st.session_state.admin_logged_in:
        st.markdown('<div class="admin-box">', unsafe_allow_html=True)
        st.markdown("🔐 **Login Admin**")
        pwd = st.text_input("Password Admin", type="password")
        if st.button("Login"):
            try:
                admin_password = st.secrets["ADMIN_PASSWORD"]
            except:
                admin_password = "admin123"
            if pwd == admin_password:
                st.session_state.admin_logged_in = True
                st.rerun()
            else:
                st.error("Password salah!")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.success("✅ Anda login sebagai Admin")
        if st.button("Logout"):
            st.session_state.admin_logged_in = False
            st.rerun()

        # Status data saat ini
        st.markdown("---")
        if df is None:
            st.error("❌ Belum ada data — pastikan file CSV ada di GitHub atau upload manual.")
        else:
            st.info(f"📊 Data aktif: **{len(df)} rumah sakit**")
            st.caption(f"🔗 Sumber utama: `{GITHUB_CSV_URL}`")
            st.caption(f"💾 Fallback lokal: `{CSV_PATH}`")

        st.markdown("### 📤 Upload File CSV Baru")
        st.info("""
        **Format CSV yang dibutuhkan:**
        Kolom wajib: `nama_rs`, `kota`, `provinsi`, `kelas`, `tipe`, `alamat`, `telepon`, `jam_operasional`

        Download template di bawah untuk memulai.
        """)

        # Template CSV kosong dengan 1 baris contoh
        template_data = [{
            "nama_rs": "RS Contoh",
            "kota": "Jakarta Pusat",
            "provinsi": "DKI Jakarta",
            "kelas": "A",
            "tipe": "Pemerintah",
            "alamat": "Jl. Contoh No.1",
            "telepon": "(021) 000000",
            "jam_operasional": "24 Jam"
        }]
        template_csv = pd.DataFrame(template_data).to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇️ Download Template CSV",
            data=template_csv,
            file_name="template_data_rs.csv",
            mime="text/csv",
        )

        uploaded = st.file_uploader("Upload file CSV baru:", type=["csv"])
        if uploaded:
            try:
                raw = uploaded.read()
                new_df = None
                for enc in ["utf-8", "utf-8-sig", "latin-1", "cp1252"]:
                    try:
                        new_df = pd.read_csv(io.BytesIO(raw), encoding=enc)
                        break
                    except (UnicodeDecodeError, Exception):
                        continue
                if new_df is None:
                    st.error("❌ File tidak bisa dibaca. Pastikan file CSV valid.")
                else:
                    required = ["nama_rs", "kota", "provinsi", "kelas", "tipe"]
                    missing = [c for c in required if c not in new_df.columns]
                    if missing:
                        st.error(f"❌ Kolom wajib tidak ditemukan: {', '.join(missing)}")
                    else:
                        st.success(f"✅ File valid — {len(new_df)} data RS ditemukan")
                        st.dataframe(new_df.head(5), use_container_width=True)
                        if st.button("💾 Simpan & Terapkan Data Baru", type="primary"):
                            new_df.to_csv(CSV_PATH, index=False, encoding="utf-8")
                            refresh_data()
                            st.success(f"✅ Data berhasil diperbarui! {len(new_df)} RS tersimpan.")
                            st.rerun()
            except Exception as e:
                st.error(f"Error membaca file: {e}")

        if df is not None:
            st.markdown("---")
            st.markdown("### 🗑️ Hapus Data")
            st.warning("Menghapus data akan mengosongkan direktori RS hingga CSV baru diupload.")
            if st.button("🗑️ Hapus Semua Data RS", type="secondary"):
                if os.path.exists(CSV_PATH):
                    os.remove(CSV_PATH)
                refresh_data()
                st.success("✅ Data berhasil dihapus.")
                st.rerun()

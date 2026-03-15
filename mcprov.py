import streamlit as st
import pandas as pd
import os

# ─────────────────────────────────────────────
# KONFIGURASI HALAMAN
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Direktori Rumah Sakit | MediCare Insurance",
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

    /* Background */
    .stApp {
        background: linear-gradient(135deg, #f0f4ff 0%, #fafaff 50%, #f0f8ff 100%);
    }

    /* Header banner */
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

    /* Stats row */
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

    /* Search box */
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

    /* RS Card */
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

    /* Admin panel */
    .admin-box {
        background: #fff7ed;
        border: 1px solid #fed7aa;
        border-radius: 12px;
        padding: 20px 24px;
        margin-top: 8px;
    }

    /* No result */
    .no-result {
        text-align: center;
        padding: 48px 24px;
        color: #94a3b8;
    }
    .no-result-icon { font-size: 3rem; }
    .no-result-text { font-size: 1rem; font-weight: 500; margin-top: 12px; }

    /* Sidebar */
    .css-1d391kg, [data-testid="stSidebar"] {
        background: #1a3a6b !important;
    }
    [data-testid="stSidebar"] * {
        color: white !important;
    }

    /* Hide streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# DATA RUMAH SAKIT (HARDCODED - bisa ganti via CSV)
# ─────────────────────────────────────────────
DATA_RS_DEFAULT = [
    {"nama_rs": "RS Cipto Mangunkusumo", "kota": "Jakarta Pusat", "provinsi": "DKI Jakarta", "kelas": "A", "tipe": "Pemerintah", "alamat": "Jl. Diponegoro No.71", "telepon": "(021) 500135", "jam_operasional": "24 Jam"},
    {"nama_rs": "RS Fatmawati", "kota": "Jakarta Selatan", "provinsi": "DKI Jakarta", "kelas": "A", "tipe": "Pemerintah", "alamat": "Jl. TB Simatupang No.1", "telepon": "(021) 7660552", "jam_operasional": "24 Jam"},
    {"nama_rs": "RS Persahabatan", "kota": "Jakarta Timur", "provinsi": "DKI Jakarta", "kelas": "A", "tipe": "Pemerintah", "alamat": "Jl. Persahabatan Raya No.1", "telepon": "(021) 4891708", "jam_operasional": "24 Jam"},
    {"nama_rs": "RS Premier Bintaro", "kota": "Tangerang Selatan", "provinsi": "Banten", "kelas": "B", "tipe": "Swasta", "alamat": "Jl. MH Thamrin No.1", "telepon": "(021) 27519999", "jam_operasional": "24 Jam"},
    {"nama_rs": "RS Hermina Depok", "kota": "Depok", "provinsi": "Jawa Barat", "kelas": "B", "tipe": "Swasta", "alamat": "Jl. Raya Siliwangi No.50", "telepon": "(021) 7720689", "jam_operasional": "24 Jam"},
    {"nama_rs": "RS Hasan Sadikin", "kota": "Bandung", "provinsi": "Jawa Barat", "kelas": "A", "tipe": "Pemerintah", "alamat": "Jl. Pasteur No.38", "telepon": "(022) 2034953", "jam_operasional": "24 Jam"},
    {"nama_rs": "RS Borromeus", "kota": "Bandung", "provinsi": "Jawa Barat", "kelas": "B", "tipe": "Swasta", "alamat": "Jl. Ir. H. Juanda No.100", "telepon": "(022) 2552001", "jam_operasional": "24 Jam"},
    {"nama_rs": "RS Santosa Hospital Bandung Central", "kota": "Bandung", "provinsi": "Jawa Barat", "kelas": "B", "tipe": "Swasta", "alamat": "Jl. Kebonjati No.38", "telepon": "(022) 4248333", "jam_operasional": "24 Jam"},
    {"nama_rs": "RS Dr. Kariadi", "kota": "Semarang", "provinsi": "Jawa Tengah", "kelas": "A", "tipe": "Pemerintah", "alamat": "Jl. Dr. Sutomo No.16", "telepon": "(024) 8413476", "jam_operasional": "24 Jam"},
    {"nama_rs": "RS Telogorejo", "kota": "Semarang", "provinsi": "Jawa Tengah", "kelas": "B", "tipe": "Swasta", "alamat": "Jl. KH Ahmad Dahlan No.3", "telepon": "(024) 8452575", "jam_operasional": "24 Jam"},
    {"nama_rs": "RS Dr. Soetomo", "kota": "Surabaya", "provinsi": "Jawa Timur", "kelas": "A", "tipe": "Pemerintah", "alamat": "Jl. Mayjen Prof. Dr. Moestopo No.6", "telepon": "(031) 5501078", "jam_operasional": "24 Jam"},
    {"nama_rs": "RS Siloam Surabaya", "kota": "Surabaya", "provinsi": "Jawa Timur", "kelas": "B", "tipe": "Swasta", "alamat": "Jl. Raya Gubeng No.70", "telepon": "(031) 5031111", "jam_operasional": "24 Jam"},
    {"nama_rs": "RS Universitas Airlangga", "kota": "Surabaya", "provinsi": "Jawa Timur", "kelas": "B", "tipe": "Pemerintah", "alamat": "Jl. Mayjen Prof. Dr. Moestopo No.47", "telepon": "(031) 5020082", "jam_operasional": "24 Jam"},
    {"nama_rs": "RS Sanglah", "kota": "Denpasar", "provinsi": "Bali", "kelas": "A", "tipe": "Pemerintah", "alamat": "Jl. Diponegoro No.1", "telepon": "(0361) 227911", "jam_operasional": "24 Jam"},
    {"nama_rs": "RS Kasih Ibu Denpasar", "kota": "Denpasar", "provinsi": "Bali", "kelas": "B", "tipe": "Swasta", "alamat": "Jl. Teuku Umar No.120", "telepon": "(0361) 223036", "jam_operasional": "24 Jam"},
    {"nama_rs": "RS Dr. Wahidin Sudirohusodo", "kota": "Makassar", "provinsi": "Sulawesi Selatan", "kelas": "A", "tipe": "Pemerintah", "alamat": "Jl. Perintis Kemerdekaan Km.11", "telepon": "(0411) 584677", "jam_operasional": "24 Jam"},
    {"nama_rs": "RS Siloam Makassar", "kota": "Makassar", "provinsi": "Sulawesi Selatan", "kelas": "B", "tipe": "Swasta", "alamat": "Jl. Metro Tanjung Bunga", "telepon": "(0411) 3655555", "jam_operasional": "24 Jam"},
    {"nama_rs": "RS Adam Malik", "kota": "Medan", "provinsi": "Sumatera Utara", "kelas": "A", "tipe": "Pemerintah", "alamat": "Jl. Bunga Lau No.17", "telepon": "(061) 8360381", "jam_operasional": "24 Jam"},
    {"nama_rs": "RS Columbia Asia Medan", "kota": "Medan", "provinsi": "Sumatera Utara", "kelas": "B", "tipe": "Swasta", "alamat": "Jl. Listrik No.2A", "telepon": "(061) 4566368", "jam_operasional": "24 Jam"},
    {"nama_rs": "RS Dr. M. Djamil", "kota": "Padang", "provinsi": "Sumatera Barat", "kelas": "A", "tipe": "Pemerintah", "alamat": "Jl. Perintis Kemerdekaan No.1", "telepon": "(0751) 32371", "jam_operasional": "24 Jam"},
    {"nama_rs": "RS Siloam Palembang", "kota": "Palembang", "provinsi": "Sumatera Selatan", "kelas": "B", "tipe": "Swasta", "alamat": "Jl. Rajawali No.8", "telepon": "(0711) 376767", "jam_operasional": "24 Jam"},
    {"nama_rs": "RS Abdul Moeloek", "kota": "Bandar Lampung", "provinsi": "Lampung", "kelas": "A", "tipe": "Pemerintah", "alamat": "Jl. Dr. Rivai No.6", "telepon": "(0721) 703312", "jam_operasional": "24 Jam"},
    {"nama_rs": "RS Ulin Banjarmasin", "kota": "Banjarmasin", "provinsi": "Kalimantan Selatan", "kelas": "A", "tipe": "Pemerintah", "alamat": "Jl. A. Yani Km.2.5", "telepon": "(0511) 3252180", "jam_operasional": "24 Jam"},
    {"nama_rs": "RS Siloam Balikpapan", "kota": "Balikpapan", "provinsi": "Kalimantan Timur", "kelas": "B", "tipe": "Swasta", "alamat": "Jl. MT Haryono No.165", "telepon": "(0542) 888888", "jam_operasional": "24 Jam"},
    {"nama_rs": "RS Panti Rapih", "kota": "Yogyakarta", "provinsi": "DI Yogyakarta", "kelas": "B", "tipe": "Swasta", "alamat": "Jl. Cik Di Tiro No.30", "telepon": "(0274) 514845", "jam_operasional": "24 Jam"},
    {"nama_rs": "RS Dr. Sardjito", "kota": "Yogyakarta", "provinsi": "DI Yogyakarta", "kelas": "A", "tipe": "Pemerintah", "alamat": "Jl. Kesehatan No.1", "telepon": "(0274) 587333", "jam_operasional": "24 Jam"},
]

CSV_PATH = "data_rumah_sakit.csv"

# ─────────────────────────────────────────────
# FUNGSI LOAD DATA
# ─────────────────────────────────────────────
@st.cache_data
def load_data():
    if os.path.exists(CSV_PATH):
        df = pd.read_csv(CSV_PATH)
    else:
        df = pd.DataFrame(DATA_RS_DEFAULT)
    # Normalisasi kolom
    required_cols = ["nama_rs", "kota", "provinsi", "kelas", "tipe", "alamat", "telepon", "jam_operasional"]
    for col in required_cols:
        if col not in df.columns:
            df[col] = "-"
    return df

def refresh_data():
    st.cache_data.clear()

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🏥 MediCare Insurance")
    st.markdown("---")
    st.markdown("**Menu**")
    page = st.radio(
        "",
        ["🔍 Cari Rumah Sakit", "📋 Semua RS", "⚙️ Admin Panel"],
        label_visibility="collapsed"
    )
    st.markdown("---")
    st.markdown("**Bantuan**")
    st.markdown("📞 Call Center: **1500-123**")
    st.markdown("✉️ cs@medicare-ins.co.id")
    st.markdown("---")
    st.caption("v1.0.0 © 2025 MediCare Insurance")

# ─────────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────────
df = load_data()

# ─────────────────────────────────────────────
# HELPER: Badge Kelas
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
    <p>Temukan rumah sakit rekanan MediCare Insurance di seluruh Indonesia — cashless & terpercaya</p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# STATS
# ─────────────────────────────────────────────
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
# NAVIGASI TABS (selalu tampil, tidak bergantung sidebar)
# ─────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["🔍 Cari Rumah Sakit", "📋 Semua RS", "⚙️ Admin Panel"])

# ─────────────────────────────────────────────
# TAB 1: CARI RUMAH SAKIT
# ─────────────────────────────────────────────
with tab1:
    st.markdown('<div class="search-container">', unsafe_allow_html=True)
    st.markdown('<div class="search-title">🔎 Filter Pencarian</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([3, 3, 2])
    with col1:
        keyword = st.text_input("Nama Rumah Sakit", placeholder="Contoh: Siloam, Hermina...")
    with col2:
        kota_options = ["Semua Kota"] + sorted(df["kota"].dropna().unique().tolist())
        kota_filter = st.selectbox("Kota", kota_options)
    with col3:
        provinsi_options = ["Semua Provinsi"] + sorted(df["provinsi"].dropna().unique().tolist())
        provinsi_filter = st.selectbox("Provinsi", provinsi_options)

    col4, col5 = st.columns([2, 4])
    with col4:
        kelas_options = ["Semua Kelas"] + sorted(df["kelas"].dropna().unique().tolist())
        kelas_filter = st.selectbox("Kelas RS", kelas_options)
    with col5:
        tipe_options = ["Semua Tipe", "Pemerintah", "Swasta"]
        tipe_filter = st.selectbox("Tipe RS", tipe_options)

    st.markdown('</div>', unsafe_allow_html=True)

    # Apply filters
    result = df.copy()
    if keyword:
        result = result[result["nama_rs"].str.contains(keyword, case=False, na=False)]
    if kota_filter != "Semua Kota":
        result = result[result["kota"] == kota_filter]
    if provinsi_filter != "Semua Provinsi":
        result = result[result["provinsi"] == provinsi_filter]
    if kelas_filter != "Semua Kelas":
        result = result[result["kelas"].str.strip().str.upper() == kelas_filter.strip().upper()]
    if tipe_filter != "Semua Tipe":
        result = result[result["tipe"].str.strip().str.lower() == tipe_filter.strip().lower()]

    st.markdown(f"**Menampilkan {len(result)} dari {total_rs} rumah sakit**")
    st.markdown("---")

    if len(result) == 0:
        st.markdown("""
        <div class="no-result">
            <div class="no-result-icon">🔍</div>
            <div class="no-result-text">Rumah sakit tidak ditemukan.<br>Coba ubah kata kunci atau filter pencarian.</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        for _, row in result.iterrows():
            render_rs_card(row)

# ─────────────────────────────────────────────
# TAB 2: SEMUA RS
# ─────────────────────────────────────────────
with tab2:
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

        st.markdown("---")
        st.markdown("### 📤 Upload File CSV Baru")
        st.info("""
        **Format CSV yang dibutuhkan:**
        Kolom wajib: `nama_rs`, `kota`, `provinsi`, `kelas`, `tipe`, `alamat`, `telepon`, `jam_operasional`

        Download template di bawah untuk memulai.
        """)

        template_df = pd.DataFrame(DATA_RS_DEFAULT[:3])
        template_csv = template_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇️ Download Template CSV",
            data=template_csv,
            file_name="template_data_rs.csv",
            mime="text/csv",
        )

        uploaded = st.file_uploader("Upload file CSV baru:", type=["csv"])
        if uploaded:
            try:
                # Coba baca dengan berbagai encoding (utf-8, latin-1, windows-1252)
                raw = uploaded.read()
                new_df = None
                for enc in ["utf-8", "utf-8-sig", "latin-1", "cp1252"]:
                    try:
                        import io
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
                        st.error(f"Kolom wajib tidak ditemukan: {', '.join(missing)}")
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

        st.markdown("---")
        st.markdown("### 🗑️ Reset ke Data Default")
        if st.button("Reset ke Data Hardcode Default", type="secondary"):
            if os.path.exists(CSV_PATH):
                os.remove(CSV_PATH)
            refresh_data()
            st.success("✅ Data berhasil direset ke default.")
            st.rerun()

import streamlit as st
import pandas as pd

# 1. Konfigurasi Halaman
st.set_page_config(
    page_title="Rumah Sunat Anak | Modern & Nyaman", 
    page_icon="🌙", 
    layout="wide"
)

# 2. CSS Kustom - Tema Hijau Sage & Hijau Ketupat
st.markdown("""
    <style>
    /* Background Utama Hijau Sage */
    .stApp { background-color: #B2AC88; } 
    
    /* Judul & Slogan */
    .klinik-title {
        color: #2E473B; text-align: center; font-size: 50px; font-weight: bold;
        text-shadow: 2px 2px #E0E5D9; font-family: 'Verdana', sans-serif;
    }
    .klinik-dalil { color: #2E473B; text-align: center; font-style: italic; font-size: 18px; margin-bottom: 30px; }

    /* BOX HASIL (OUTPUT CARD) - Warna Hijau Ketupat Soft */
    .result-box {
        background-color: #E0E5D9; 
        padding: 25px; 
        border-radius: 15px; 
        border: 3px solid #2E473B;
        margin-top: 20px;
    }
    .result-box h3, .result-box p, .result-box li, .result-box b {
        color: #2E473B !important;
    }

    /* Tabel & Form */
    .stTable { background-color: #E0E5D9 !important; border-radius: 10px; }
    .stTable td, .stTable th { color: #2E473B !important; font-weight: bold !important; }
    
    input, select, [data-baseweb="select"] {
        background-color: #F0F2ED !important;
        color: #2E473B !important;
    }
    label { color: #2E473B !important; font-weight: bold; }

    /* Sidebar Custom */
    [data-testid="stSidebar"] { background-color: #2E473B; }
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] h2 { color: #E0E5D9 !important; }
    </style>
""", unsafe_allow_html=True)

# 3. Data Master Rumah Sunat
data_dokter = {
    "Khitan Reguler": {"dokter": "dr. Ahmad Subarjo", "jadwal": "Senin - Jumat (08:00 - 12:00)"},
    "Khitan Metode Klem": {"dokter": "dr. Hilman Syah", "jadwal": "Setiap Hari (13:00 - 17:00)"},
    "Khitan Metode Stapler": {"dokter": "dr. Yusuf Mansur", "jadwal": "Sabtu & Minggu (09:00 - 15:00)"},
    "Khitan Gemuk (Spesialis)": {"dokter": "dr. Zulkifli, Sp.B", "jadwal": "Selasa & Kamis (15:00 - 18:00)"}
}

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>Menu Utama 🌙</h2>", unsafe_allow_html=True)
    menu = st.radio("Navigasi", ["🏠 Beranda", "📐 Kalkulator Metode", "💊 Panduan Perawatan", "📊 Cek Kuota Massal", "📝 Pendaftaran", "🏢 Tentang Kami"])

# --- HEADER ---
st.markdown("<h1 class='klinik-title'>RUMAH SUNAT ANAK</h1>", unsafe_allow_html=True)
st.markdown("<p class='klinik-dalil'>\"Kesucian (fitrah) itu ada lima: Khitan, mencukur bulu kemaluan, mencabut bulu ketiak, memotong kuku, dan mencukur kumis.\" (HR. Bukhari & Muslim)</p>", unsafe_allow_html=True)

# --- 1. KALKULATOR METODE SUNAT (PENGGANTI DIAGNOSIS) ---
if menu == "📐 Kalkulator Metode":
    st.subheader("Smart Method Selector 📐")
    usia = st.number_input("Usia Anak (Tahun)", 0, 15, 7)
    aktif = st.select_slider("Tingkat Aktivitas Anak", options=["Sangat Tenang", "Normal", "Sangat Aktif"])
    keinginan = st.selectbox("Prioritas Utama", ["Tanpa Jahitan", "Bisa Langsung Mandi", "Penyembuhan Tercepat"])
    
    if st.button("Rekomendasikan Metode ✨"):
        metode = ""
        desc = ""
        if aktif == "Sangat Aktif" or keinginan == "Bisa Langsung Mandi":
            metode = "Metode Klem (Power Clamp)"
            desc = "Sangat aman untuk anak aktif, tanpa perban, dan bisa langsung terkena air."
        elif usia > 10:
            metode = "Metode Stapler"
            desc = "Teknologi terbaru, hasil sangat rapi (estetik), dan proses sangat cepat."
        else:
            metode = "Metode Laser (Electric Cauter)"
            desc = "Metode paling umum, minim perdarahan, namun perlu perawatan perban."
            
        st.markdown(f"""<div class="result-box">
            <h3>Hasil Rekomendasi: {metode}</h3>
            <p><b>Kenapa cocok?</b> {desc}</p>
        </div>""", unsafe_allow_html=True)

# --- 2. PANDUAN PERAWATAN PASCA-SUNAT ---
elif menu == "💊 Panduan Perawatan":
    st.subheader("Post-Op Care Guide 💊")
    hari = st.selectbox("Pilih Fase Penyembuhan:", ["Hari ke-1", "Hari ke-3", "Hari ke-7 (Pelepasan Alat)"])
    
    if hari == "Hari ke-1":
        st.info("Berikan obat pereda nyeri setiap 4-6 jam. Pastikan anak memakai celana sunat yang longgar.")
    elif hari == "Hari ke-3":
        st.warning("Bersihkan area ujung sunat dengan cairan antiseptik secara perlahan menggunakan kassa.")
    else:
        st.success("Waktunya kontrol kembali ke klinik untuk pelepasan klem atau pengecekan luka tahap akhir.")

# --- 3. CEK KUOTA SUNAT MASSAL ---
elif menu == "📊 Cek Kuota Massal":
    st.subheader("Ketersediaan Kuota Khitan 📊")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Kuota Khitan Massal (Juni)", "5/50 Kursi", "-2 Hari Lagi")
    with col2:
        st.metric("Kuota Reguler Hari Ini", "8 Sisa Kuota", "Update 5 Menit Lalu")
    st.progress(10)
    st.write("Segera daftar sebelum kuota periode libur sekolah habis!")

# --- MENU LAINNYA (Daftar & Tentang) ---
elif menu == "📝 Pendaftaran":
    st.subheader("Formulir Pendaftaran Digital 📝")
    with st.form("daftar"):
        nama = st.text_input("Nama Anak")
        metode_fix = st.selectbox("Pilih Paket Sunat", list(data_dokter.keys()))
        if st.form_submit_button("Daftar Sekarang"):
            st.balloons()
            st.markdown(f"<div class='result-box'><b>{nama}</b> berhasil terdaftar untuk <b>{metode_fix}</b> dengan {data_dokter[metode_fix]['dokter']}.</div>", unsafe_allow_html=True)

elif menu == "🏠 Beranda":
    st.subheader("Selamat Datang di Rumah Sunat Anak 🌙")
    st.write("Tempat sunat modern yang mengutamakan kenyamanan psikologis anak dan keamanan medis.")
    st.image("https://cdn-icons-png.flaticon.com/512/2864/2864413.png", width=200)

elif menu == "🏢 Tentang Kami":
    st.subheader("Profil Rumah Sunat")
    st.write("Berdiri sejak 2020, kami telah mengkhitan lebih dari 5.000 anak dengan metode minim nyeri.")
    st.table(pd.DataFrame({
        "Jabatan": ["Kepala Klinik", "Spesialis Bedah", "Admin Keuangan"],
        "Nama": ["dr. Ahmad Subarjo", "dr. Zulkifli, Sp.B", "Siti Aminah"]
    }))
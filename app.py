import streamlit as st
import pandas as pd
from datetime import datetime
import time

# =================================================================
# 1. KONFIGURASI HALAMAN & STATE MANAGEMENT
# =================================================================
st.set_page_config(
    page_title="Rumah Sunat Anak | Pusat Khitan Modern", 
    page_icon="🌙", 
    layout="wide"
)

# Inisialisasi Session State agar data sinkron antar menu
if 'kuota_massal_total' not in st.session_state:
    st.session_state.kuota_massal_total = 50
if 'terdaftar_massal' not in st.session_state:
    st.session_state.terdaftar_massal = 18
if 'kuota_reguler' not in st.session_state:
    st.session_state.kuota_reguler = 12
if 'rekomendasi_metode' not in st.session_state:
    st.session_state.rekomendasi_metode = "Khitan Reguler"
if 'last_submit' not in st.session_state:
    st.session_state.last_submit = None

# =================================================================
# 2. CUSTOM CSS (TEMA HIJAU SAGE & TEKS HITAM)
# =================================================================
st.markdown("""
    <style>
    /* Background Utama */
    .stApp { background-color: #B2AC88; } 
    
    /* Judul Utama dengan Outline */
    .header-style {
        color: white; text-align: center; font-size: 60px; font-weight: bold;
        text-shadow: -3px -3px 0 #000, 3px -3px 0 #000, -3px 3px 0 #000, 3px 3px 0 #000;
        font-family: 'Verdana', sans-serif; margin-bottom: 0px;
    }
    
    .slogan-style {
        color: #1A2E25; text-align: center; font-style: italic; font-size: 18px;
        font-weight: bold; margin-bottom: 30px;
    }

    .subheader-style {
        color: white; font-size: 35px; font-weight: bold;
        text-shadow: -1px -1px 0 #000, 1px -1px 0 #000, -1px 1px 0 #000, 1px 1px 0 #000;
        margin-bottom: 25px; border-left: 10px solid #2E473B; padding-left: 15px;
    }

    /* Box Output Card - Teks Hitam Pekat */
    .result-box {
        background-color: #F7F9F2; padding: 35px; border-radius: 25px; 
        border: 5px solid #2E473B; margin-top: 20px;
        box-shadow: 10px 10px 20px rgba(0,0,0,0.15);
    }
    .result-box h3, .result-box p, .result-box b, .result-box li, .stTable td, .stTable th {
        color: #000000 !important;
    }

    /* Sidebar & Navigation */
    [data-testid="stSidebar"] { background-color: #2E473B; border-right: 3px solid #E0E5D9; }
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] h2 { color: #E0E5D9 !important; }
    
    /* Input Styling */
    label { color: white !important; font-weight: bold; text-shadow: 1px 1px 2px #000; }
    .stButton>button {
        background-color: #2E473B !important; color: white !important;
        border-radius: 10px; font-weight: bold; width: 100%; height: 50px;
    }
    </style>
""", unsafe_allow_html=True)

# =================================================================
# 3. DATA MASTER (DOKTER & ORGANISASI)
# =================================================================
data_dokter_db = [
    {"Nama": "dr. Ahmad Subarjo", "Keahlian": "Kepala Klinik & Ahli Klem"},
    {"Nama": "dr. Zulkifli, Sp.B", "Keahlian": "Spesialis Bedah Umum"},
    {"Nama": "dr. Hilman Syah", "Keahlian": "Dokter Pelaksana Senior"},
    {"Nama": "dr. Yusuf Mansur", "Keahlian": "Spesialis Stapler Estetik"},
    {"Nama": "dr. Ridwan Hakim, Sp.U", "Keahlian": "Konsultan Urologi"},
    {"Nama": "dr. Faisal Anwar", "Keahlian": "Spesialis Sunat Gemuk"},
    {"Nama": "dr. Siti Aminah", "Keahlian": "Kepala Perawat & Nyeri"},
    {"Nama": "dr. Budi Santoso", "Keahlian": "Ahli Bius Tanpa Jarum"}
]

data_organisasi = {
    "Level Eksekutif": [
        {"Jabatan": "Direktur Utama", "Nama": "H. Salim Wijaya, M.M"},
        {"Jabatan": "Wakil Direktur Medis", "Nama": "dr. Ahmad Subarjo"}
    ],
    "Manajemen Operasional": [
        {"Jabatan": "Manajer Operasional", "Nama": "Rina Kartika, S.E"},
        {"Jabatan": "Manajer Keuangan", "Nama": "Anita Sari, Ak."},
        {"Jabatan": "Humas & Kemitraan", "Nama": "Bambang Pamungkas"}
    ],
    "Penunjang Medis": [
        {"Jabatan": "Kepala Farmasi", "Nama": "Apt. Linda Mayasari"},
        {"Jabatan": "IT Support & Digital", "Nama": "Eko Prasetyo, S.Kom"},
        {"Jabatan": "Manajemen Fasilitas", "Nama": "Doni Setiawan"}
    ]
}

# =================================================================
# 4. SIDEBAR NAVIGASI
# =================================================================
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>MENU UTAMA 🌙</h2>", unsafe_allow_html=True)
    menu = st.radio("Pilih Layanan:", [
        "🏠 Beranda Utama", 
        "📐 Kalkulator Metode Smart", 
        "📝 Pendaftaran Digital", 
        "📊 Monitoring Kuota", 
        "💊 Panduan Pasca-Tindakan",
        "🏢 Profil & Struktur RS"
    ])
    st.divider()
    st.sidebar.warning("Layanan IGD Khitan buka 24/7.")

# Header Global
st.markdown("<h1 class='header-style'>RUMAH SUNAT ANAK</h1>", unsafe_allow_html=True)
st.markdown("<p class='slogan-style'>\"Kesucian (fitrah) itu ada lima: Khitan...\" (HR. Bukhari & Muslim)</p>", unsafe_allow_html=True)

# =================================================================
# 5. IMPLEMENTASI FITUR
# =================================================================

# --- MENU: BERANDA ---
if menu == "🏠 Beranda Utama":
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("https://cdn-icons-png.flaticon.com/512/3774/3774299.png", use_container_width=True)
        st.markdown("<h2 style='text-align:center; color:white;'>Selamat Datang</h2>", unsafe_allow_html=True)
        st.write("""
            <div style='text-align: center; color: #1A2E25; font-weight: 500; font-size: 1.1em;'>
                Kami menyediakan layanan khitan modern dengan pendekatan psikologis anak yang ramah dan aman. 
                Nikmati fasilitas ruang tindakan bertema dan teknologi terbaru tanpa jahitan.
            </div>
        """, unsafe_allow_html=True)

# --- MENU: KALKULATOR (SINKRON KE DAFTAR) ---
elif menu == "📐 Kalkulator Metode Smart":
    st.markdown("<h2 class='subheader-style'>Smart Method Selector 📐</h2>", unsafe_allow_html=True)
    
    with st.container():
        c1, c2 = st.columns(2)
        with c1:
            usia_k = st.number_input("Berapa usia anak saat ini?", 0, 18, 7)
            kondisi_k = st.selectbox("Kondisi Fisik Khusus?", ["Normal", "Gemuk", "Phimosis"])
        with c2:
            aktif_k = st.select_slider("Tingkat Aktivitas Anak", options=["Tenang", "Normal", "Sangat Aktif"])
            prioritas = st.selectbox("Apa prioritas Anda?", ["Hasil Estetik", "Bisa Mandi Langsung", "Ekonomis"])

    if st.button("Analisis Rekomendasi Medis ✨"):
        with st.spinner("Menganalisis data..."):
            time.sleep(1)
            # Logika Pemilihan
            if kondisi_k == "Gemuk":
                st.session_state.rekomendasi_metode = "Khitan Gemuk (Spesialis)"
                hasil_txt = "Memerlukan teknik bedah minor khusus untuk hasil maksimal."
            elif aktif_k == "Sangat Aktif" or prioritas == "Bisa Mandi Langsung":
                st.session_state.rekomendasi_metode = "Khitan Metode Klem"
                hasil_txt = "Alat klem melindungi luka, anak bisa langsung sekolah dan mandi."
            elif usia_k > 10 or prioritas == "Hasil Estetik":
                st.session_state.rekomendasi_metode = "Khitan Metode Stapler"
                hasil_txt = "Teknologi sekali pakai, hasil sangat rapi dan penyembuhan cepat."
            else:
                st.session_state.rekomendasi_metode = "Khitan Reguler"
                hasil_txt = "Metode laser cauter standar yang aman dan terjangkau."
            
            st.markdown(f"""
                <div class="result-box">
                    <h3>Metode Disarankan: {st.session_state.rekomendasi_metode}</h3>
                    <p><b>Catatan Medis:</b> {hasil_txt}</p>
                    <p><i>Data ini telah diteruskan ke bagian Pendaftaran.</i></p>
                </div>
            """, unsafe_allow_html=True)

# --- MENU: PENDAFTARAN (AUTO-FILL) ---
elif menu == "📝 Pendaftaran Digital":
    st.markdown("<h2 class='subheader-style'>Pendaftaran Pasien Baru 📝</h2>", unsafe_allow_html=True)
    
    metode_opt = [d['Nama'] for d in data_dokter_db] # Error handling: data_dokter_db keys
    # Map rekomendasi ke list pilihan formulir
    map_metode = {
        "Khitan Reguler": 0, "Khitan Metode Klem": 2, 
        "Khitan Metode Stapler": 3, "Khitan Gemuk (Spesialis)": 5
    }
    default_idx = map_metode.get(st.session_state.rekomendasi_metode, 0)

    with st.form("form_daftar"):
        c1, c2 = st.columns(2)
        with c1:
            nama_p = st.text_input("Nama Lengkap Anak")
            tgl_p = st.date_input("Rencana Tanggal Tindakan")
        with c2:
            ortu_p = st.text_input("Nama Orang Tua")
            layanan_p = st.selectbox("Kategori Layanan", ["Reguler/Privat", "Massal/Promo"])
        
        # SINKRONISASI OTOMATIS
        paket_p = st.selectbox("Paket Metode (Sesuai Rekomendasi Kalkulator)", 
                               ["Khitan Reguler", "Khitan Laser", "Khitan Metode Klem", "Khitan Metode Stapler", "Khitan Urologi", "Khitan Gemuk (Spesialis)"],
                               index=default_idx)
        
        st.divider()
        if st.form_submit_button("KONFIRMASI PENDAFTARAN ✨"):
            if nama_p:
                st.balloons() # EFEK VISUAL BALON
                if layanan_p == "Reguler/Privat": st.session_state.kuota_reguler -= 1
                else: st.session_state.terdaftar_massal += 1
                
                st.markdown(f"""
                    <div class="result-box">
                        <h3>✅ Pendaftaran Berhasil!</h3>
                        <p><b>Nama:</b> {nama_p} | <b>Paket:</b> {paket_p}</p>
                        <p>Silahkan datang pada {tgl_p.strftime('%d %m %Y')} jam 08:00 WIB.</p>
                    </div>
                """, unsafe_allow_html=True)

# --- MENU: MONITORING KUOTA ---
elif menu == "📊 Monitoring Kuota":
    st.markdown("<h2 class='subheader-style'>Cek Ketersediaan Kuota 📊</h2>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Pendaftar Sunat Massal", f"{st.session_state.terdaftar_massal}/50", "Terisi")
    with col2:
        st.metric("Sisa Slot Reguler Hari Ini", f"{st.session_state.kuota_reguler}", "Tersedia")
    st.progress(int((st.session_state.terdaftar_massal / 50) * 100))

# --- MENU: PROFIL & STRUKTUR (EKSPANSI BESAR) ---
elif menu == "🏢 Profil & Struktur RS":
    st.markdown("<h2 class='subheader-style'>Mengenal Rumah Sunat Anak 🏢</h2>", unsafe_allow_html=True)
    
    # 1. Narasi Profil Panjang
    st.markdown("""
        <div class="result-box">
            <h3>Sejarah & Filosofi</h3>
            <p>Didirikan pada 15 April 2015, <b>Rumah Sunat Anak</b> bermula dari visi dr. Ahmad Subarjo untuk menghadirkan layanan khitan yang manusiawi. Kami percaya bahwa pengalaman khitan yang positif akan membangun rasa percaya diri pada anak. Dengan filosofi <i>"Modern, Syar'i, & Nyaman"</i>, kami mengintegrasikan standar sterilitas rumah sakit dengan kenyamanan layaknya di rumah sendiri.</p>
            <p>Hingga tahun 2026, kami telah mengoperasikan 5 cabang di seluruh Indonesia dan mengkhitan lebih dari 20.000 anak. Kami terus berinovasi dengan alat-alat disposabel (sekali pakai) untuk menjamin keamanan 100% bagi setiap pasien.</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 2. Layout Kolom: List Dokter di Kiri
    col_kiri, col_kanan = st.columns([1, 2])
    
    with col_kiri:
        st.markdown("<h3 style='color:white;'>📋 Tim Dokter Spesialis</h3>", unsafe_allow_html=True)
        st.table(pd.DataFrame(data_dokter_db))
        st.info("Seluruh dokter kami telah tersertifikasi oleh Perhimpunan Khitan Indonesia.")

    with col_kanan:
        st.markdown("<h3 style='color:white;'>🏆 Visi & Keunggulan</h3>", unsafe_allow_html=True)
        st.markdown("""
            <div class="result-box" style="margin-top:0px;">
                <ul>
                    <li><b>Visi:</b> Menjadi pusat khitan modern referensi nasional tahun 2030.</li>
                    <li><b>Keunggulan 1:</b> Tanpa Jarum Suntik (Teknologi Needle-Free Injection).</li>
                    <li><b>Keunggulan 2:</b> Tanpa Jahit & Tanpa Perban (Metode Klem & Stapler).</li>
                    <li><b>Keunggulan 3:</b> Kontrol pasca-khitan gratis hingga sembuh total.</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

    # 3. Struktur Organisasi Luas (Di Bawah Profil)
    st.markdown("<h3 style='color:white;'>🏛️ Struktur Organisasi & Manajemen</h3>", unsafe_allow_html=True)
    
    for div_name, div_data in data_organisasi.items():
        with st.expander(f"Buka Detail: {div_name}"):
            st.table(pd.DataFrame(div_data))

# --- MENU: PANDUAN ---
elif menu == "💊 Panduan Pasca-Tindakan":
    st.markdown("<h2 class='subheader-style'>Post-Op Care Guide 💊</h2>", unsafe_allow_html=True)
    opsi_p = st.radio("Fase Penyembuhan:", ["24 Jam Pertama", "Hari 2 - 5", "Hari 7+ (Kontrol)"])
    
    if opsi_p == "24 Jam Pertama":
        st.markdown("<div class='result-box'><b>Fokus:</b> Istirahat total. Berikan obat pereda nyeri tiap 6 jam.</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='result-box'><b>Fokus:</b> Jaga kebersihan area. Lakukan aktivitas ringan saja.</div>", unsafe_allow_html=True)
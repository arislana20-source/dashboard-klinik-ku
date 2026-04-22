import streamlit as st
import pandas as pd
from datetime import datetime
import time

# =================================================================
# 1. KONFIGURASI HALAMAN
# =================================================================
st.set_page_config(
    page_title="Rumah Sunat Anak | Pusat Khitan Modern", 
    page_icon="🌙", 
    layout="wide"
)

# Inisialisasi Session State (Tanpa Kuota Massal)
if 'kuota_reguler' not in st.session_state:
    st.session_state.kuota_reguler = 15
if 'rekomendasi_paket' not in st.session_state:
    st.session_state.rekomendasi_paket = "Sunat Laser"

# =================================================================
# 2. CSS KUSTOM (STRICT CONTRAST & VERTICAL LAYOUT)
# =================================================================
st.markdown("""
    <style>
    .stApp { background-color: #B2AC88; } 
    
    .header-container {
        text-align: center;
        padding: 30px 10px;
        background-color: rgba(46, 71, 59, 0.1);
        border-radius: 20px;
        margin-bottom: 10px;
    }
    .header-style {
        color: white; font-size: clamp(40px, 8vw, 65px); font-weight: bold;
        text-shadow: -3px -3px 0 #000, 3px -3px 0 #000, -3px 3px 0 #000, 3px 3px 0 #000;
        font-family: 'Verdana', sans-serif;
        line-height: 1.1;
    }
    .slogan-style {
        color: #1A2E25; font-size: 19px; font-weight: 600;
        font-style: italic; margin-top: 15px; display: block;
    }

    .subheader-style {
        color: white; font-size: 30px; font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        border-bottom: 5px solid #2E473B;
        padding-bottom: 10px; margin-bottom: 20px;
    }

    .result-box {
        background-color: #F7F9F2; padding: 30px; border-radius: 20px; 
        border: 4px solid #2E473B; margin-top: 15px;
        box-shadow: 8px 8px 0px #2E473B;
    }
    .result-box h3 { color: #2E473B !important; font-weight: 800; }
    .result-box p, .result-box b, .result-box li, .result-box span {
        color: #000000 !important; font-size: 17px; line-height: 1.6;
    }

    .stTable { background-color: #F7F9F2 !important; border-radius: 15px; }
    .stTable td, .stTable th { color: #000000 !important; }

    [data-testid="stSidebar"] { background-color: #2E473B; }
    [data-testid="stSidebar"] .stRadio label { color: #E0E5D9 !important; font-size: 17px !important; }
    
    .stButton>button {
        background-color: #2E473B !important; color: white !important;
        border-radius: 12px; font-weight: bold; height: 50px; width: 100%;
        border: 2px solid white;
    }
    label { color: white !important; font-size: 17px !important; text-shadow: 1px 1px 2px #000; }
    </style>
""", unsafe_allow_html=True)

# =================================================================
# 3. DATA MASTER
# =================================================================
data_dokter_list = [
    {"Nama": "dr. Ahmad Subarjo", "Keahlian": "Kepala Klinik & Ahli Klem"},
    {"Nama": "dr. Zulkifli, Sp.B", "Keahlian": "Spesialis Bedah & Sunat Gunting"},
    {"Nama": "dr. Hilman Syah", "Keahlian": "Dokter Pelaksana Laser Cauter"},
    {"Nama": "dr. Yusuf Mansur", "Keahlian": "Spesialis Stapler Estetik"},
    {"Nama": "dr. Faisal Anwar", "Keahlian": "Spesialis Sunat Gemuk"}
]

org_manajemen = {
    "Pimpinan": [{"Jabatan": "Direktur", "Nama": "H. Salim Wijaya, M.M"}],
    "Medis": [{"Jabatan": "Kepala Perawat", "Nama": "Ns. Siti Aminah, S.Kep"}],
    "Admin": [{"Jabatan": "Manajer Keuangan", "Nama": "Anita Sari, A.Md"}]
}

# =================================================================
# 4. SIDEBAR MENU
# =================================================================
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>NAVIGASI KLINIK 🌙</h2>", unsafe_allow_html=True)
    menu = st.radio("Pilih Halaman:", [
        "🏠 Beranda Utama", 
        "📐 Kalkulator Paket Sunat", 
        "📝 Pendaftaran Digital", 
        "📊 Monitoring Kuota", 
        "💊 Panduan Pasca-Khitan",
        "🏢 Profil Lengkap RS"
    ])

# =================================================================
# 5. HEADER DINAMIS (Slogan Hanya di Beranda)
# =================================================================
if menu == "🏠 Beranda Utama":
    st.markdown(f"""
        <div class="header-container">
            <h1 class="header-style">RUMAH SUNAT ANAK</h1>
            <span class="slogan-style">
                "Kesucian (fitrah) itu ada lima: Khitan, mencukur bulu kemaluan, mencabut bulu ketiak, memotong kuku, dan mencukur kumis."<br>
                <b>(HR. Bukhari & Muslim)</b>
            </span>
        </div>
    """, unsafe_allow_html=True)
else:
    st.markdown(f"""
        <div class="header-container">
            <h1 class="header-style">RUMAH SUNAT ANAK</h1>
        </div>
    """, unsafe_allow_html=True)

# =================================================================
# 6. IMPLEMENTASI FITUR
# =================================================================

# --- BERANDA ---
if menu == "🏠 Beranda Utama":
    st.markdown("<h2 class='subheader-style'>Selamat Datang</h2>", unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/3774/3774299.png", width=250)
    st.markdown("""
        <div class="result-box">
            <h3>Pusat Khitan Modern Terpercaya</h3>
            <p>Rumah Sunat Anak menyediakan berbagai metode khitan terkini yang disesuaikan dengan kebutuhan anatomi dan aktivitas anak Anda.</p>
        </div>
    """, unsafe_allow_html=True)

# --- KALKULATOR PAKET (REVISI: SESUAI PAKET) ---
elif menu == "📐 Kalkulator Paket Sunat":
    st.markdown("<h2 class='subheader-style'>Penentuan Paket Sunat 📐</h2>", unsafe_allow_html=True)
    
    usia = st.number_input("Usia Pasien", 0, 18, 7)
    kondisi = st.selectbox("Kondisi Anatomi", ["Normal", "Fimosis (Perlekatan)", "Gemuk (Micro Penis)"])
    aktif = st.select_slider("Tingkat Aktivitas", options=["Sangat Tenang", "Normal", "Sangat Aktif"])
    
    if st.button("Cek Rekomendasi Paket ✨"):
        if kondisi == "Gemuk (Micro Penis)":
            st.session_state.rekomendasi_paket = "Sunat Gunting (Konvensional/Bedah)"
            txt = "Memerlukan teknik bedah manual untuk koreksi prepusium yang lebih akurat."
        elif aktif == "Sangat Aktif":
            st.session_state.rekomendasi_paket = "Sunat Metode Klem"
            txt = "Alat klem melindungi luka sehingga aman untuk anak yang tidak bisa diam."
        elif usia > 11:
            st.session_state.rekomendasi_paket = "Sunat Metode Stapler"
            txt = "Sangat direkomendasikan untuk remaja karena hasil estetik yang sangat rapi."
        else:
            st.session_state.rekomendasi_paket = "Sunat Laser (Flashcutter)"
            txt = "Metode laser cauter yang cepat kering dan minim perdarahan."

        st.markdown(f"""
            <div class="result-box">
                <h3>Paket Disarankan: {st.session_state.rekomendasi_paket}</h3>
                <p><b>Analisis:</b> {txt}</p>
            </div>
        """, unsafe_allow_html=True)

# --- PENDAFTARAN (REVISI: OPSI METODE) ---
elif menu == "📝 Pendaftaran Digital":
    st.markdown("<h2 class='subheader-style'>Formulir Pendaftaran 📝</h2>", unsafe_allow_html=True)
    
    list_metode = ["Sunat Laser (Flashcutter)", "Sunat Gunting (Konvensional/Bedah)", "Sunat Metode Klem", "Sunat Metode Stapler"]
    try:
        idx_def = list_metode.index(st.session_state.rekomendasi_paket)
    except:
        idx_def = 0

    with st.form("regis_form"):
        nama = st.text_input("Nama Lengkap Pasien")
        ortu = st.text_input("Nama Orang Tua")
        # Pilihan Paket sesuai revisi
        paket_pilih = st.selectbox("Pilih Paket Metode:", list_metode, index=idx_def)
        tgl = st.date_input("Tanggal Tindakan")
        
        if st.form_submit_button("SUBMIT DATA ✨"):
            if nama:
                st.balloons()
                st.session_state.kuota_reguler -= 1
                st.markdown(f"""
                    <div class="result-box">
                        <h3>✅ Berhasil Terdaftar!</h3>
                        <p>Pasien <b>{nama}</b> dijadwalkan untuk <b>{paket_pilih}</b>.</p>
                    </div>
                """, unsafe_allow_html=True)

# --- MONITORING KUOTA (REVISI: REGULER SAJA) ---
elif menu == "📊 Monitoring Kuota":
    st.markdown("<h2 class='subheader-style'>Cek Ketersediaan Slot Reguler 📊</h2>", unsafe_allow_html=True)
    st.metric("Sisa Kuota Reguler Hari Ini", f"{st.session_state.kuota_reguler} Kursi", "Update Real-time")
    st.progress(st.session_state.kuota_reguler * 6)
    st.info("Kuota ini mencakup semua metode (Laser, Gunting, Klem, Stapler).")

# --- PANDUAN (TEKS HITAM JELAS) ---
elif menu == "💊 Panduan Pasca-Khitan":
    st.markdown("<h2 class='subheader-style'>Post-Op Care Guide 💊</h2>", unsafe_allow_html=True)
    fase = st.selectbox("Pilih Fase:", ["24 Jam Pertama", "Hari 2 - 5", "Kontrol"])
    
    st.markdown(f"""
        <div class="result-box">
            <h3>Instruksi {fase}</h3>
            <p>1. Pastikan area luka tetap kering (kecuali metode klem/stapler).<br>
            2. Minum obat pereda nyeri secara teratur.<br>
            3. Gunakan celana khitan pelindung.</p>
        </div>
    """, unsafe_allow_html=True)

# --- PROFIL & STRUKTUR (LAYOUT RAPI) ---
elif menu == "🏢 Profil Lengkap RS":
    st.markdown("<h2 class='subheader-style'>Tentang Rumah Sunat Anak 🏢</h2>", unsafe_allow_html=True)
    
    st.markdown("""
        <div class="result-box">
            <h3>Visi & Misi</h3>
            <p>Menjadi pusat rujukan khitan modern yang aman dan ramah anak. Kami menggunakan teknologi medis sekali pakai (single-use) untuk menjamin keamanan 100%.</p>
        </div>
    """, unsafe_allow_html=True)

    # Struktur di bawah visi misi
    st.markdown("<h3 style='color:white; margin-top:20px;'>🏛️ Struktur Organisasi</h3>", unsafe_allow_html=True)
    for k, v in org_manajemen.items():
        with st.expander(f"Detail Divisi: {k}"):
            st.table(pd.DataFrame(v))

    # List Dokter
    st.markdown("<h3 style='color:white; margin-top:20px;'>👨‍⚕️ Tim Dokter Spesialis</h3>", unsafe_allow_html=True)
    st.table(pd.DataFrame(data_dokter_list))
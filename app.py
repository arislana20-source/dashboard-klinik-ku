import streamlit as st
import pandas as pd
from datetime import datetime

# 1. Konfigurasi Halaman
st.set_page_config(
    page_title="Rumah Sunat Anak | Modern & Nyaman", 
    page_icon="🌙", 
    layout="wide"
)

# --- 2. INISIALISASI SESSION STATE ---
if 'kuota_massal_total' not in st.session_state:
    st.session_state.kuota_massal_total = 50
if 'terdaftar_massal' not in st.session_state:
    st.session_state.terdaftar_massal = 5
if 'kuota_reguler' not in st.session_state:
    st.session_state.kuota_reguler = 8
# State untuk menyimpan rekomendasi metode
if 'rekomendasi_user' not in st.session_state:
    st.session_state.rekomendasi_user = "Khitan Reguler" 

# 3. CSS Kustom
st.markdown("""
    <style>
    .stApp { background-color: #B2AC88; } 
    .header-style {
        color: white; text-align: center; font-size: 55px; font-weight: bold;
        text-shadow: -2px -2px 0 #000, 2px -2px 0 #000, -2px 2px 0 #000, 2px 2px 0 #000;
        font-family: 'Verdana', sans-serif;
    }
    .subheader-style {
        color: white; font-size: 30px; font-weight: bold;
        text-shadow: -1px -1px 0 #000, 1px -1px 0 #000, -1px 1px 0 #000, 1px 1px 0 #000;
    }
    .result-box {
        background-color: #F7F9F2; padding: 25px; border-radius: 15px; 
        border: 3px solid #2E473B; margin-top: 20px; color: black !important;
    }
    .result-box h3, .result-box p, .result-box b { color: black !important; }
    [data-testid="stSidebar"] { background-color: #2E473B; }
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] h2 { color: #E0E5D9 !important; }
    .stTable { background-color: #F7F9F2 !important; color: black !important; }
    label { color: white !important; font-weight: bold; text-shadow: 1px 1px 1px #000; }
    </style>
""", unsafe_allow_html=True)

# 4. Data Master
data_metode = {
    "Khitan Reguler": {"dokter": "dr. Ahmad Subarjo"},
    "Khitan Metode Klem": {"dokter": "dr. Hilman Syah"},
    "Khitan Metode Stapler": {"dokter": "dr. Yusuf Mansur"},
    "Khitan Gemuk (Spesialis)": {"dokter": "dr. Zulkifli, Sp.B"}
}

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>Menu Utama 🌙</h2>", unsafe_allow_html=True)
    menu = st.radio("Navigasi", ["🏠 Beranda", "📊 Cek Kuota", "📐 Kalkulator Metode", "📝 Pendaftaran", "💊 Panduan Perawatan", "🏢 Tentang Kami"])

st.markdown("<h1 class='header-style'>RUMAH SUNAT ANAK</h1>", unsafe_allow_html=True)

# --- LOGIKA MENU ---

if menu == "🏠 Beranda":
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div style='text-align: center;'><h2 style='color: white; text-shadow: 1px 1px 2px #000;'>Selamat Datang di Rumah Sunat Anak 🌙</h2></div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.image("https://cdn-icons-png.flaticon.com/512/3774/3774299.png", use_container_width=True)

elif menu == "📊 Cek Kuota":
    st.markdown("<h2 class='subheader-style'>Status Kuota 📊</h2>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    col1.metric("Kuota Massal", f"{st.session_state.terdaftar_massal}/{st.session_state.kuota_massal_total}")
    col2.metric("Sisa Reguler", f"{st.session_state.kuota_reguler} Kursi")

elif menu == "📐 Kalkulator Metode":
    st.markdown("<h2 class='subheader-style'>Smart Method Selector 📐</h2>", unsafe_allow_html=True)
    usia = st.number_input("Usia Anak", 0, 15, 7)
    aktif = st.select_slider("Aktivitas Anak", options=["Tenang", "Normal", "Aktif"])
    
    if st.button("Cek Rekomendasi ✨"):
        # Logika pemilihan metode
        if aktif == "Aktif":
            st.session_state.rekomendasi_user = "Khitan Metode Klem"
        elif usia > 10:
            st.session_state.rekomendasi_user = "Khitan Metode Stapler"
        else:
            st.session_state.rekomendasi_user = "Khitan Reguler"
            
        st.markdown(f"""<div class="result-box">
            <h3>Rekomendasi: {st.session_state.rekomendasi_user}</h3>
            <p>Metode ini telah disimpan. Silahkan lanjut ke menu <b>Pendaftaran</b>.</p>
        </div>""", unsafe_allow_html=True)

elif menu == "📝 Pendaftaran":
    st.markdown("<h2 class='subheader-style'>Pendaftaran Digital 📝</h2>", unsafe_allow_html=True)
    
    # Mencari index metode yang direkomendasikan agar otomatis terpilih
    list_metode = list(data_metode.keys())
    default_index = list_metode.index(st.session_state.rekomendasi_user)
    
    with st.form("daftar_form"):
        nama = st.text_input("Nama Anak")
        jenis_layanan = st.selectbox("Jenis Layanan", ["Khitan Reguler (Harian)", "Khitan Massal (Promo)"])
        # Pilihan paket otomatis menyesuaikan hasil kalkulator
        metode_fix = st.selectbox("Paket Metode (Otomatis Terpilih)", list_metode, index=default_index)
        submit = st.form_submit_button("Konfirmasi")
        
        if submit and nama:
            success = False
            if jenis_layanan == "Khitan Reguler (Harian)" and st.session_state.kuota_reguler > 0:
                st.session_state.kuota_reguler -= 1
                success = True
            elif jenis_layanan == "Khitan Massal (Promo)" and st.session_state.terdaftar_massal < st.session_state.kuota_massal_total:
                st.session_state.terdaftar_massal += 1
                success = True
            
            if success:
                st.snow() # Efek bintang melayang
                st.markdown(f"<div class='result-box'><h3>✅ Berhasil!</h3><p>{nama} terdaftar di paket {metode_fix}.</p></div>", unsafe_allow_html=True)

elif menu == "🏢 Tentang Kami":
    st.markdown("<h2 class='subheader-style'>Profil Klinik 🏢</h2>", unsafe_allow_html=True)
    st.markdown("<div class='result-box'><p>Berdiri sejak 2015, melayani dengan hati.</p></div>", unsafe_allow_html=True)
    st.markdown("<h3 style='color:white;'>Daftar 8 Dokter Spesialis</h3>", unsafe_allow_html=True)
    df = pd.DataFrame({
        "Nama Dokter": ["dr. Ahmad", "dr. Zulkifli", "dr. Hilman", "dr. Yusuf", "dr. Ridwan", "dr. Faisal", "dr. Siti", "dr. Budi"],
        "Keahlian": ["Kepala Klinik", "Bedah Umum", "Klem Senior", "Stapler", "Urologi", "Sunat Gemuk", "Nyeri", "Bius"]
    })
    st.table(df) # Tabel dengan teks hitam agar mudah dibaca
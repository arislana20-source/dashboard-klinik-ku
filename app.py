import streamlit as st
import pandas as pd
from datetime import datetime

# 1. Konfigurasi Halaman
st.set_page_config(
    page_title="Rumah Sunat Anak | Modern & Nyaman", 
    page_icon="🌙", 
    layout="wide"
)

# --- 2. INISIALISASI KUOTA (Session State) ---
if 'kuota_massal_total' not in st.session_state:
    st.session_state.kuota_massal_total = 50
if 'terdaftar_massal' not in st.session_state:
    st.session_state.terdaftar_massal = 5
if 'kuota_reguler' not in st.session_state:
    st.session_state.kuota_reguler = 8

# 3. CSS Kustom
st.markdown("""
    <style>
    .stApp { background-color: #B2AC88; } 
    
    .header-style {
        color: white; 
        text-align: center; 
        font-size: 55px; 
        font-weight: bold;
        text-shadow: -2px -2px 0 #000, 2px -2px 0 #000, -2px 2px 0 #000, 2px 2px 0 #000;
        font-family: 'Verdana', sans-serif;
        margin-bottom: 10px;
    }
    
    .subheader-style {
        color: white;
        font-size: 30px;
        font-weight: bold;
        text-shadow: -1px -1px 0 #000, 1px -1px 0 #000, -1px 1px 0 #000, 1px 1px 0 #000;
        margin-bottom: 15px;
    }

    .result-box {
        background-color: #F7F9F2; 
        padding: 25px; 
        border-radius: 15px; 
        border: 3px solid #2E473B;
        margin-top: 20px;
    }
    /* Warna teks hitam di dalam box agar tidak bertabrakan dengan background */
    .result-box h3, .result-box p, .result-box b, .result-box li, .result-box td {
        color: #000000 !important;
    }

    [data-testid="stSidebar"] { background-color: #2E473B; }
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] h2 { color: #E0E5D9 !important; }
    
    label { color: #FFFFFF !important; font-weight: bold; text-shadow: 1px 1px 1px #000; }
    
    /* Memastikan tabel di menu Tentang Kami berwarna hitam teksnya */
    .stTable { background-color: #F7F9F2 !important; color: #000000 !important; }
    </style>
""", unsafe_allow_html=True)

# 4. Data Master Dokter
data_metode = {
    "Khitan Reguler": {"dokter": "dr. Ahmad Subarjo", "jadwal": "Senin - Jumat"},
    "Khitan Metode Klem": {"dokter": "dr. Hilman Syah", "jadwal": "Setiap Hari"},
    "Khitan Metode Stapler": {"dokter": "dr. Yusuf Mansur", "jadwal": "Sabtu & Minggu"},
    "Khitan Gemuk (Spesialis)": {"dokter": "dr. Zulkifli, Sp.B", "jadwal": "Selasa & Kamis"}
}

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>Menu Utama 🌙</h2>", unsafe_allow_html=True)
    menu = st.radio("Navigasi", ["🏠 Beranda", "📊 Cek Kuota", "📝 Pendaftaran", "📐 Kalkulator Metode", "💊 Panduan Perawatan", "🏢 Tentang Kami"])

st.markdown("<h1 class='header-style'>RUMAH SUNAT ANAK</h1>", unsafe_allow_html=True)

# --- LOGIKA MENU ---

if menu == "🏠 Beranda":
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
        <div style='text-align: center;'>
            <h2 style='color: #FFFFFF; text-shadow: 1px 1px 2px #000;'>Selamat Datang di Rumah Sunat Anak 🌙</h2>
            <p style='font-size: 18px; color: #000000; font-style: italic; font-weight: bold;'>
                "Kesucian (fitrah) itu ada lima: Khitan, mencukur bulu kemaluan, mencabut bulu ketiak, memotong kuku, dan mencukur kumis." 
                <br><b>(HR. Bukhari & Muslim)</b>
            </p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.image("https://cdn-icons-png.flaticon.com/512/3774/3774299.png", use_container_width=True)

elif menu == "📊 Cek Kuota":
    st.markdown("<h2 class='subheader-style'>Status Ketersediaan Kuota 📊</h2>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Kuota Khitan Massal", f"{st.session_state.terdaftar_massal}/{st.session_state.kuota_massal_total}")
    with col2:
        st.metric("Sisa Kuota Reguler", f"{st.session_state.kuota_reguler} Kursi")
    st.progress(int((st.session_state.terdaftar_massal / st.session_state.kuota_massal_total) * 100))

elif menu == "📝 Pendaftaran":
    st.markdown("<h2 class='subheader-style'>Formulir Pendaftaran Digital 📝</h2>", unsafe_allow_html=True)
    with st.form("daftar_form"):
        nama = st.text_input("Nama Lengkap Anak")
        jenis_layanan = st.selectbox("Jenis Layanan", ["Khitan Reguler (Harian)", "Khitan Massal (Promo)"])
        metode_fix = st.selectbox("Pilih Paket Metode", list(data_metode.keys()))
        tgl_rencana = st.date_input("Pilih Tanggal Kedatangan", min_value=datetime.now())
        submit = st.form_submit_button("Konfirmasi Pendaftaran")
        
        if submit and nama:
            success = False
            if jenis_layanan == "Khitan Reguler (Harian)" and st.session_state.kuota_reguler > 0:
                st.session_state.kuota_reguler -= 1
                success = True
            elif jenis_layanan == "Khitan Massal (Promo)" and st.session_state.terdaftar_massal < st.session_state.kuota_massal_total:
                st.session_state.terdaftar_massal += 1
                success = True
            
            if success:
                # EFEK BINTANG MELAYANG (Menggunakan st.snow sebagai alternatif bintang)
                st.snow()
                st.markdown(f"""<div class="result-box">
                    <h3>✅ Pendaftaran Berhasil!</h3>
                    <p><b>Nama:</b> {nama}</p>
                    <p><b>Dokter:</b> {data_metode[metode_fix]['dokter']}</p>
                    <p><b>Jadwal:</b> {tgl_rencana.strftime('%d %B %Y')}</p>
                </div>""", unsafe_allow_html=True)

# --- FITUR KALKULATOR METODE (DIKEMBALIKAN) ---
elif menu == "📐 Kalkulator Metode":
    st.markdown("<h2 class='subheader-style'>Smart Method Selector 📐</h2>", unsafe_allow_html=True)
    usia = st.number_input("Usia Anak (Tahun)", 0, 15, 7)
    aktif = st.select_slider("Tingkat Aktivitas Anak", options=["Sangat Tenang", "Normal", "Sangat Aktif"])
    
    if st.button("Rekomendasikan Metode ✨"):
        if aktif == "Sangat Aktif":
            metode, desc = "Metode Klem", "Sangat aman untuk anak aktif, tanpa perban."
        elif usia > 10:
            metode, desc = "Metode Stapler", "Hasil sangat rapi dan estetik untuk usia remaja."
        else:
            metode, desc = "Metode Laser", "Metode umum yang minim perdarahan."
            
        st.markdown(f"""<div class="result-box">
            <h3>Hasil: {metode}</h3>
            <p>{desc}</p>
        </div>""", unsafe_allow_html=True)

elif menu == "💊 Panduan Perawatan":
    st.markdown("<h2 class='subheader-style'>Post-Op Care Guide 💊</h2>", unsafe_allow_html=True)
    fase = st.selectbox("Pilih Fase:", ["Fase 1", "Fase 2", "Fase 3"])
    st.markdown(f"""<div class="result-box"><h3>{fase}</h3><p>Ikuti instruksi dokter dengan teliti.</p></div>""", unsafe_allow_html=True)

elif menu == "🏢 Tentang Kami":
    st.markdown("<h2 class='subheader-style'>Profil & Sejarah Klinik 🏢</h2>", unsafe_allow_html=True)
    st.markdown("""<div class="result-box">
        <p><b>Sejarah:</b> Didirikan tahun 2015 untuk memberikan pengalaman khitan tanpa trauma bagi anak-anak Indonesia.</p>
    </div>""", unsafe_allow_html=True)
    
    # DAFTAR 8 DOKTER (TEKS HITAM)
    st.markdown("<h3 style='color:white; text-shadow:1px 1px #000;'>Tenaga Medis Ahli</h3>", unsafe_allow_html=True)
    dokter_list = pd.DataFrame({
        "Nama Tenaga Medis": ["dr. Ahmad Subarjo", "dr. Zulkifli, Sp.B", "dr. Hilman Syah", "dr. Yusuf Mansur", "dr. Ridwan Hakim", "dr. Faisal Anwar", "dr. Siti Aminah", "dr. Budi Santoso"],
        "Spesialisasi": ["Kepala Klinik", "Spesialis Bedah", "Pelaksana Senior", "Spesialis Stapler", "Urologi", "Sunat Gemuk", "Manajemen Nyeri", "Ahli Bius"]
    })
    st.table(dokter_list)
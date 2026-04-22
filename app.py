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

# 3. CSS Kustom - Tema Hijau Sage & Putih Outline Hitam
st.markdown("""
    <style>
    .stApp { background-color: #B2AC88; } 
    
    /* Judul Besar: Font Putih dengan Outline Hitam */
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

    /* Box Output: Warna lebih cerah agar teks gelap mudah dibaca */
    .result-box {
        background-color: #F7F9F2; 
        padding: 25px; 
        border-radius: 15px; 
        border: 3px solid #2E473B;
        margin-top: 20px;
    }
    .result-box h3, .result-box p, .result-box b, .result-box li {
        color: #1A2E25 !important;
    }

    /* Sidebar Custom */
    [data-testid="stSidebar"] { background-color: #2E473B; }
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] h2 { color: #E0E5D9 !important; }
    
    /* Form & Input */
    input, select, [data-baseweb="select"] {
        background-color: #FFFFFF !important;
        color: #000000 !important;
    }
    label { color: #FFFFFF !important; font-weight: bold; text-shadow: 1px 1px 1px #000; }
    
    /* Tabel */
    .stTable { background-color: #F7F9F2 !important; border-radius: 10px; }
    </style>
""", unsafe_allow_html=True)

# 4. Data Master
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

# --- HEADER UTAMA (Sesuai Permintaan: Font Putih Outline Hitam) ---
st.markdown("<h1 class='header-style'>RUMAH SUNAT ANAK</h1>", unsafe_allow_html=True)

# --- LOGIKA MENU ---

if menu == "🏠 Beranda":
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
        <div style='text-align: center;'>
            <h2 style='color: #FFFFFF; text-shadow: 1px 1px 2px #000;'>Selamat Datang di Rumah Sunat Anak 🌙</h2>
            <p style='font-size: 18px; color: #1A2E25; font-style: italic; font-weight: bold;'>
                "Kesucian (fitrah) itu ada lima: Khitan, mencukur bulu kemaluan, mencabut bulu ketiak, memotong kuku, dan mencukur kumis." 
                <br><b>(HR. Bukhari & Muslim)</b>
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Gambar Dokter Laki-Laki di Tengah
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.image("https://cdn-icons-png.flaticon.com/512/3774/3774299.png", use_container_width=True)

    st.markdown("""
        <div style='text-align: center; margin-top: 20px;'>
            <p style='font-size: 18px; color: #1A2E25; font-weight: 500;'>
                Pusat khitan modern dengan tenaga medis ahli. Mengutamakan metode yang <b>minim nyeri</b>, 
                <b>tanpa jahit</b>, dan <b>langsung bisa beraktivitas</b>.
            </p>
        </div>
    """, unsafe_allow_html=True)

elif menu == "📊 Cek Kuota":
    st.markdown("<h2 class='subheader-style'>Status Ketersediaan Kuota 📊</h2>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Kuota Khitan Massal (Periode Ini)", f"{st.session_state.terdaftar_massal}/{st.session_state.kuota_massal_total}")
    with col2:
        st.metric("Sisa Kuota Reguler Hari Ini", f"{st.session_state.kuota_reguler} Kursi")
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
                st.balloons()
                hari_indo = {"Monday": "Senin", "Tuesday": "Selasa", "Wednesday": "Rabu", "Thursday": "Kamis", "Friday": "Jumat", "Saturday": "Sabtu", "Sunday": "Minggu"}
                st.markdown(f"""<div class="result-box">
                    <h3>✅ Pendaftaran Berhasil!</h3>
                    <p><b>Nama:</b> {nama}</p>
                    <p><b>Jadwal:</b> {hari_indo.get(tgl_rencana.strftime('%A'))}, {tgl_rencana.strftime('%d %B %Y')}</p>
                    <p><b>Dokter:</b> {data_metode[metode_fix]['dokter']}</p>
                </div>""", unsafe_allow_html=True)

elif menu == "💊 Panduan Perawatan":
    st.markdown("<h2 class='subheader-style'>Post-Op Care Guide 💊</h2>", unsafe_allow_html=True)
    fase = st.selectbox("Pilih Fase Pemulihan:", ["Fase 1: 24 Jam Pertama", "Fase 2: Hari ke 3-5", "Fase 3: Pelepasan Alat/Kontrol"])
    
    # Output menggunakan warna kontras (Result Box Terang) agar mudah dibaca
    if fase == "Fase 1: 24 Jam Pertama":
        st.markdown("""<div class="result-box">
            <h3>🛡️ Instruksi 24 Jam Pertama</h3>
            <ul>
                <li>Berikan obat pereda nyeri (Analgetik) setiap 4-6 jam sesuai resep.</li>
                <li>Pastikan perban atau klem tidak tertarik kencang.</li>
                <li>Gunakan celana sunat yang longgar/berpelindung.</li>
                <li>Kompres area sekitar jika terjadi pembengkakan ringan.</li>
            </ul>
        </div>""", unsafe_allow_html=True)
    elif fase == "Fase 2: Hari ke 3-5":
        st.markdown("""<div class="result-box">
            <h3>🚿 Instruksi Kebersihan</h3>
            <ul>
                <li>Anak diperbolehkan mandi (untuk metode klem bisa langsung kena air).</li>
                <li>Teteskan cairan antiseptik pada area luka secara rutin.</li>
                <li>Jangan mencoba melepas keropeng atau alat sendiri.</li>
            </ul>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown("""<div class="result-box">
            <h3>🏥 Jadwal Kontrol Akhir</h3>
            <p>Silahkan datang kembali ke klinik untuk proses pelepasan alat klem atau pengecekan hasil akhir oleh dokter spesialis.</p>
        </div>""", unsafe_allow_html=True)

elif menu == "🏢 Tentang Kami":
    st.markdown("<h2 class='subheader-style'>Profil & Sejarah Klinik 🏢</h2>", unsafe_allow_html=True)
    
    st.markdown("""<div class="result-box">
        <p><b>Sejarah & Latar Belakang:</b><br>
        Rumah Sunat Anak didirikan pada tahun 2015 berawal dari keprihatinan terhadap trauma psikologis yang sering dialami anak saat proses khitan konvensional. 
        Kami mempelopori penggunaan teknologi medis terkini seperti <i>Power Clamp</i> dan <i>Stapler ZSR</i> di wilayah ini. Dengan visi menjadi pusat khitan modern terbaik, 
        kami telah melayani lebih dari 10.000 pasien dengan tingkat keberhasilan dan kepuasan orang tua yang sangat tinggi. Fokus kami bukan hanya pada tindakan medis, 
        tetapi juga pendekatan edukatif agar anak merasa berani dan nyaman.</p>
    </div>""", unsafe_allow_html=True)

    st.markdown("<h3 style='color:white; text-shadow:1px 1px #000;'>Struktur Organisasi & Tenaga Ahli</h3>", unsafe_allow_html=True)
    
    # Daftar 8 Nama Dokter dengan Spesialisasi Berbeda
    dokter_list = pd.DataFrame({
        "Nama Tenaga Medis": [
            "dr. Ahmad Subarjo", "dr. Zulkifli, Sp.B", "dr. Hilman Syah", "dr. Yusuf Mansur",
            "dr. Ridwan Hakim, Sp.U", "dr. Faisal Anwar", "dr. Siti Aminah", "dr. Budi Santoso"
        ],
        "Spesialisasi / Jabatan": [
            "Kepala Klinik & Ahli Klem", "Spesialis Bedah Umum", "Dokter Pelaksana Senior", "Spesialis Stapler Estetik",
            "Konsultan Urologi", "Spesialis Sunat Gemuk", "Kepala Perawat & Manajemen Nyeri", "Ahli Bius Tanpa Jarum"
        ]
    })
    st.table(dokter_list)
    
    st.markdown("<h3 style='color:white; text-shadow:1px 1px #000;'>Manajemen & Administrasi</h3>", unsafe_allow_html=True)
    st.table(pd.DataFrame({
        "Jabatan": ["Manajer Operasional", "Humas & Kemitraan", "Admin Keuangan", "Layanan Pelanggan"],
        "Nama": ["H. Salim Wijaya", "Rina Kartika", "Anita Sari", "Doni Setiawan"]
    }))
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
# Menggunakan session_state agar data tetap tersimpan selama aplikasi berjalan
if 'kuota_massal_total' not in st.session_state:
    st.session_state.kuota_massal_total = 50
if 'terdaftar_massal' not in st.session_state:
    st.session_state.terdaftar_massal = 5
if 'kuota_reguler' not in st.session_state:
    st.session_state.kuota_reguler = 8

# 3. CSS Kustom - Tema Hijau Sage & Hijau Ketupat
st.markdown("""
    <style>
    .stApp { background-color: #B2AC88; } 
    
    .klinik-title {
        color: #2E473B; text-align: center; font-size: 50px; font-weight: bold;
        text-shadow: 2px 2px #E0E5D9; font-family: 'Verdana', sans-serif;
    }
    
    .result-box {
        background-color: #E0E5D9; 
        padding: 25px; 
        border-radius: 15px; 
        border: 3px solid #2E473B;
        margin-top: 20px;
    }
    .result-box h3, .result-box p, .result-box b {
        color: #2E473B !important;
    }

    [data-testid="stSidebar"] { background-color: #2E473B; }
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] h2 { color: #E0E5D9 !important; }
    
    /* Membuat teks input lebih kontras */
    input, select, [data-baseweb="select"] {
        background-color: #F0F2ED !important;
        color: #2E473B !important;
    }
    label { color: #2E473B !important; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# 4. Data Master Dokter
data_dokter = {
    "Khitan Reguler": {"dokter": "dr. Ahmad Subarjo", "jadwal": "Senin - Jumat"},
    "Khitan Metode Klem": {"dokter": "dr. Hilman Syah", "jadwal": "Setiap Hari"},
    "Khitan Metode Stapler": {"dokter": "dr. Yusuf Mansur", "jadwal": "Sabtu & Minggu"},
    "Khitan Gemuk (Spesialis)": {"dokter": "dr. Zulkifli, Sp.B", "jadwal": "Selasa & Kamis"}
}

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>Menu Utama 🌙</h2>", unsafe_allow_html=True)
    menu = st.radio("Navigasi", ["🏠 Beranda", "📊 Cek Kuota", "📝 Pendaftaran", "📐 Kalkulator Metode", "💊 Panduan Perawatan", "🏢 Tentang Kami"])

# --- HEADER UTAMA ---
st.markdown("<h1 class='klinik-title'>RUMAH SUNAT ANAK</h1>", unsafe_allow_html=True)

# --- LOGIKA MENU ---

if menu == "🏠 Beranda":
    st.markdown("<br>", unsafe_allow_html=True)
    # Header Beranda dengan Slogan Dalil di bawah Judul
    st.markdown("""
        <div style='text-align: center;'>
            <h2 style='color: #2E473B;'>Selamat Datang di Rumah Sunat Anak 🌙</h2>
            <p style='font-size: 20px; color: #2E473B; font-style: italic;'>
                "Kesucian (fitrah) itu ada lima: Khitan, mencukur bulu kemaluan, mencabut bulu ketiak, memotong kuku, dan mencukur kumis." 
                <br><b>(HR. Bukhari & Muslim)</b>
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Gambar Karakter Anak Laki-Laki di Tengah
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("https://cdn-icons-png.flaticon.com/512/4042/4042422.png", use_container_width=True)

    # Teks Deskripsi Rata Tengah
    st.markdown("""
        <div style='text-align: center; margin-top: 20px;'>
            <p style='font-size: 18px; color: #2E473B;'>
                Tempat sunat modern yang mengutamakan <b>kenyamanan psikologis anak</b> dan <b>keamanan medis</b>. 
                Kami hadir dengan teknologi terbaru untuk pengalaman berkhitan yang minim nyeri dan penyembuhan cepat.
            </p>
        </div>
    """, unsafe_allow_html=True)

elif menu == "📊 Cek Kuota":
    st.subheader("Ketersediaan Kuota Real-Time 📊")
    col1, col2 = st.columns(2)
    with col1:
        # Menampilkan kuota massal yang sudah terisi
        st.metric("Kuota Khitan Massal (Juni)", f"{st.session_state.terdaftar_massal}/{st.session_state.kuota_massal_total}", "Update Live")
    with col2:
        # Menampilkan sisa kuota harian
        st.metric("Sisa Kuota Reguler Hari Ini", f"{st.session_state.kuota_reguler} Kursi", "Tersedia")
    
    persen_massal = (st.session_state.terdaftar_massal / st.session_state.kuota_massal_total) * 100
    st.progress(int(persen_massal))
    st.write(f"Tingkat keterisian pendaftaran sunat massal: {int(persen_massal)}%")

elif menu == "📝 Pendaftaran":
    st.subheader("Formulir Pendaftaran Digital 📝")
    
    with st.form("daftar_form"):
        nama = st.text_input("Nama Lengkap Anak")
        jenis_layanan = st.selectbox("Jenis Layanan", ["Khitan Reguler (Harian)", "Khitan Massal (Promo)"])
        metode_fix = st.selectbox("Pilih Paket Metode", list(data_dokter.keys()))
        tgl_rencana = st.date_input("Rencana Tanggal Kedatangan", min_value=datetime.now())
        
        submit = st.form_submit_button("Konfirmasi Pendaftaran ✨")
        
        if submit:
            if not nama:
                st.error("Silakan masukkan nama anak.")
            else:
                pendaftaran_berhasil = False
                
                # Logika Pengurangan Kuota
                if jenis_layanan == "Khitan Reguler (Harian)":
                    if st.session_state.kuota_reguler > 0:
                        st.session_state.kuota_reguler -= 1
                        pendaftaran_berhasil = True
                    else:
                        st.error("Mohon maaf, kuota reguler untuk hari ini sudah penuh.")
                else:
                    if st.session_state.terdaftar_massal < st.session_state.kuota_massal_total:
                        st.session_state.terdaftar_massal += 1
                        pendaftaran_berhasil = True
                    else:
                        st.error("Mohon maaf, kuota promo sunat massal sudah habis.")
                
                if pendaftaran_berhasil:
                    st.balloons()
                    # Konversi Hari ke Bahasa Indonesia
                    hari_eng = tgl_rencana.strftime("%A")
                    hari_indo = {"Monday": "Senin", "Tuesday": "Selasa", "Wednesday": "Rabu", "Thursday": "Kamis", "Friday": "Jumat", "Saturday": "Sabtu", "Sunday": "Minggu"}
                    
                    st.markdown(f"""
                        <div class="result-box">
                            <h3>Konfirmasi Jadwal Berhasil! ✅</h3>
                            <p><b>Nama Pasien:</b> {nama}</p>
                            <p><b>Layanan:</b> {jenis_layanan}</p>
                            <p><b>Hari/Tanggal:</b> {hari_indo.get(hari_eng, hari_eng)}, {tgl_rencana.strftime('%d %B %Y')}</p>
                            <p><b>Dokter:</b> {data_dokter[metode_fix]['dokter']}</p>
                            <hr>
                            <p style='font-size: 14px;'><i>Harap datang tepat waktu sesuai tanggal yang dipilih. Simpan halaman ini sebagai bukti pendaftaran.</i></p>
                        </div>
                    """, unsafe_allow_html=True)

elif menu == "📐 Kalkulator Metode":
    st.subheader("Smart Method Selector 📐")
    usia = st.number_input("Usia Anak (Tahun)", 0, 15, 7)
    aktif = st.select_slider("Tingkat Aktivitas Anak", options=["Sangat Tenang", "Normal", "Sangat Aktif"])
    keinginan = st.selectbox("Prioritas Utama", ["Tanpa Jahitan", "Bisa Langsung Mandi", "Penyembuhan Tercepat"])
    
    if st.button("Rekomendasikan Metode ✨"):
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
            <p><b>Analisis:</b> {desc}</p>
        </div>""", unsafe_allow_html=True)

elif menu == "💊 Panduan Perawatan":
    st.subheader("Post-Op Care Guide 💊")
    fase = st.radio("Pilih Fase:", ["24 Jam Pertama", "Masa Penyembuhan (3-5 Hari)", "Pelepasan Alat/Kontrol"])
    
    if fase == "24 Jam Pertama":
        st.info("Fokus pada istirahat. Minum obat pereda nyeri sesuai instruksi dokter.")
    elif fase == "Masa Penyembuhan (3-5 Hari)":
        st.warning("Jaga kebersihan area sunat. Gunakan celana sunat agar sirkulasi udara baik.")
    else:
        st.success("Waktunya kontrol ke klinik untuk memastikan luka mengering dengan sempurna.")

elif menu == "🏢 Tentang Kami":
    st.subheader("Profil Rumah Sunat")
    st.write("Profesional, Berpengalaman, dan Ramah Anak.")
    df_tim = pd.DataFrame({
        "Posisi": ["Kepala Klinik", "Spesialis Bedah", "Admin Medis"],
        "Nama": ["dr. Ahmad Subarjo", "dr. Zulkifli, Sp.B", "Siti Aminah"]
    })
    st.table(df_tim)
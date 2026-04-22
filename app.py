import streamlit as st
import pandas as pd
from datetime import datetime
import time

# =================================================================
# 1. KONFIGURASI HALAMAN
# =================================================================
st.set_page_config(
    page_title="Rumah Sunat Anak | Modern & Nyaman", 
    page_icon="🌙", 
    layout="wide"
)

# Inisialisasi Session State
if 'kuota_reguler' not in st.session_state:
    st.session_state.kuota_reguler = 12
if 'rekomendasi_paket' not in st.session_state:
    st.session_state.rekomendasi_paket = "Sunat Laser (Flashcutter)"

# =================================================================
# 2. CSS KUSTOM
# =================================================================
st.markdown("""
    <style>
    .stApp { background-color: #B2AC88; } 
    
    .header-container {
        text-align: center;
        padding: 30px 10px;
        background-color: rgba(46, 71, 59, 0.15);
        border-radius: 25px;
        margin-bottom: 20px;
    }
    .header-style {
        color: white; font-size: clamp(35px, 8vw, 65px); font-weight: bold;
        text-shadow: -3px -3px 0 #000, 3px -3px 0 #000, -3px 3px 0 #000, 3px 3px 0 #000;
        font-family: 'Verdana', sans-serif;
    }
    .slogan-style {
        color: #1A2E25; font-size: 19px; font-weight: 600;
        font-style: italic; margin-top: 15px; display: block; line-height: 1.5;
    }

    .center-content {
        text-align: center;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }

    .result-box {
        background-color: #F7F9F2; padding: 35px; border-radius: 20px; 
        border: 4px solid #2E473B; margin-top: 15px;
        box-shadow: 8px 8px 0px #2E473B;
        text-align: left;
    }
    .result-box h3 { color: #2E473B !important; font-weight: 800; margin-bottom: 15px; }
    .result-box p, .result-box b, .result-box li, .result-box span {
        color: #000000 !important; font-size: 18px; line-height: 1.6;
    }

    .custom-info {
        background-color: #2E473B; color: #F7F9F2;
        padding: 15px; border-radius: 10px; border-left: 10px solid #F7F9F2;
        font-weight: bold; margin-bottom: 20px; font-size: 16px;
    }

    .subheader-style {
        color: white; font-size: 32px; font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        border-bottom: 5px solid #2E473B; padding-bottom: 5px;
    }

    [data-testid="stSidebar"] { background-color: #2E473B; }
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
data_dokter = [
    {"Nama": "dr. Ahmad Subarjo", "Spesialisasi": "Kepala Klinik & Ahli Klem"},
    {"Nama": "dr. Zulkifli, Sp.B", "Spesialisasi": "Spesialis Bedah & Sunat Gunting"},
    {"Nama": "dr. Hilman Syah", "Spesialisasi": "Dokter Pelaksana Laser Cauter"},
    {"Nama": "dr. Yusuf Mansur", "Spesialisasi": "Spesialis Stapler Estetik"},
    {"Nama": "dr. Faisal Anwar", "Spesialisasi": "Spesialis Sunat Gemuk"}
]

struktur_manajemen = {
    "Pimpinan Tinggi": [{"Jabatan": "Direktur Utama", "Nama": "H. Salim Wijaya, M.M"}],
    "Operasional Medis": [
        {"Jabatan": "Kepala Medis", "Nama": "dr. Ahmad Subarjo"},
        {"Jabatan": "Kepala Perawat", "Nama": "Ns. Siti Aminah, S.Kep"}
    ],
    "Administrasi": [{"Jabatan": "Admin & Keuangan", "Nama": "Anita Sari, A.Md"}]
}

# =================================================================
# 4. SIDEBAR NAVIGATION
# =================================================================
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: white;'>MENU UTAMA 🌙</h2>", unsafe_allow_html=True)
    menu = st.radio("Pilih Halaman:", [
        "🏠 Beranda Utama", 
        "📐 Kalkulator Paket Sunat", 
        "📝 Pendaftaran Digital", 
        "📊 Monitoring Kuota", 
        "💊 Panduan Pasca-Khitan",
        "🏢 Profil Lengkap RS"
    ])

# =================================================================
# 5. HEADER LOGIC
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
# 6. MENU IMPLEMENTATION
# =================================================================

# --- BERANDA (FOTO DIEDIT KE TENGAH) ---
if menu == "🏠 Beranda Utama":
    st.markdown('<div class="center-content">', unsafe_allow_html=True)
    st.markdown("<h2 class='subheader-style'>Selamat Datang di Pusat Khitan Modern</h2>", unsafe_allow_html=True)
    
    # PERUBAHAN DISINI: Menggunakan sistem kolom untuk menengahkan foto dokter
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.image("https://cdn-icons-png.flaticon.com/512/3774/3774299.png", use_container_width=True)
    
    st.markdown("""
        <div class="result-box" style="text-align: center;">
            <h3>Layanan Khitan Professional & Ramah Anak</h3>
            <p>Kami menggabungkan keahlian medis spesialis dengan teknologi modern untuk memberikan hasil khitan yang estetik, cepat sembuh, dan minim rasa sakit.</p>
            <p><b>Visi Kami:</b> Mewujudkan generasi sehat yang menjalankan syariat dengan nyaman.</p>
        </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- KALKULATOR PAKET ---
elif menu == "📐 Kalkulator Paket Sunat":
    st.markdown("<h2 class='subheader-style'>Penentuan Paket Sunat 📐</h2>", unsafe_allow_html=True)
    usia = st.number_input("Input Usia Pasien (Tahun)", 0, 18, 7)
    kondisi = st.selectbox("Kondisi Fisik", ["Normal", "Fimosis (Perlekatan)", "Gemuk (Micro Penis)"])
    aktif = st.select_slider("Tingkat Aktivitas Anak", options=["Tenang", "Normal", "Sangat Aktif"])
    
    if st.button("Analisis Rekomendasi Paket ✨"):
        with st.spinner("Menganalisis..."):
            time.sleep(1)
            if kondisi == "Gemuk (Micro Penis)":
                st.session_state.rekomendasi_paket = "Sunat Gunting (Konvensional/Bedah)"
                txt = "Dibutuhkan ketelitian manual tinggi untuk pasien gemuk agar hasil tidak tenggelam."
            elif aktif == "Sangat Aktif":
                st.session_state.rekomendasi_paket = "Sunat Metode Klem"
                txt = "Alat klem berfungsi sebagai pelindung luka, sangat aman bagi anak yang aktif bergerak."
            elif usia > 11:
                st.session_state.rekomendasi_paket = "Sunat Metode Stapler"
                txt = "Metode paling premium dan modern dengan hasil sangat rapi, cocok untuk usia remaja."
            else:
                st.session_state.rekomendasi_paket = "Sunat Laser (Flashcutter)"
                txt = "Metode laser cauter yang efisien, proses cepat, dan luka cepat kering."

            st.markdown(f"""
                <div class="result-box">
                    <h3>Hasil Rekomendasi: {st.session_state.rekomendasi_paket}</h3>
                    <p><b>Alasan Medis:</b> {txt}</p>
                </div>
            """, unsafe_allow_html=True)

# --- PENDAFTARAN DIGITAL ---
elif menu == "📝 Pendaftaran Digital":
    st.markdown("<h2 class='subheader-style'>Formulir Pendaftaran Pasien 📝</h2>", unsafe_allow_html=True)
    list_metode = ["Sunat Laser (Flashcutter)", "Sunat Gunting (Konvensional/Bedah)", "Sunat Metode Klem", "Sunat Metode Stapler"]
    
    try: idx_pilih = list_metode.index(st.session_state.rekomendasi_paket)
    except: idx_pilih = 0

    with st.form("form_pendaftaran"):
        n_pasien = st.text_input("Nama Lengkap Pasien")
        n_ortu = st.text_input("Nama Orang Tua")
        paket_fix = st.selectbox("Pilih Paket Tindakan:", list_metode, index=idx_pilih)
        tgl_tindakan = st.date_input("Pilih Tanggal")
        
        if st.form_submit_button("KONFIRMASI PENDAFTARAN ✨"):
            if n_pasien:
                st.balloons()
                st.session_state.kuota_reguler -= 1
                st.markdown(f"""
                    <div class="result-box">
                        <h3>✅ Pendaftaran Berhasil!</h3>
                        <p>Ananda <b>{n_pasien}</b> telah terdata untuk paket <b>{paket_fix}</b>.</p>
                        <p>Silahkan datang pada tanggal {tgl_tindakan} jam 08:00 WIB.</p>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.error("Nama pasien tidak boleh kosong!")

# --- MONITORING KUOTA ---
elif menu == "📊 Monitoring Kuota":
    st.markdown("<h2 class='subheader-style'>Status Slot Harian 📊</h2>", unsafe_allow_html=True)
    st.metric("Sisa Kuota Reguler", f"{st.session_state.kuota_reguler} Pasien", "Tersedia")
    st.progress(st.session_state.kuota_reguler * 8)
    
    st.markdown(f"""
        <div class="custom-info">
            PEMBERITAHUAN: Saat ini sisa kuota adalah {st.session_state.kuota_reguler} slot. 
            Segera lakukan pendaftaran digital untuk mengunci jadwal tindakan Anda.
        </div>
    """, unsafe_allow_html=True)

# --- PANDUAN PASCA KHITAN ---
elif menu == "💊 Panduan Pasca-Khitan":
    st.markdown("<h2 class='subheader-style'>Panduan Pemulihan 💊</h2>", unsafe_allow_html=True)
    
    opsi_panduan = st.selectbox("Pilih Fase Pemulihan:", 
                                ["-- Pilih Fase --", "Fase 24 Jam Pertama", "Fase Hari 2 - 5", "Fase Kontrol Akhir"],
                                key="panduan_selector")
    
    if opsi_panduan == "Fase 24 Jam Pertama":
        st.markdown("""
            <div class="result-box">
                <h3>Saran 24 Jam Pertama (Kritis)</h3>
                <p>1. <b>Istirahat:</b> Biarkan anak beristirahat total, minimalisir gerakan mendadak.</p>
                <p>2. <b>Obat:</b> Minum obat pereda nyeri (Analgesik) tepat waktu setiap 6 jam meskipun tidak sakit.</p>
                <p>3. <b>Observasi:</b> Pastikan tidak ada perdarahan aktif (darah yang menetes terus menerus).</p>
                <p>4. <b>Posisi:</b> Gunakan celana khitan atau biarkan area terbuka (tanpa celana dalam) untuk sirkulasi udara.</p>
            </div>
        """, unsafe_allow_html=True)
    elif opsi_panduan == "Fase Hari 2 - 5":
        st.markdown("""
            <div class="result-box">
                <h3>Saran Pemulihan Lanjutan</h3>
                <p>1. <b>Kebersihan:</b> Bersihkan area sekitar luka dengan kassa steril dan cairan infus (NaCl).</p>
                <p>2. <b>Aktivitas:</b> Anak sudah boleh berjalan santai namun belum boleh berlari atau bersepeda.</p>
                <p>3. <b>Nutrisi:</b> Perbanyak asupan protein (telur, ikan, daging) untuk mempercepat pertumbuhan jaringan.</p>
                <p>4. <b>Mandi:</b> Gunakan teknik lap badan atau mandi sesuai instruksi khusus metode (Klem boleh mandi).</p>
            </div>
        """, unsafe_allow_html=True)
    elif opsi_panduan == "Fase Kontrol Akhir":
        st.markdown("""
            <div class="result-box">
                <h3>Saran Kontrol & Lepas Alat</h3>
                <p>1. <b>Jadwal:</b> Segera datang ke klinik sesuai tanggal kontrol yang diberikan dokter.</p>
                <p>2. <b>Pelepasan:</b> Untuk metode klem/stapler, alat akan dilepas oleh tenaga medis profesional.</p>
                <p>3. <b>Pasca Lepas:</b> Area mungkin akan terlihat kemerahan atau kuning (fibrin), hal ini normal dan jangan ditarik paksa.</p>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.write("Silahkan pilih fase di atas untuk melihat detail panduan.")

# --- PROFIL LENGKAP RS ---
elif menu == "🏢 Profil Lengkap RS":
    st.markdown("<h2 class='subheader-style'>Mengenal Rumah Sunat Anak 🏢</h2>", unsafe_allow_html=True)
    
    st.markdown("""
        <div class="result-box">
            <h3>Sejarah & Komitmen</h3>
            <p>Berdiri sejak tahun 2018, kami berkomitmen menjadi garda terdepan dalam pelayanan sirkumsisi modern. Dengan mengutamakan sterilitas dan pendekatan psikologis 'Ramah Anak', kami telah melayani ribuan pasien dengan tingkat kepuasan tinggi.</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<h3 style='color:white; margin-top:30px;'>🏛️ Struktur Manajemen & Organisasi</h3>", unsafe_allow_html=True)
    for kategori, data in struktur_manajemen.items():
        with st.expander(f"Lihat Divisi: {kategori}"):
            st.table(pd.DataFrame(data))

    st.markdown("<h3 style='color:white; margin-top:30px;'>👨‍⚕️ Tim Dokter Spesialis Kami</h3>", unsafe_allow_html=True)
    st.table(pd.DataFrame(data_dokter))
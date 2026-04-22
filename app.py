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

# Inisialisasi Session State
if 'kuota_massal' not in st.session_state:
    st.session_state.kuota_massal = 15
if 'rekomendasi_metode' not in st.session_state:
    st.session_state.rekomendasi_metode = "Khitan Reguler"

# =================================================================
# 2. CSS KUSTOM (STRICT CONTRAST & NO OVERLAP)
# =================================================================
st.markdown("""
    <style>
    /* Background Utama Sage */
    .stApp { background-color: #B2AC88; } 
    
    /* Judul Utama dengan Outline agar tidak terpotong */
    .header-container {
        text-align: center;
        padding: 40px 20px;
        background-color: rgba(46, 71, 59, 0.1);
        border-radius: 20px;
        margin-bottom: 20px;
    }
    .header-style {
        color: white; font-size: clamp(40px, 8vw, 70px); font-weight: bold;
        text-shadow: -3px -3px 0 #000, 3px -3px 0 #000, -3px 3px 0 #000, 3px 3px 0 #000;
        font-family: 'Verdana', sans-serif;
        line-height: 1.2;
    }
    .slogan-style {
        color: #1A2E25; font-size: 20px; font-weight: 600;
        font-style: italic; margin-top: 15px; line-height: 1.6;
        display: block; /* Memastikan tidak terpotong */
    }

    /* Subheader dengan Bar Hijau */
    .subheader-style {
        color: white; font-size: 32px; font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        border-bottom: 5px solid #2E473B;
        padding-bottom: 10px; margin-bottom: 25px;
    }

    /* BOX CARD (Teks Hitam Pekat - Anti Tabrakan Warna) */
    .result-box {
        background-color: #F7F9F2; padding: 30px; border-radius: 20px; 
        border: 4px solid #2E473B; margin-top: 20px;
        box-shadow: 8px 8px 0px #2E473B;
    }
    .result-box h3 { color: #2E473B !important; font-weight: 800; margin-bottom: 15px; }
    .result-box p, .result-box b, .result-box li, .result-box span {
        color: #000000 !important; font-size: 18px; line-height: 1.6;
    }

    /* Tabel Styling */
    .stTable { background-color: #F7F9F2 !important; border-radius: 15px; overflow: hidden; }
    .stTable td, .stTable th { color: #000000 !important; font-size: 16px !important; }

    /* Sidebar Navigation */
    [data-testid="stSidebar"] { background-color: #2E473B; border-right: 5px solid #8C9476; }
    [data-testid="stSidebar"] .stRadio label { color: #E0E5D9 !important; font-size: 18px !important; }
    [data-testid="stSidebar"] h2 { color: #B2AC88 !important; border-bottom: 2px solid #B2AC88; }
    
    /* Tombol & Input */
    .stButton>button {
        background-color: #2E473B !important; color: white !important;
        border-radius: 12px; font-weight: bold; height: 55px; width: 100%;
        border: 2px solid white; transition: 0.3s;
    }
    .stButton>button:hover { transform: scale(1.02); background-color: #3d5e4e !important; }
    label { color: white !important; font-size: 18px !important; text-shadow: 1px 1px 2px #000; }
    </style>
""", unsafe_allow_html=True)

# =================================================================
# 3. DATA MASTER (STURKTUR & DOKTER)
# =================================================================
data_dokter_db = [
    {"Nama": "dr. Ahmad Subarjo", "Spesialisasi": "Kepala Klinik & Ahli Klem", "Jam": "08:00 - 14:00"},
    {"Nama": "dr. Zulkifli, Sp.B", "Spesialisasi": "Spesialis Bedah Umum", "Jam": "15:00 - 19:00"},
    {"Nama": "dr. Hilman Syah", "Spesialisasi": "Dokter Pelaksana Senior", "Jam": "10:00 - 16:00"},
    {"Nama": "dr. Yusuf Mansur", "Spesialisasi": "Spesialis Stapler Estetik", "Jam": "13:00 - 20:00"},
    {"Nama": "dr. Faisal Anwar", "Spesialisasi": "Spesialis Sunat Gemuk", "Jam": "Sesuai Perjanjian"}
]

struktur_organisasi = {
    "Pimpinan Tinggi": [
        {"Jabatan": "Direktur Utama", "Nama": "H. Salim Wijaya, M.M"},
        {"Jabatan": "Komite Medik", "Nama": "dr. Ahmad Subarjo"}
    ],
    "Divisi Operasional": [
        {"Jabatan": "Manajer Klinik", "Nama": "Rina Kartika, S.E"},
        {"Jabatan": "Kepala Perawat", "Nama": "Ns. Siti Aminah, S.Kep"},
        {"Jabatan": "Admin & Keuangan", "Nama": "Anita Sari, A.Md"}
    ],
    "Divisi Pelayanan": [
        {"Jabatan": "IT & Digital Marketing", "Nama": "Eko Prasetyo, S.Kom"},
        {"Jabatan": "Customer Service", "Nama": "Budi Santoso"},
        {"Jabatan": "Logistik & Sterilisasi", "Nama": "Doni Setiawan"}
    ]
}

# =================================================================
# 4. SIDEBAR MENU
# =================================================================
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>LAYANAN UTAMA 🌙</h2>", unsafe_allow_html=True)
    menu = st.radio("Pilih Navigasi:", [
        "🏠 Beranda Utama", 
        "📐 Kalkulator Metode", 
        "📝 Pendaftaran Digital", 
        "📊 Monitoring Kuota", 
        "💊 Panduan Pasca-Khitan",
        "🏢 Profil Lengkap RS"
    ])
    st.divider()
    st.info("IGD Khitan 24 Jam: 0812-XXXX-XXXX")

# =================================================================
# 5. HEADER (SLOGAN TIDAK TERPOTONG)
# =================================================================
st.markdown(f"""
    <div class="header-container">
        <h1 class="header-style">RUMAH SUNAT ANAK</h1>
        <span class="slogan-style">
            "Kesucian (fitrah) itu ada lima: Khitan, mencukur bulu kemaluan, mencabut bulu ketiak, memotong kuku, dan mencukur kumis."<br>
            <b>(HR. Bukhari & Muslim)</b>
        </span>
    </div>
""", unsafe_allow_html=True)

# =================================================================
# 6. LOGIKA MENU (LAYOUT VERTIKAL & TEKS JELAS)
# =================================================================

# --- BERANDA ---
if menu == "🏠 Beranda Utama":
    st.markdown("<h2 class='subheader-style'>Selamat Datang di Pusat Khitan Modern</h2>", unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/3774/3774299.png", width=300)
    st.markdown("""
        <div class="result-box">
            <h3>Solusi Khitan Tanpa Trauma</h3>
            <p>Kami menghadirkan pengalaman khitan yang berbeda. Menggunakan pendekatan psikologis 'Hypnosirkumsisi' dan teknologi medis terbaru, kami memastikan anak Anda tetap tenang dan nyaman selama proses tindakan.</p>
            <ul>
                <li><b>Metode Modern:</b> Tanpa jahitan, tanpa perban, bisa langsung mandi.</li>
                <li><b>Fasilitas:</b> Ruang tindakan bertema (VR Cinema & PlayStation).</li>
                <li><b>Tim Ahli:</b> Ditangani oleh dokter spesialis dan perawat berpengalaman.</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

# --- KALKULATOR (LAYOUT VERTIKAL) ---
elif menu == "📐 Kalkulator Metode":
    st.markdown("<h2 class='subheader-style'>Smart Method Selector 📐</h2>", unsafe_allow_html=True)
    # Ubah Kolom Jadi Vertikal
    usia = st.number_input("Berapa usia anak saat ini?", 0, 18, 7)
    kondisi = st.selectbox("Kondisi Fisik Khusus?", ["Normal", "Kelebihan Berat Badan (Gemuk)", "Phimosis/Perlengketan"])
    aktif = st.select_slider("Tingkat Aktivitas Anak", options=["Tenang", "Normal", "Sangat Aktif"])
    prioritas = st.selectbox("Apa prioritas utama Anda?", ["Hasil Estetik Maksimal", "Bisa Mandi & Sekolah Langsung", "Ekonomis & Aman"])

    if st.button("Analisis Rekomendasi Medis ✨"):
        with st.spinner("Menghitung akurasi metode..."):
            time.sleep(1)
            if kondisi == "Kelebihan Berat Badan (Gemuk)":
                st.session_state.rekomendasi_metode = "Khitan Gemuk (Spesialis Bedah)"
                h_txt = "Memerlukan teknik penyayatan khusus agar hasil tidak tenggelam kembali."
            elif aktif == "Sangat Aktif" or prioritas == "Bisa Mandi & Sekolah Langsung":
                st.session_state.rekomendasi_metode = "Khitan Metode Klem (Power Clamp)"
                h_txt = "Alat pelindung klem memungkinkan anak tetap bebas bergerak dan terkena air."
            elif prioritas == "Hasil Estetik Maksimal":
                st.session_state.rekomendasi_metode = "Khitan Metode Stapler"
                h_txt = "Teknologi sirkular otomatis yang memberikan hasil paling rapi tanpa jahitan manual."
            else:
                st.session_state.rekomendasi_metode = "Khitan Reguler (Laser Cauter)"
                h_txt = "Metode standar yang efektif dengan pemulihan jaringan yang stabil."

            st.markdown(f"""
                <div class="result-box">
                    <h3>Rekomendasi: {st.session_state.rekomendasi_metode}</h3>
                    <p><b>Analisis:</b> {h_txt}</p>
                    <p><i>Silahkan lanjutkan ke menu Pendaftaran untuk memesan jadwal.</i></p>
                </div>
            """, unsafe_allow_html=True)

# --- PANDUAN PASCA-KHITAN (ANTI-TABRAKAN WARNA) ---
elif menu == "💊 Panduan Pasca-Khitan":
    st.markdown("<h2 class='subheader-style'>Post-Op Care Guide 💊</h2>", unsafe_allow_html=True)
    fase = st.radio("Pilih Fase Pemulihan:", [
        "24 Jam Pertama (Fase Kritis)", 
        "Hari 2 - 5 (Fase Penyembuhan)", 
        "Hari 7+ (Fase Pelepasan Alat/Kontrol)"
    ])
    
    # Pastikan Teks Hitam di Atas Background Gading
    if "24 Jam" in fase:
        st.markdown("""
            <div class="result-box">
                <h3>Instruksi 24 Jam Pertama</h3>
                <p>1. <b>Istirahat Total:</b> Hindari anak melompat atau berlari berlebihan.</p>
                <p>2. <b>Obat:</b> Minum obat pereda nyeri (Analgesik) tepat waktu setiap 6 jam.</p>
                <p>3. <b>Observasi:</b> Pastikan tidak ada rembesan darah aktif pada alat atau perban.</p>
                <p>4. <b>Kebersihan:</b> Gunakan celana khitan yang memiliki pelindung (tempurung).</p>
            </div>
        """, unsafe_allow_html=True)
    elif "Hari 2 - 5" in fase:
        st.markdown("""
            <div class="result-box">
                <h3>Instruksi Perawatan Rutin</h3>
                <p>1. <b>Tetes Antiseptik:</b> Berikan cairan antiseptik pada area luka 3 kali sehari.</p>
                <p>2. <b>Mandi:</b> Jika menggunakan Klem, anak boleh mandi namun pastikan sela klem dibilas bersih.</p>
                <p>3. <b>Nutrisi:</b> Perbanyak protein (telur, ikan, daging) untuk mempercepat pertumbuhan jaringan baru.</p>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div class="result-box">
                <h3>Instruksi Akhir & Kontrol</h3>
                <p>1. <b>Pelepasan:</b> Datang tepat waktu sesuai jadwal untuk pelepasan alat klem.</p>
                <p>2. <b>Perawatan Lanjutan:</b> Setelah alat lepas, area luka biasanya akan tampak kuning (fibrin), jangan dikelupas paksa.</p>
                <p>3. <b>Sembuh Total:</b> Biasanya terjadi pada hari ke-14 hingga ke-21.</p>
            </div>
        """, unsafe_allow_html=True)

# --- PROFIL & STRUKTUR (LAYOUT RAPI & LENGKAP) ---
elif menu == "🏢 Profil Lengkap RS":
    st.markdown("<h2 class='subheader-style'>Mengenal Rumah Sunat Anak 🏢</h2>", unsafe_allow_html=True)
    
    # Sejarah Panjang
    st.markdown("""
        <div class="result-box">
            <h3>Sejarah & Visi</h3>
            <p>Didirikan pada tahun 2020, <b>Rumah Sunat Anak</b> lahir dari kegelisahan akan banyaknya anak yang mengalami trauma fisik dan mental akibat metode khitan konvensional yang menyakitkan. Kami memulai perjalanan dari sebuah klinik kecil di Jakarta dan kini telah berkembang menjadi pusat rujukan khitan modern dengan standar medis internasional.</p>
            <p>Visi kami adalah menjadi <b>"Pusat Khitan Terbesar dan Teramah Anak di Indonesia"</b> pada tahun 2030, dengan mengedepankan keamanan medis dan kenyamanan psikologis.</p>
        </div>
    """, unsafe_allow_html=True)

    # Visi & Keunggulan Vertikal
    st.markdown("<h3 style='color:white; margin-top:30px;'>Keunggulan Layanan Kami</h3>", unsafe_allow_html=True)
    st.markdown("""
        <div class="result-box">
            <ul>
                <li><b>Tanpa Jarum Suntik:</b> Menggunakan teknologi <i>Needle-Free Injection</i> untuk bius awal.</li>
                <li><b>Sterilitas Terjamin:</b> Semua alat pendukung menggunakan material <i>single-use</i> (sekali pakai).</li>
                <li><b>Tanpa Perban:</b> Metode Klem dan Stapler memungkinkan luka tetap terbuka namun terlindungi.</li>
                <li><b>Konsultasi 24 Jam:</b> Dokter siap menjawab pertanyaan darurat via WhatsApp kapanpun.</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

    # Struktur Organisasi (Dibawah Visi Misi)
    st.markdown("<h3 style='color:white; margin-top:40px;'>🏛️ Struktur Manajemen & Organisasi</h3>", unsafe_allow_html=True)
    for kategori, staf in struktur_organisasi.items():
        with st.expander(f"Lihat Detail: {kategori}"):
            st.table(pd.DataFrame(staf))

    # List Dokter
    st.markdown("<h3 style='color:white; margin-top:30px;'>👨‍⚕️ Tim Dokter Spesialis</h3>", unsafe_allow_html=True)
    st.table(pd.DataFrame(data_dokter_db))

# --- MONITORING KUOTA ---
elif menu == "📊 Monitoring Kuota":
    st.markdown("<h2 class='subheader-style'>Cek Ketersediaan Slot 📊</h2>", unsafe_allow_html=True)
    val_massal = st.session_state.kuota_massal
    st.metric("Kuota Khitan Massal (Periode Libur)", f"{val_massal}/50 Kursi", "-2 Hari Lagi")
    st.progress(val_massal * 2)
    st.write(f"Sisa {50 - val_massal} kuota tersedia untuk pendaftaran hari ini.")

# --- PENDAFTARAN ---
elif menu == "📝 Pendaftaran Digital":
    st.markdown("<h2 class='subheader-style'>Formulir Pendaftaran 📝</h2>", unsafe_allow_html=True)
    with st.form("form_regis"):
        n_anak = st.text_input("Nama Lengkap Anak")
        n_ortu = st.text_input("Nama Orang Tua / Wali")
        wa_ortu = st.text_input("Nomor WhatsApp (Aktif)")
        
        # Sinkron dengan kalkulator
        p_khitan = st.selectbox("Pilih Paket Sunat:", 
                                ["Khitan Reguler", "Khitan Metode Klem", "Khitan Metode Stapler", "Khitan Gemuk (Spesialis)"],
                                index=["Khitan Reguler", "Khitan Metode Klem", "Khitan Metode Stapler", "Khitan Gemuk (Spesialis)"].index(st.session_state.rekomendasi_metode) if st.session_state.rekomendasi_metode in ["Khitan Reguler", "Khitan Metode Klem", "Khitan Metode Stapler", "Khitan Gemuk (Spesialis)"] else 0)
        
        tgl_rencana = st.date_input("Rencana Tanggal Tindakan")
        
        if st.form_submit_button("KONFIRMASI PENDAFTARAN ✨"):
            if n_anak and wa_ortu:
                st.balloons() # Efek Balloons
                st.session_state.kuota_massal += 1
                st.markdown(f"""
                    <div class="result-box">
                        <h3>✅ Pendaftaran Sukses!</h3>
                        <p>Ananda <b>{n_anak}</b> telah terdaftar untuk paket <b>{p_khitan}</b>.</p>
                        <p>Admin kami akan menghubungi nomor {wa_ortu} untuk verifikasi akhir.</p>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.error("Mohon isi Nama Anak dan Nomor WhatsApp!")
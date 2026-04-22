import streamlit as st
import pandas as pd
from datetime import datetime

# ==========================================
# 1. KONFIGURASI HALAMAN & THEME
# ==========================================
st.set_page_config(
    page_title="Rumah Sunat Anak | Modern & Nyaman", 
    page_icon="🌙", 
    layout="wide"
)

# ==========================================
# 2. INISIALISASI SESSION STATE
# ==========================================
# Menyimpan data agar tidak hilang saat pindah menu
if 'kuota_massal_total' not in st.session_state:
    st.session_state.kuota_massal_total = 50
if 'terdaftar_massal' not in st.session_state:
    st.session_state.terdaftar_massal = 12
if 'kuota_reguler' not in st.session_state:
    st.session_state.kuota_reguler = 8
if 'rekomendasi_metode' not in st.session_state:
    st.session_state.rekomendasi_metode = "Khitan Reguler"

# ==========================================
# 3. CSS KUSTOM (STYLING)
# ==========================================
st.markdown("""
    <style>
    /* Background Utama Hijau Sage */
    .stApp { background-color: #B2AC88; } 
    
    /* Judul Besar: Putih dengan Outline Hitam */
    .header-style {
        color: white; 
        text-align: center; 
        font-size: 55px; 
        font-weight: bold;
        text-shadow: -2px -2px 0 #000, 2px -2px 0 #000, -2px 2px 0 #000, 2px 2px 0 #000;
        font-family: 'Verdana', sans-serif;
        margin-bottom: 5px;
    }
    
    .subheader-style {
        color: white;
        font-size: 32px;
        font-weight: bold;
        text-shadow: -1px -1px 0 #000, 1px -1px 0 #000, -1px 1px 0 #000, 1px 1px 0 #000;
        margin-bottom: 20px;
    }

    /* Box Output: Putih Gading agar Teks Hitam Jelas */
    .result-box {
        background-color: #F7F9F2; 
        padding: 30px; 
        border-radius: 20px; 
        border: 4px solid #2E473B;
        margin-top: 20px;
        box-shadow: 5px 5px 15px rgba(0,0,0,0.2);
    }
    
    /* Memaksa Teks Hitam di Dalam Box & Tabel */
    .result-box h3, .result-box p, .result-box b, .result-box li, .stTable td, .stTable th {
        color: #000000 !important;
    }

    /* Sidebar Custom */
    [data-testid="stSidebar"] { background-color: #2E473B; border-right: 2px solid #E0E5D9; }
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] h2 { color: #E0E5D9 !important; }
    
    /* Input Form */
    input, select, [data-baseweb="select"] {
        background-color: #FFFFFF !important;
        color: #000000 !important;
    }
    label { color: white !important; font-weight: bold; text-shadow: 1px 1px 1px #000; }
    
    /* Styling Tabel */
    .stTable { background-color: #F7F9F2 !important; border-radius: 15px; overflow: hidden; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 4. DATA MASTER (DOKTER & LAYANAN)
# ==========================================
data_dokter_lengkap = {
    "Khitan Reguler": {"dokter": "dr. Ahmad Subarjo", "spesialis": "Khitan Anak & Dewasa"},
    "Khitan Metode Klem": {"dokter": "dr. Hilman Syah", "spesialis": "Ahli Power Clamp"},
    "Khitan Metode Stapler": {"dokter": "dr. Yusuf Mansur", "spesialis": "Estetika Stapler ZSR"},
    "Khitan Gemuk (Spesialis)": {"dokter": "dr. Zulkifli, Sp.B", "spesialis": "Bedah Umum & Pediatrik"},
    "Khitan Laser": {"dokter": "dr. Faisal Anwar", "spesialis": "Cauter Expert"},
    "Khitan Urologi": {"dokter": "dr. Ridwan Hakim, Sp.U", "spesialis": "Spesialis Urologi"},
    "Khitan Bayi": {"dokter": "dr. Siti Aminah", "spesialis": "Manajemen Trauma Bayi"},
    "Khitan Tanpa Jarum Suntik": {"dokter": "dr. Budi Santoso", "spesialis": "Ahli Bius Needle-Free"}
}

# ==========================================
# 5. SIDEBAR NAVIGASI
# ==========================================
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>MENU KLINIK 🌙</h2>", unsafe_allow_html=True)
    menu = st.radio("Pilih Menu:", [
        "🏠 Beranda", 
        "📊 Cek Kuota Real-Time", 
        "📐 Kalkulator Metode Smart", 
        "📝 Pendaftaran Digital", 
        "💊 Panduan Pasca-Khitan", 
        "🏢 Profil Rumah Sunat"
    ])
    st.divider()
    st.info("Buka 24 Jam untuk Konsultasi Darurat Pasca-Khitan.")

# HEADER UTAMA (Selalu Muncul)
st.markdown("<h1 class='header-style'>RUMAH SUNAT ANAK</h1>", unsafe_allow_html=True)

# ==========================================
# 6. LOGIKA SETIAP FITUR
# ==========================================

# --- MENU: BERANDA ---
if menu == "🏠 Beranda":
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
        <div style='text-align: center;'>
            <h2 style='color: white; text-shadow: 1px 1px 2px #000;'>Solusi Khitan Modern, Aman & Nyaman</h2>
            <p style='font-size: 20px; color: #1A2E25; font-style: italic; font-weight: bold;'>
                "Kesucian (fitrah) itu ada lima: Khitan, mencukur bulu kemaluan, mencabut bulu ketiak, memotong kuku, dan mencukur kumis." 
                <br><b>(HR. Bukhari & Muslim)</b>
            </p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        # Foto Dokter Laki-laki
        st.image("https://cdn-icons-png.flaticon.com/512/3774/3774299.png", use_container_width=True)

    st.markdown("""
        <div style='text-align: center; margin-top: 20px; background: rgba(255,255,255,0.2); padding: 20px; border-radius: 15px;'>
            <p style='font-size: 18px; color: #1A2E25; font-weight: 500;'>
                Selamat datang di pusat pelayanan khitan terbaik. Kami menggabungkan pendekatan <b>psikologis anak</b> 
                dengan <b>teknologi medis terbaru</b> untuk memberikan pengalaman berharga sekali seumur hidup yang tanpa trauma.
            </p>
        </div>
    """, unsafe_allow_html=True)

# --- MENU: CEK KUOTA ---
elif menu == "📊 Cek Kuota Real-Time":
    st.markdown("<h2 class='subheader-style'>Status Ketersediaan Kuota 📊</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Kuota Khitan Massal (Libur Sekolah)", f"{st.session_state.terdaftar_massal}/{st.session_state.kuota_massal_total}", "+3 Pasien Baru")
    with col2:
        st.metric("Sisa Antrean Reguler Hari Ini", f"{st.session_state.kuota_reguler} Kursi", "Tersedia")
    
    st.write("### Grafik Keterisian Kuota")
    persen = int((st.session_state.terdaftar_massal / st.session_state.kuota_massal_total) * 100)
    st.progress(persen)
    st.caption(f"Sudah terisi {persen}% dari total kapasitas sunat massal bulan Juni.")

# --- MENU: KALKULATOR METODE (SINKRON KE DAFTAR) ---
elif menu == "📐 Kalkulator Metode Smart":
    st.markdown("<h2 class='subheader-style'>Smart Method Selector 📐</h2>", unsafe_allow_html=True)
    st.write("Gunakan fitur ini untuk menentukan paket terbaik bagi buah hati Anda.")
    
    col1, col2 = st.columns(2)
    with col1:
        usia = st.number_input("Usia Anak (Tahun)", 0, 18, 7)
        kondisi = st.selectbox("Kondisi Fisik Anak", ["Normal", "Gemuk (Micro Penis)", "Phimosis (Perlekatan)"])
    with col2:
        aktif = st.select_slider("Tingkat Aktivitas", options=["Sangat Tenang", "Normal", "Sangat Aktif"])
        keinginan = st.selectbox("Prioritas Hasil", ["Tanpa Jahitan", "Bisa Langsung Mandi", "Estetika Sempurna"])

    if st.button("Dapatkan Rekomendasi Medis ✨"):
        # Logika Penentuan
        if kondisi == "Gemuk (Micro Penis)":
            st.session_state.rekomendasi_metode = "Khitan Gemuk (Spesialis)"
            penjelasan = "Dibutuhkan teknik khusus bedah minor untuk hasil fungsional yang optimal."
        elif aktif == "Sangat Aktif" or keinginan == "Bisa Langsung Mandi":
            st.session_state.rekomendasi_metode = "Khitan Metode Klem"
            penjelasan = "Menggunakan alat klem yang melindungi luka sehingga anak bebas bergerak dan mandi."
        elif usia > 11 or keinginan == "Estetika Sempurna":
            st.session_state.rekomendasi_metode = "Khitan Metode Stapler"
            penjelasan = "Teknologi terbaru sekali pakai yang memberikan hasil sangat rapi tanpa jahitan manual."
        else:
            st.session_state.rekomendasi_metode = "Khitan Reguler"
            penjelasan = "Metode laser cauter yang efisien dan ekonomis untuk anak usia sekolah."
            
        st.markdown(f"""
            <div class="result-box">
                <h3>Rekomendasi Utama: {st.session_state.rekomendasi_metode}</h3>
                <p><b>Analisis Dokter:</b> {penjelasan}</p>
                <hr>
                <p><i>Hasil ini telah disimpan. Silahkan langsung menuju menu <b>Pendaftaran Digital</b> untuk memesan jadwal.</i></p>
            </div>
        """, unsafe_allow_html=True)

# --- MENU: PENDAFTARAN (AUTO-SYNC) ---
elif menu == "📝 Pendaftaran Digital":
    st.markdown("<h2 class='subheader-style'>Formulir Pendaftaran Pasien 📝</h2>", unsafe_allow_html=True)
    
    # Sinkronisasi Otomatis dengan Kalkulator
    list_metode = list(data_dokter_lengkap.keys())
    idx_default = list_metode.index(st.session_state.rekomendasi_metode)
    
    with st.form("pendaftaran_form"):
        st.write("### Data Pasien & Jadwal")
        c1, c2 = st.columns(2)
        with c1:
            nama = st.text_input("Nama Lengkap Anak")
            ortu = st.text_input("Nama Orang Tua / Wali")
        with c2:
            layanan = st.selectbox("Jenis Layanan", ["Reguler (Berbayar)", "Massal (Promo/Gratis)"])
            tgl = st.date_input("Rencana Tanggal", min_value=datetime.now())
        
        st.divider()
        st.write("### Pilihan Paket")
        # Field ini terisi otomatis dari hasil kalkulator tadi
        paket = st.selectbox("Metode Khitan (Rekomendasi Terpilih)", list_metode, index=idx_default)
        
        pesan = st.text_area("Catatan Tambahan (Riwayat Alergi, dll)")
        konfirmasi = st.checkbox("Saya setuju dengan syarat dan ketentuan tindakan medis.")
        
        if st.form_submit_button("SUBMIT PENDAFTARAN ✨"):
            if not nama or not konfirmasi:
                st.error("Mohon isi nama dan setujui konfirmasi.")
            else:
                # EFEK BINTANG MELAYANG (Snow)
                st.snow()
                
                # Update Kuota
                if layanan == "Reguler (Berbayar)": st.session_state.kuota_reguler -= 1
                else: st.session_state.terdaftar_massal += 1
                
                st.markdown(f"""
                    <div class="result-box">
                        <h3>✅ Pendaftaran Berhasil Disimpan!</h3>
                        <p><b>No. Antrean:</b> RSA-{datetime.now().strftime('%y%m%d')}-09</p>
                        <p><b>Nama Anak:</b> {nama}</p>
                        <p><b>Paket:</b> {paket}</p>
                        <p><b>Dokter PJ:</b> {data_dokter_lengkap[paket]['dokter']}</p>
                        <p><b>Tanggal Kedatangan:</b> {tgl.strftime('%d %B %Y')}</p>
                        <hr>
                        <p>Silahkan screenshot halaman ini dan tunjukkan ke resepsionis saat kedatangan.</p>
                    </div>
                """, unsafe_allow_html=True)

# --- MENU: PANDUAN ---
elif menu == "💊 Panduan Pasca-Khitan":
    st.markdown("<h2 class='subheader-style'>Panduan Perawatan & Pemulihan 💊</h2>", unsafe_allow_html=True)
    
    fase = st.radio("Pilih Fase Pemulihan:", ["24 Jam Pertama (Kritis)", "Hari ke 2-5 (Penyembuhan)", "Hari ke 7+ (Pelepasan Alat)"])
    
    if fase == "24 Jam Pertama (Kritis)":
        st.markdown("""<div class="result-box">
            <h3>🛡️ Penanganan Awal</h3>
            <ul>
                <li>Berikan obat anti-nyeri tepat waktu setiap 4-6 jam.</li>
                <li>Gunakan celana sunat (batok) agar luka tidak tergesek.</li>
                <li>Jika terjadi rembesan darah sedikit, tekan perlahan dengan kassa steril.</li>
                <li>Pastikan anak tetap terhidrasi dengan baik.</li>
            </ul>
        </div>""", unsafe_allow_html=True)
    elif fase == "Hari ke 2-5 (Penyembuhan)":
        st.markdown("""<div class="result-box">
            <h3>🚿 Kebersihan & Aktivitas</h3>
            <ul>
                <li>Untuk metode Klem/Stapler, anak diperbolehkan mandi seperti biasa.</li>
                <li>Bersihkan sisa buang air kecil dengan tissue basah non-alkohol atau kassa.</li>
                <li>Teteskan minyak antiseptik (jika dibekali) pada ujung penis.</li>
                <li>Hindari aktivitas berat seperti bersepeda atau melompat berlebihan.</li>
            </ul>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown("""<div class="result-box">
            <h3>🏥 Kontrol & Finalisasi</h3>
            <p>Datang kembali ke klinik sesuai jadwal kontrol. Untuk metode klem, alat akan dilepas oleh tenaga medis kami. Pastikan luka sudah mengering sempurna sebelum anak kembali berolahraga berat.</p>
        </div>""", unsafe_allow_html=True)

# --- MENU: TENTANG KAMI (SEJARAH & STRUKTUR) ---
elif menu == "🏢 Tentang Kami":
    st.markdown("<h2 class='subheader-style'>Profil Rumah Sunat Anak 🏢</h2>", unsafe_allow_html=True)
    
    st.markdown("""<div class="result-box">
        <p><b>Sejarah & Latar Belakang:</b><br>
        Rumah Sunat Anak didirikan pada tahun 2015 di bawah naungan Yayasan Medika Nusantara. Berawal dari sebuah klinik kecil, kami melihat tingginya tingkat trauma anak pasca-khitan akibat metode konvensional. 
        Oleh karena itu, kami bertransformasi menjadi pusat khitan modern yang hanya menggunakan metode bersertifikasi internasional. 
        Dalam 10 tahun terakhir, kami telah berhasil mengkhitan lebih dari 15.000 anak dari berbagai daerah, menjadikannya salah satu rujukan utama di Indonesia. 
        Filosofi kami adalah 'Khitan Tanpa Tangis', yang kami wujudkan melalui manajemen nyeri yang komprehensif dan lingkungan klinik yang ramah anak (Playground Area & VR Cinema saat tindakan).</p>
    </div>""", unsafe_allow_html=True)

    # Struktur Organisasi Luas
    st.markdown("<h3 style='color:white; text-shadow:1px 1px #000;'>Struktur Organisasi Klinik</h3>", unsafe_allow_html=True)
    org_data = pd.DataFrame({
        "Divisi": ["Direktur Utama", "Kepala Medis", "Manajer Operasional", "Humas & Edukasi", "Admin & IT Support", "Kepala Perawat", "Manajemen Fasilitas"],
        "Nama Pejabat": ["H. Salim Wijaya, M.M", "dr. Ahmad Subarjo", "Rina Kartika, S.E", "Bambang Pamungkas", "Anita Sari, S.Kom", "Ns. Siti Khadijah", "Doni Setiawan"]
    })
    st.table(org_data)

    # 8 Dokter Spesialis (Teks Hitam)
    st.markdown("<h3 style='color:white; text-shadow:1px 1px #000;'>Tim Dokter Spesialis & Tenaga Ahli</h3>", unsafe_allow_html=True)
    list_dr = []
    for k, v in data_dokter_lengkap.items():
        list_dr.append({"Nama Dokter": v['dokter'], "Keahlian Spesifik": v['spesialis']})
    
    st.table(pd.DataFrame(list_dr))

    st.info("Seluruh tenaga medis kami telah tersertifikasi oleh Perhimpunan Khitan Indonesia (PKI).")
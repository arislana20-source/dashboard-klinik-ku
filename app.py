import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# 1. Konfigurasi Halaman
st.set_page_config(
    page_title="Rumah Sunat Anak | Modern & Nyaman", 
    page_icon="🌙", 
    layout="wide"
)

# --- INISIALISASI KUOTA (Session State) ---
if 'kuota_massal' not in st.session_state:
    st.session_state.kuota_massal = 50
if 'kuota_reguler' not in st.session_state:
    st.session_state.kuota_reguler = 8
if 'terdaftar_massal' not in st.session_state:
    st.session_state.terdaftar_massal = 5

# 2. CSS Kustom
st.markdown("""
    <style>
    .stApp { background-color: #B2AC88; } 
    .klinik-title {
        color: #2E473B; text-align: center; font-size: 50px; font-weight: bold;
        text-shadow: 2px 2px #E0E5D9; font-family: 'Verdana', sans-serif;
    }
    .klinik-dalil { color: #2E473B; text-align: center; font-style: italic; font-size: 18px; margin-bottom: 30px; }
    .result-box {
        background-color: #E0E5D9; 
        padding: 25px; 
        border-radius: 15px; 
        border: 3px solid #2E473B;
        margin-top: 20px;
    }
    .result-box h3, .result-box p, .result-box b { color: #2E473B !important; }
    [data-testid="stSidebar"] { background-color: #2E473B; }
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] h2 { color: #E0E5D9 !important; }
    </style>
""", unsafe_allow_html=True)

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

st.markdown("<h1 class='klinik-title'>RUMAH SUNAT ANAK</h1>", unsafe_allow_html=True)

# --- 1. CEK KUOTA (DIPERBARUI) ---
if menu == "📊 Cek Kuota":
    st.subheader("Ketersediaan Kuota Real-Time 📊")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Kuota Khitan Massal (Juni)", f"{st.session_state.terdaftar_massal}/{st.session_state.kuota_massal}", "Update Live")
    with col2:
        st.metric("Sisa Kuota Reguler Hari Ini", f"{st.session_state.kuota_reguler} Kursi", "-1 Baru Saja" if st.session_state.kuota_reguler < 8 else "Full")
    
    persen_massal = (st.session_state.terdaftar_massal / st.session_state.kuota_massal) * 100
    st.progress(int(persen_massal))
    st.write(f"Tingkat keterisian sunat massal: {int(persen_massal)}%")

# --- 2. PENDAFTARAN (DENGAN LOGIKA PENGURANG KUOTA) ---
elif menu == "📝 Pendaftaran":
    st.subheader("Formulir Pendaftaran & Jadwal 📝")
    
    with st.form("daftar_form"):
        nama = st.text_input("Nama Anak")
        jenis_layanan = st.selectbox("Jenis Layanan", ["Khitan Reguler (Harian)", "Khitan Massal (Promo)"])
        metode_fix = st.selectbox("Pilih Metode", list(data_dokter.keys()))
        tgl_rencana = st.date_input("Rencana Tanggal Kedatangan", min_value=datetime.now())
        
        submit = st.form_submit_button("Konfirmasi Pendaftaran ✨")
        
        if submit:
            if nama == "":
                st.error("Mohon isi nama anak terlebih dahulu.")
            else:
                # Logika Pengurangan Kuota
                bisa_daftar = False
                if jenis_layanan == "Khitan Reguler (Harian)":
                    if st.session_state.kuota_reguler > 0:
                        st.session_state.kuota_reguler -= 1
                        bisa_daftar = True
                    else:
                        st.error("Maaf, kuota reguler hari ini sudah habis!")
                
                else: # Khitan Massal
                    if st.session_state.terdaftar_massal < st.session_state.kuota_massal:
                        st.session_state.terdaftar_massal += 1
                        bisa_daftar = True
                    else:
                        st.error("Maaf, kuota sunat massal sudah penuh!")

                if bisa_daftar:
                    st.balloons()
                    # Format Tanggal
                    hari_ini = tgl_rencana.strftime("%A")
                    # Translate hari sederhana
                    hari_indo = {"Monday": "Senin", "Tuesday": "Selasa", "Wednesday": "Rabu", "Thursday": "Kamis", "Friday": "Jumat", "Saturday": "Sabtu", "Sunday": "Minggu"}
                    
                    st.markdown(f"""
                    <div class="result-box">
                        <h3>Pendaftaran Berhasil! ✅</h3>
                        <p><b>Nama Pasien:</b> {nama}</p>
                        <p><b>Jenis Layanan:</b> {jenis_layanan}</p>
                        <p><b>Jadwal Sunat:</b> {hari_indo.get(hari_ini, hari_ini)}, {tgl_rencana.strftime('%d %B %Y')}</p>
                        <p><b>Dokter Penanggung Jawab:</b> {data_dokter[metode_fix]['dokter']}</p>
                        <hr>
                        <p style='font-size: 14px;'><i>Silahkan datang 15 menit sebelum jadwal. Tunjukkan bukti ini kepada admin.</i></p>
                    </div>
                    """, unsafe_allow_html=True)

# --- MENU LAINNYA (TETAP SAMA) ---
elif menu == "🏠 Beranda":
    st.subheader("Selamat Datang di Rumah Sunat Anak 🌙")
    st.write("Tempat sunat modern yang mengutamakan kenyamanan psikologis anak dan keamanan medis.")
    st.image("https://cdn-icons-png.flaticon.com/512/2864/2864413.png", width=200)

elif menu == "📐 Kalkulator Metode":
    # (Isi sama seperti kode lama Anda)
    st.subheader("Smart Method Selector 📐")
    usia = st.number_input("Usia Anak (Tahun)", 0, 15, 7)
    aktif = st.select_slider("Tingkat Aktivitas Anak", options=["Sangat Tenang", "Normal", "Sangat Aktif"])
    
    if st.button("Rekomendasikan Metode ✨"):
        st.success("Rekomendasi telah dibuat (Gunakan Metode Klem untuk anak aktif).")

elif menu == "💊 Panduan Perawatan":
    st.subheader("Post-Op Care Guide 💊")
    st.info("Gunakan celana sunat dan minum obat pereda nyeri secara teratur.")

elif menu == "🏢 Tentang Kami":
    st.subheader("Profil Rumah Sunat")
    st.table(pd.DataFrame({
        "Jabatan": ["Kepala Klinik", "Spesialis Bedah"],
        "Nama": ["dr. Ahmad Subarjo", "dr. Zulkifli, Sp.B"]
    }))
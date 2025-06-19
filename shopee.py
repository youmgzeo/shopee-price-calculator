import streamlit as st

st.markdown("""
    <style>
    html, body, [class*="css"] {
        font-size: 18px !important;
    }

    .stNumberInput > div > input {
        font-size: 18px !important;
    }

    .stButton>button {
        font-size: 18px !important;
        padding: 0.6rem 1.4rem;
    }

    .warning-box {
        background-color: #ffcccc;
        padding: 10px;
        border-radius: 5px;
        font-size: 16px;
        margin-top: 15px;
        margin-bottom: 10px;
    }

    .stCaption, .stMarkdown, .stText, .stSubheader {
        font-size: 18px !important;
    }
    </style>
""", unsafe_allow_html=True)

def hitung_harga_jual(bersih, p_admin, p_premi, p_layanan, p_promo, biaya_program, biaya_proses):
    layanan_max = 20000
    promo_max = 10000
    flat_biaya = biaya_program + biaya_proses
    x = bersih + flat_biaya
    while True:
        admin = p_admin * x
        premi = p_premi * x
        layanan = min(p_layanan * x, layanan_max)
        promo = min(p_promo * x, promo_max)
        total_biaya = admin + premi + layanan + promo + flat_biaya
        if x - total_biaya >= bersih:
            return round(x)
        x += 1

st.title("Kalkulator Harga Jual Shopee")

st.subheader("Pengaturan Biaya Tambahan")

st.markdown(
    """
    <div style='background-color: #ffcccc; padding: 10px; border-radius: 5px;'>
        Harap isi biaya ter-update berdasarkan kebijakan Shopee dengan benar.
    </div>
    """,
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)
with col1:
    p_admin = st.number_input("Biaya Admin (%)", value=0.0, step=0.1) / 100
    p_promo = st.number_input("Biaya Promo Xtra (%)", value=0.0, step=0.1) / 100
    p_layanan = st.number_input("Biaya Layanan Gratis Ongkir Xtra (%)", value=0.0, step=0.1) / 100
with col2:
    p_premi = st.number_input("Biaya Premi Asuransi (%)", value=0.0, step=0.1) / 100
    biaya_program = st.number_input("Biaya Program Hemat Pengembalian (Rp)", value=0, step=100)
    biaya_proses = st.number_input("Biaya Proses Pesanan (Rp)", value=0, step=100)

# Inisialisasi daftar input
if "harga_bersih_list" not in st.session_state:
    st.session_state.harga_bersih_list = [10000]

st.subheader("Target Penghasilan Bersih")

st.markdown(
    """
    <div class='warning-box'>
        Masukkan jumlah penghasilan bersih yang Anda harapkan dari produk yang dijual.
        <br>Contoh: jika Anda menjual Photocard seharga <strong>Rp120.000</strong> dengan biaya packing sebesar <strong>Rp3.000</strong>,
        maka isikan <strong>Rp123.000</strong> sebagai penghasilan bersih.
        <br>Harga jual yang dihitung adalah harga yang perlu Anda pasang di Shopee.
    </div>
    """,
    unsafe_allow_html=True
)

# Tombol tambah
col_tambah, col_reset = st.columns([1, 1])
with col_tambah:
    if st.button("➕ Tambah Input") and len(st.session_state.harga_bersih_list) < 10:
        st.session_state.harga_bersih_list.append(10000)

# Tampilkan semua input + tombol hapus
hapus_index = None
for i, val in enumerate(st.session_state.harga_bersih_list):
    col1, col2 = st.columns([6, 1])
    with col1:
        st.session_state.harga_bersih_list[i] = st.number_input(
            f"Penghasilan bersih ke-{i+1} (Rp)", min_value=1000, step=1000, value=val, key=f"input_{i}"
        )
    with col2:
        if i > 0:  # baris pertama tidak bisa dihapus
            if st.button("🗑️", key=f"hapus_{i}"):
                hapus_index = i

if hapus_index is not None:
    st.session_state.harga_bersih_list.pop(hapus_index)

# Tombol hitung
if st.button("Hitung Harga Jual"):
    st.subheader("Hasil Perhitungan")
    for i, bersih in enumerate(st.session_state.harga_bersih_list):
        harga_jual = hitung_harga_jual(bersih, p_admin, p_premi, p_layanan, p_promo, biaya_program, biaya_proses)
        st.write(f"Untuk penghasilan bersih Rp {bersih:,} → harga jual: **Rp {harga_jual:,}**")
    st.caption("Catatan: disarankan untuk membulatkan harga jual ke atas agar penghasilan tidak terlalu mepet.")

# Footer
st.markdown(
    """
    <hr style="margin-top: 30px; margin-bottom: 10px;">
    <div style='text-align: center; font-size: 14px;'>
        Dibuat oleh youmgzeo dan terinspirasi dari lhsnimarchieve & geniustangerine.<br>
        Jika ada kritik atau saran, Anda dapat menghubungi <a href='https://x.com/youmgzeo' target='_blank'>@youmgzeo</a>.
    </div>
    """,
    unsafe_allow_html=True
)

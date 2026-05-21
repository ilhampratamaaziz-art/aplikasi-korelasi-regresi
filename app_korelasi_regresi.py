import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import pearsonr,spearmanr
import matplotlib.pyplot as plt

# ========================
# KONFIGURASI
# ========================

st.set_page_config(
page_title="Korelasi Regresi",
page_icon="📊",
layout="wide"
)

# ========================
# CSS
# ========================

st.markdown("""
<style>

.stApp{
background:
linear-gradient(
135deg,
#0f172a,
#1e293b,
#334155
);
}

h1{

text-align:center;

color:white;

font-size:40px;

}

.block-container{

background:
rgba(255,255,255,0.05);

padding:30px;

border-radius:30px;

box-shadow:
0px 8px 32px
rgba(0,0,0,0.3);

}

.stButton button{

width:100%;

height:55px;

border-radius:20px;

font-weight:bold;

font-size:18px;

}

.stButton button:hover{

transform:scale(1.03);

transition:0.3s;

}

</style>

""",unsafe_allow_html=True)

# ========================
# SIDEBAR
# ========================

with st.sidebar:

    st.image(
    "logo_teknokrat.png",
    width=180
    )

    st.title(
    "Universitas Teknokrat Indonesia"
    )

    st.markdown("---")

    st.subheader(
    "Kelompok"
    )

    st.write(
    "M. ILHAM PRATAMA AZIZ"
    )

    st.write(
    "FARHAN GUNARSO"
    )

    st.write(
    "GIAN GABRIEL BAGITU"
    )

    st.write(
    "SAFEL RISKI RAMADHAN"
    )

    st.write(
    "REIHAN ADI PERMANA"
    )

    st.markdown("---")

    menu=st.selectbox(

    "Pilih Menu",

    [

    "Analisis",

    "Tentang"

    ]

    )

# ========================
# HALAMAN TENTANG
# ========================

if menu=="Tentang":

    st.title(
    "Tentang Aplikasi"
    )

    st.write("""

Aplikasi ini dibuat
untuk:

✔ Analisis Korelasi Pearson

✔ Korelasi Spearman

✔ Regresi Linear

✔ Prediksi Data

✔ Statistik

Dibangun menggunakan:

Python

Streamlit

Matplotlib

Scipy

Pandas

""")

    st.stop()

# ========================
# SESSION
# ========================

if "hasil" not in st.session_state:

    st.session_state.hasil=None

if "a" not in st.session_state:

    st.session_state.a=None

if "b" not in st.session_state:

    st.session_state.b=None

# ========================
# JUDUL
# ========================

st.markdown("""

<h1>

📊 Aplikasi Korelasi & Regresi

</h1>

""",unsafe_allow_html=True)

st.markdown("---")

# ========================
# INPUT
# ========================

kiri,kanan=st.columns(2)

with kiri:

    x_input=st.text_area(

    "Masukkan Data X",

    "10,20,30,40,50"

    )

with kanan:

    y_input=st.text_area(

    "Masukkan Data Y",

    "15,25,35,45,55"

    )

uploaded=st.file_uploader(

"Upload CSV / Excel",

type=["csv","xlsx"]

)

# ========================
# AMBIL DATA
# ========================

try:

    if uploaded:

        if uploaded.name.endswith(".csv"):

            df=pd.read_csv(
            uploaded
            )

        else:

            df=pd.read_excel(
            uploaded
            )

        x=np.array(
        df.iloc[:,0]
        )

        y=np.array(
        df.iloc[:,1]
        )

    else:

        x=np.array(
        list(
        map(
        float,
        x_input.split(",")
        )
        )
        )

        y=np.array(
        list(
        map(
        float,
        y_input.split(",")
        )
        )
        )

except:

    st.error(
    "Format Salah"
    )

    st.stop()

# ========================
# HITUNG
# ========================

if st.button(
"HITUNG ANALISIS"
):

    with st.spinner(
    "Menghitung..."
    ):

        pearson,_=pearsonr(
        x,y
        )

        spearman,_=spearmanr(
        x,y
        )

        b,a=np.polyfit(
        x,
        y,
        1
        )

        st.session_state.a=a
        st.session_state.b=b

        prediksi=a+b*x

        r2=np.corrcoef(
        x,
        y
        )[0,1]**2

        st.session_state.hasil={

        "pearson":pearson,

        "spearman":spearman,

        "r2":r2,

        "x":x,

        "y":y,

        "prediksi":prediksi

        }

# ========================
# HASIL
# ========================

if st.session_state.hasil:

    h=st.session_state.hasil

    a,b,c=st.columns(3)

    a.metric(
    "Pearson",
    f"{h['pearson']:.4f}"
    )

    b.metric(
    "Spearman",
    f"{h['spearman']:.4f}"
    )

    c.metric(
    "R²",
    f"{h['r2']:.4f}"
    )

    fig,ax=plt.subplots()

    ax.scatter(
    h["x"],
    h["y"]
    )

    ax.plot(
    h["x"],
    h["prediksi"],
    linewidth=3
    )

    ax.grid()

    st.pyplot(fig)

# ========================
# PREDIKSI
# ========================

if st.session_state.a!=None:

    st.subheader(
    "Prediksi"
    )

    nilai=st.number_input(
    "Masukkan X Prediksi"
    )

    if st.button(
    "PREDIKSI"
    ):

        hasil=(
        st.session_state.a+
        st.session_state.b*nilai
        )

        st.success(
        f"Hasil Prediksi Y = {hasil:.2f}"
        )

st.markdown("---")

st.markdown("""

<div style='text-align:center'>

Dibuat Oleh Kelompok

Universitas Teknokrat Indonesia

2026

</div>

""",unsafe_allow_html=True)
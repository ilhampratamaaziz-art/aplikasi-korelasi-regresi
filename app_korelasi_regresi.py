import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import pearsonr, spearmanr
import matplotlib.pyplot as plt

# =============================
# KONFIGURASI
# =============================

st.set_page_config(
    page_title="Korelasi Regresi",
    page_icon="📊",
    layout="wide"
)

# =============================
# CSS CUSTOM
# =============================

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
font-size:42px;
}

.block-container{

background:
rgba(255,255,255,0.05);

padding:30px;

border-radius:30px;

box-shadow:
0px 8px 32px
rgba(0,0,0,0.4);

}

.stTextArea textarea,
.stNumberInput input{

border-radius:15px;

border:2px solid #60a5fa;

}

.stButton button{

width:100%;

height:55px;

font-size:18px;

font-weight:bold;

border-radius:20px;

transition:0.3s;

}

.stButton button:hover{

transform:scale(1.02);

}

[data-testid="stFileUploader"]{

border:2px dashed #60a5fa;

padding:15px;

border-radius:20px;

}

div[data-testid="metric-container"]{

background:#111827;

padding:15px;

border-radius:20px;

}

</style>
""",unsafe_allow_html=True)

# =============================
# JUDUL
# =============================

st.markdown("""
<h1>
📊 Aplikasi Korelasi & Regresi
</h1>
""",unsafe_allow_html=True)

st.markdown("---")

# =============================
# SESSION
# =============================

if "hasil" not in st.session_state:
    st.session_state.hasil=None

if "a" not in st.session_state:
    st.session_state.a=None

if "b" not in st.session_state:
    st.session_state.b=None

# =============================
# INPUT
# =============================

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

# =============================
# BACA DATA
# =============================

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

        st.success(
        "Data berhasil diimport"
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
    "Format data salah"
    )

    st.stop()

# =============================
# HITUNG
# =============================

if st.button(
"HITUNG ANALISIS"
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

    ss_total=np.sum(
    (y-np.mean(y))**2
    )

    ss_res=np.sum(
    (y-prediksi)**2
    )

    r2=1-(ss_res/ss_total)

    hasil={

    "pearson":pearson,

    "spearman":spearman,

    "r2":r2,

    "meanx":np.mean(x),

    "meany":np.mean(y),

    "medianx":np.median(x),

    "mediany":np.median(y),

    "stdx":np.std(x),

    "stdy":np.std(y),

    "x":x,

    "y":y,

    "prediksi":prediksi

    }

    st.session_state.hasil=hasil

# =============================
# TAMPILKAN
# =============================

if st.session_state.hasil:

    h=st.session_state.hasil

    st.subheader(
    "Hasil Analisis"
    )

    c1,c2,c3=st.columns(3)

    c1.metric(
    "Pearson",
    f"{h['pearson']:.4f}"
    )

    c2.metric(
    "Spearman",
    f"{h['spearman']:.4f}"
    )

    c3.metric(
    "R²",
    f"{h['r2']:.4f}"
    )

    st.markdown("---")

    a1,a2,a3=st.columns(3)

    a1.metric(
    "Mean X",
    f"{h['meanx']:.2f}"
    )

    a2.metric(
    "Mean Y",
    f"{h['meany']:.2f}"
    )

    a3.metric(
    "Median X",
    f"{h['medianx']:.2f}"
    )

    b1,b2,b3=st.columns(3)

    b1.metric(
    "Median Y",
    f"{h['mediany']:.2f}"
    )

    b2.metric(
    "Std X",
    f"{h['stdx']:.2f}"
    )

    b3.metric(
    "Std Y",
    f"{h['stdy']:.2f}"
    )

    st.markdown("---")

    st.subheader(
    "Grafik Korelasi & Regresi"
    )

    fig,ax=plt.subplots(
    figsize=(10,5)
    )

    ax.scatter(
    h["x"],
    h["y"]
    )

    ax.plot(
    h["x"],
    h["prediksi"],
    linewidth=3
    )

    ax.set_xlabel(
    "X"
    )

    ax.set_ylabel(
    "Y"
    )

    ax.grid()

    st.pyplot(
    fig
    )

# =============================
# PREDIKSI
# =============================

if st.session_state.a is not None:

    st.markdown("---")

    st.subheader(
    "Prediksi Nilai"
    )

    nilai=st.number_input(
    "Masukkan X Prediksi",
    value=0.0
    )

    if st.button(
    "PREDIKSI"
    ):

        hasil=(
        st.session_state.a+
        st.session_state.b*nilai
        )

        st.success(
        f"Prediksi Y = {hasil:.2f}"
        )
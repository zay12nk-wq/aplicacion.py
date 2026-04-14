import streamlit as st
import pandas as pd
import os
import io

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="Sistema Retenciones PRO", layout="wide")

# =========================
# 🎨 ESTILO
# =========================
st.markdown("""
<style>
.stApp { background-color: #0f172a; }

h1 {
    color: white;
    text-align: center;
}

.kpi {
    background: #020617;
    padding: 20px;
    border-radius: 10px;
    text-align: center;
    color: white;
}

.kpi-value {
    font-size: 28px;
    color: #22c55e;
    font-weight: bold;
}

/* Firma */
.firma {
    position: fixed;
    bottom: 10px;
    right: 20px;
    color: #94a3b8;
    font-size: 12px;
    font-style: italic;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>💼 Sistema Contable de Retenciones</h1>", unsafe_allow_html=True)

# =========================
# CARGAR EXCEL
# =========================
ruta = os.path.join(os.getcwd(), "retenciones_colombia.xlsx")
df = pd.read_excel(ruta)

# =========================
# INPUTS
# =========================
col1, col2 = st.columns(2)

with col1:
    valor = st.number_input("💰 Base", min_value=0, step=1000)

with col2:
    ciudad = st.selectbox("🏙️ Ciudad", df["Ciudad"].unique())

df_ciudad = df[df["Ciudad"] == ciudad].copy()

# =========================
# FORMATO CONTABLE
# =========================
def formato_tarifa(t):
    if t < 0.1:
        return f"{t*1000:.2f} x mil"
    else:
        return f"{t*100:.2f} %"

df_ciudad["Retención"] = df_ciudad["Tarifa"] * valor

df_ciudad["Tarifa Formato"] = df_ciudad["Tarifa"].apply(formato_tarifa)
df_ciudad["Retención ($)"] = df_ciudad["Retención"].apply(lambda x: f"${x:,.0f}")

# =========================
# ORDENAR
# =========================
df_ciudad = df_ciudad.sort_values(by="Retención", ascending=False)

# =========================
# KPI
# =========================
total = df_ciudad["Retención"].sum()

st.markdown(f"""
<div class="kpi">
    <div>Total Retenciones</div>
    <div class="kpi-value">${total:,.0f}</div>
</div>
""", unsafe_allow_html=True)

# =========================
# TABLA
# =========================
st.subheader("📊 Detalle de Retenciones")

st.dataframe(
    df_ciudad[["Concepto", "Tarifa Formato", "Retención ($)"]],
    use_container_width=True
)

# =========================
# EXPORTAR EXCEL
# =========================
st.subheader("📥 Exportar Reporte Profesional")

export_df = df_ciudad[["Concepto", "Tarifa Formato", "Retención"]].copy()

buffer = io.BytesIO()

with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
    export_df.to_excel(writer, index=False, sheet_name="Reporte")

st.download_button(
    label="⬇️ Descargar Excel",
    data=buffer.getvalue(),
    file_name=f"reporte_retenciones_{ciudad}.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

# =========================
# ✍️ FIRMA
# =========================
st.markdown("""
<div class="firma">
Nohora Portillo
</div>
""", unsafe_allow_html=True)
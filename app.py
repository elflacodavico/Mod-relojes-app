import streamlit as st
from PIL import Image

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Mod Relojes IA", layout="wide")

st.title("🛠️ Laboratorio de Mods NH35")
st.write("Sube tus piezas, verifica compatibilidad y visualiza tu mod.")

# --- BARRA LATERAL (Tus controles) ---
with st.sidebar:
    st.header("1. Elige tu Base (Caja)")
    
    # Selector de Estilo
    estilo = st.selectbox("Estilo de Caja", ["Submariner (Diver)", "Datejust (Dress)", "Pilot"])
    
    # Lógica de Tamaños (Condicionales)
    if estilo == "Submariner (Diver)":
        tamano = st.selectbox("Diámetro", ["40mm", "41mm"])
        corona = st.radio("Posición Corona", ["3.0", "3.8 (Seiko SKX)"])
    elif estilo == "Datejust (Dress)":
        tamano = st.selectbox("Diámetro", ["36mm", "39mm", "41mm"])
        corona = "3.0" # Fijo
        st.info("ℹ️ Los tipo Rolex siempre llevan corona a las 3.")
    else:
        tamano = "42mm"
        corona = "3.0"

    st.header("2. El Dial (Esfera)")
    # AQUÍ ESTÁ LO QUE QUERÍAS: SUBIR FOTO
    archivo_dial = st.file_uploader("Sube una foto o captura del Dial (AliExpress)", type=["png", "jpg", "jpeg"])

# --- ÁREA PRINCIPAL (Visualización) ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("📋 Especificaciones Técnicas")
    st.markdown(f"""
    * **Movimiento Base:** Seiko NH35 (Automático)
    * **Caja Seleccionada:** {estilo} - {tamano}
    * **Posición Corona:** {corona}
    * **Diámetro Dial Requerido:** 28.5mm
    """)
    
    # Lógica de Compatibilidad (El "Cerebro")
    if corona == "3.8 (Seiko SKX)":
        st.warning("⚠️ **ATENCIÓN:** Has elegido una caja con corona a las 4. Asegúrate que tu dial tenga 4 patas o tendrás que cortarlas.")
    else:
        st.success("✅ Configuración estándar (Corona a las 3). La mayoría de diales funcionarán.")

with col2:
    st.subheader("🖼️ Visualización Previa")
    
    if archivo_dial is not None:
        # Si el usuario subió foto, la mostramos
        imagen = Image.open(archivo_dial)
        st.image(imagen, caption="Tu posible Dial", width=300)
        st.success("¡Imagen cargada! (En el futuro aquí superpondremos la caja)")
    else:
        st.info("👈 Sube una imagen en el menú de la izquierda para verla aquí.")

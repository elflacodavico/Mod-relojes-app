import streamlit as st
from PIL import Image
# OJO: YA NO IMPORTAMOS REMBG AQUÍ ARRIBA PARA QUE NO SE CUELGUE AL INICIO

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Mod Lab NH35", layout="wide")

st.title("🛠️ Laboratorio de Mods NH35 - Fase 2")

# --- BARRA LATERAL ---
with st.sidebar:
    st.header("1. La Caja")
    estilo = st.selectbox("Estilo", ["Submariner (Diver)", "Datejust (Dress)"])
    
    st.header("2. El Dial")
    archivo_dial = st.file_uploader("Sube tu Dial", type=["png", "jpg", "jpeg"])

# --- ZONA DE TRABAJO ---
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("🎛️ Mesa de Trabajo")
    if archivo_dial is not None:
        rotacion = st.slider("Rotar", -180, 180, 0)
        tamano_percent = st.slider("Tamaño (%)", 10, 150, 100)
        
        # Checkbox para activar la IA
        usar_ia = st.checkbox("🪄 Usar IA (Puede tardar)", value=False) # Empezamos en False para no bloquear
        
    else:
        st.info("👈 Sube una imagen")

with col2:
    st.subheader("👁️ Visualización")
    
    if archivo_dial is not None:
        imagen_original = Image.open(archivo_dial)
        imagen_procesada = imagen_original

        # --- AQUÍ ESTÁ EL TRUCO (LAZY IMPORT) ---
        if usar_ia:
            with st.spinner('Despertando a la IA... (Esto tarda la primera vez)'):
                try:
                    # IMPORTAMOS SOLO CUANDO HACE FALTA
                    from rembg import remove 
                    imagen_procesada = remove(imagen_original)
                except Exception as e:
                    st.error(f"Error de memoria: {e}")
                    st.warning("El servidor gratuito se quedó sin fuerza. Intenta sin la IA.")

        # Rotación y Tamaño
        imagen_rotada = imagen_procesada.rotate(rotacion * -1, expand=True)
        w, h = imagen_rotada.size
        nuevo_w = int(w * (tamano_percent / 100))
        nuevo_h = int(h * (tamano_percent / 100))
        imagen_final = imagen_rotada.resize((nuevo_w, nuevo_h))
        
        st.image(imagen_final)

import streamlit as st
from PIL import Image
from rembg import remove # Importamos la IA quita-fondos

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Mod Lab NH35", layout="wide")

st.title("🛠️ Laboratorio de Mods NH35 - Fase 2")

# --- BARRA LATERAL (CONTROLES) ---
with st.sidebar:
    st.header("1. La Caja (Chassis)")
    estilo = st.selectbox("Estilo", ["Submariner (Diver)", "Datejust (Dress)"])
    if estilo == "Datejust (Dress)":
        st.image("https://raw.githubusercontent.com/elflacodavico/mod-relojes-app/main/assets/caja_dj_ejemplo.png", caption="Referencia Visual", width=150)
        # Nota: Arriba puse un link roto a propósito, luego te enseño a poner fotos base reales
    
    st.header("2. El Dial (Tu pieza)")
    archivo_dial = st.file_uploader("Sube tu Dial", type=["png", "jpg", "jpeg"])

# --- ZONA DE TRABAJO ---
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("🎛️ Mesa de Trabajo")
    if archivo_dial is not None:
        st.info("Ajusta la imagen para que encaje")
        
        # CONTROLES MANUALES
        rotacion = st.slider("Rotar Dial (Grados)", -180, 180, 0)
        tamano_percent = st.slider("Redimensionar (%)", 10, 200, 100)
        
        # BOTÓN DE IA
        usar_ia = st.checkbox("🪄 Usar IA para borrar fondo", value=True)
        
    else:
        st.warning("👈 Sube una imagen primero")

with col2:
    st.subheader("👁️ Visualización Final")
    
    # LIENZO (CANVAS)
    if archivo_dial is not None:
        # 1. Abrir imagen original
        imagen_original = Image.open(archivo_dial)
        
        # 2. PROCESAMIENTO
        # A. Borrar fondo (Si el checkbox está activo)
        if usar_ia:
            with st.spinner('La IA está limpiando el fondo...'):
                try:
                    imagen_procesada = remove(imagen_original)
                except Exception as e:
                    st.error(f"Error en IA: {e}")
                    imagen_procesada = imagen_original
        else:
            imagen_procesada = imagen_original

        # B. Rotación
        imagen_rotada = imagen_procesada.rotate(rotacion * -1, expand=True) # * -1 para que gire intuitivamente
        
        # C. Redimensión
        width, height = imagen_rotada.size
        nuevo_w = int(width * (tamano_percent / 100))
        nuevo_h = int(height * (tamano_percent / 100))
        imagen_final = imagen_rotada.resize((nuevo_w, nuevo_h))
        
        # MOSTRAR RESULTADO
        st.image(imagen_final, caption="Dial Procesado y Limpio")
        
        st.markdown("---")
        st.success(f"✅ Dial listo para montaje virtual. Orientación: {rotacion}°")

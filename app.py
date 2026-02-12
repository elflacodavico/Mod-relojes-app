import streamlit as st
from PIL import Image

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Mod Lab NH35", layout="wide")

st.title("🛠️ Laboratorio de Mods NH35 - Versión Ligera")

# --- BARRA LATERAL (CONTROLES) ---
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
        # Controles manuales
        rotacion = st.slider("Rotar (Grados)", -180, 180, 0)
        tamano_percent = st.slider("Tamaño (%)", 10, 150, 100)
        
        st.markdown("---")
        # Checkbox para activar la IA
        st.write("🧠 **Inteligencia Artificial**")
        usar_ia = st.checkbox("Quitar fondo (Modo Ahorro)", value=False)
        
    else:
        st.info("👈 Sube una imagen primero")

with col2:
    st.subheader("👁️ Visualización")
    
    if archivo_dial is not None:
        imagen_original = Image.open(archivo_dial)
        imagen_procesada = imagen_original

        # --- LÓGICA DE IA (MODO LIGERO) ---
        if usar_ia:
            with st.spinner('Procesando con modelo ligero (u2netp)...'):
                try:
                    # Importamos AQUÍ DENTRO para que la app no cargue lento al inicio
                    from rembg import remove, new_session
                    
                    # Usamos el modelo "u2netp" (Pocket) que gasta menos RAM
                    session = new_session("u2netp")
                    imagen_procesada = remove(imagen_original, session=session)
                    
                except Exception as e:
                    st.error(f"Error de memoria: {e}")
                    st.warning("El servidor gratuito está saturado. Intenta recargar la página (F5).")

        # --- TRANSFORMACIONES (Rotar y Escalar) ---
        # 1. Rotar
        imagen_rotada = imagen_procesada.rotate(rotacion * -1, expand=True)
        
        # 2. Redimensionar
        w, h = imagen_rotada.size
        nuevo_w = int(w * (tamano_percent / 100))
        nuevo_h = int(h * (tamano_percent / 100))
        imagen_final = imagen_rotada.resize((nuevo_w, nuevo_h))
        
        # 3. Mostrar Resultado
        st.image(imagen_final, caption="Resultado Final")
        
    else:
        st.write("Aquí verás tu diseño.")

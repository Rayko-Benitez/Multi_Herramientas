import streamlit as st
import yt_dlp as youtube_dl
import os


#---------------visual de la pagina y complementos-----------
# Logo
st.sidebar.image("static/logo av sunglass.png", width=100)


# Título y descripción
st.sidebar.title("Aplicación de descargas Youtube")


# Instrucciones de uso
#st.sidebar.header("Instrucciones")

with st.sidebar.expander("Instrucciones:"):
                    st.caption(
                            """
                            1. Paso 1: Selecciona el tipo de archivo que quieres descargar (Audio o Video).
                            2. Paso 2: Añade la URL de la carpeta del equipo donde lo vas a descargar.
                            3. Paso 3: Selecciona la cantidad de URL o enlaces a descargar.
                            4. Paso 4: Si has llenado todo, presiona el botón "Descargar todas"
                            """)




# Interfaz del Menú desplegable

#st.sidebar.write('Selecciona el formato de descarga')
formato = st.sidebar.selectbox("Selecciona el formato de descarga:", ["Audio", "Video"])



#Interfaz de la pagina

# Encabezado principal
st.header("Descarga videos y audios de Youtube")


output_path = st.sidebar.text_input("Ingresa la ruta de la carpeta donde quieres descargar los archivos")  # Carpeta local de descargas

if output_path:
    if not os.path.exists(output_path):
        st.error("La carpeta ingresada no existe. Por favor verifica la ruta.")
    else:
        st.success("Carpeta encontrada. Añade URL e inicia descarga.")


# Inicializar la lista de URLs en session_state
if "url_list" not in st.session_state:
    st.session_state.url_list = [""]  # Comienza con un campo vacío

# Función para añadir un nuevo campo
def add_url_field():
    st.session_state.url_list.append("")  # Añadir un nuevo campo vacío

# Botón para añadir más campos
num_urls = st.sidebar.number_input(
    "Cantidad de URLs", min_value=1, value=len(st.session_state.url_list), step=1
)

# Ajustar el número de campos dinámicamente
if num_urls > len(st.session_state.url_list):
    # Añadir más campos
    st.session_state.url_list.extend([""] * (num_urls - len(st.session_state.url_list)))
elif num_urls < len(st.session_state.url_list):
    # Reducir los campos
    st.session_state.url_list = st.session_state.url_list[:num_urls]

# Mostrar los campos dinámicos
for i, url in enumerate(st.session_state.url_list):
    st.session_state.url_list[i] = st.text_input(f"URL {i+1}", value=url)

# Procesar todas las URLs
if st.button("Descargar todas"):
    if not output_path:
        st.error("Por favor, ingresa la ruta de la carpeta.") 
    else:
        for url in st.session_state.url_list:
            if url.strip():  # Validar que no esté vacío
                st.write(f"Procesando: {url}")
                ydl_opts = {
                    "outtmpl": f"{output_path}/%(title)s.%(ext)s",  # Formato de salida
                    "format": "bestaudio" if formato == "Audio" else "best",  # Formato según selección
                }
                try:
                    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                        with st.spinner("Descargando, por favor espera..."):
                            ydl.download([url])  # Usa `url` en lugar de `youtube_url`
                            st.success(f"¡{formato} descargado con éxito en la carpeta {output_path}!")
                except Exception as e:
                    st.error(f"Error al descargar: {e}")



# boton para abrir la carpeta de descarga en la barra lateral
if st.sidebar.button('Abrir carpeta'):
    os.startfile(output_path)



# Icono de Linktree centrado

# Insertar un espacio vacío en la barra lateral para "empujar" el icono hacia abajo
for _ in range(5):  # Ajusta el número de líneas vacías para más o menos espacio
    st.sidebar.write("")

st.sidebar.markdown(
    """
    <div style="text-align: center;">
        <a href="https://linktr.ee/rayko_benitez" target="_blank">
            <img src="https://ugc.production.linktr.ee/097834f8-e2d7-4fe7-9d38-489fc794f840_DAGNQ4WeEPc.png?io=true&size=avatar-v3_0" width="50">
        </a>
    </div>
    """,
    unsafe_allow_html=True
)
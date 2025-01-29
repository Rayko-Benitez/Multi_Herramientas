import streamlit as st
import os
import speech_recognition as sr
from pydub import AudioSegment
from pydub.utils import make_chunks
from tqdm import tqdm
import shutil



#---------------visual de la pagina y complementos-----------
# Logo
st.sidebar.image("static/logo av sunglass.png", width=100)


# Título y descripción
st.sidebar.title("Aplicación de transcripción de audios")


# Instrucciones de uso
st.sidebar.header("Instrucciones")
st.sidebar.write("""
1. Paso 1: Pega la URL de tus archivos a la barra de carga.
2. Paso 2: Presiona el botón Iniciar transcripción, espera a que termine.
3. Paso 3: Si quieres iniciar otra carpeta, repite los pasos.
""")


st.sidebar.error('Solo funciona con formatos de archivos .wav')


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



# -------------Configuración de la interfaz de usuario------------
st.title("Aplicación de Transcripción de Audios WAV")
st.subheader("De momento no funciona online, solo en local por las carpetas")

# Input para la carpeta de archivos
input_folder = st.text_input("Ingresa la ruta de la carpeta que contiene los archivos .wav")

if input_folder:
    if not os.path.exists(input_folder):
        st.error("La carpeta ingresada no existe. Por favor verifica la ruta.")
    else:
        st.success("Carpeta encontrada. Iniciando el proceso de transcripción.")

# Botón para iniciar la transcripción
if st.button("Iniciar transcripción"):
    if not input_folder:
        st.error("Por favor, ingresa la ruta de la carpeta.")
    else:
        # Crear una carpeta temporal para dividir audios si es necesario
        temp_folder = os.path.join(input_folder, "temp")
        os.makedirs(temp_folder, exist_ok=True)

        success_files = []
        error_files = {}

        # Procesar cada archivo en la carpeta
        audio_files = [f for f in os.listdir(input_folder) if f.endswith(".wav")]
        progress_bar = st.progress(0)

        for i, audio_file in enumerate(audio_files):
            try:
                st.write(f"Procesando: {audio_file}")

                # Ruta completa del archivo
                audio_path = os.path.join(input_folder, audio_file)

                # Dividir el audio en fragmentos si es necesario
                audio = AudioSegment.from_wav(audio_path)
                if len(audio) > 60000:  # Fragmentar si dura más de 60 segundos
                    chunks = make_chunks(audio, 60000)
                    temp_text = ""

                    for j, chunk in enumerate(chunks):
                        chunk_path = os.path.join(temp_folder, f"chunk_{j}.wav")
                        chunk.export(chunk_path, format="wav")

                        # Transcribir el fragmento
                        recognizer = sr.Recognizer()
                        with sr.AudioFile(chunk_path) as source:
                            audio_data = recognizer.record(source)
                            temp_text += recognizer.recognize_google(audio_data, language="es-ES") + " "

                        os.remove(chunk_path)
                else:
                    # Transcribir directamente si no requiere fragmentación
                    recognizer = sr.Recognizer()
                    with sr.AudioFile(audio_path) as source:
                        audio_data = recognizer.record(source)
                        temp_text = recognizer.recognize_google(audio_data, language="es-ES")

                # Guardar la transcripción en un archivo de texto
                output_path = os.path.join(input_folder, f"{os.path.splitext(audio_file)[0]}.txt")
                with open(output_path, "w", encoding="utf-8") as txt_file:
                    txt_file.write(temp_text)

                success_files.append(audio_file)

            except Exception as e:
                st.error(f"Error procesando {audio_file}: {str(e)}")
                error_files[audio_file] = str(e)

            # Actualizar barra de progreso
            progress_bar.progress((i + 1) / len(audio_files))

        # Limpiar carpeta temporal
        shutil.rmtree(temp_folder)

        # Mostrar resultados
        st.success("Proceso completado.")
        st.write("Archivos transcritos correctamente:")
        st.write(success_files)

        if error_files:
            st.write("Archivos con errores:")
            for file, error in error_files.items():
                st.write(f"{file}: {error}")

        st.write("Todos los archivos temporales han sido eliminados. Puedes iniciar un nuevo proceso si lo deseas.")

import streamlit as st
st.__version__ = "1.38.0"  # Define manualmente la versión de Streamlit
import speech_recognition as sr
import moviepy.editor as mp
import pyperclip
import os
from pydub import AudioSegment
from pydub.utils import make_chunks
import signal


#visual de la pagina y complementos
# Logo
st.sidebar.image("static/logo av sunglass.png", width=100)


# Título y descripción
st.sidebar.title("Aplicación de transcripción de audios")


# Instrucciones de uso
st.sidebar.header("Instrucciones")
st.sidebar.write("""
1. Paso 1: Carga tu archivo a la barra de carga en formato .wav.
2. Paso 2: Se inicia automaticamente, solo espera a que termine.
3. Paso 3: No lo edites en el recuadro, usa el boton para copiarlo al portapales y pégalo en otro lugar.
4. Paso 4: Sigue las instrucciones de los botones principales en el orden que aparecen.
""")


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



# Función para convertir .m4a a .wav
def convert_m4a_to_wav(m4a_path):
    audio_clip = mp.AudioFileClip(m4a_path)
    wav_path = "converted_audio.wav"
    audio_clip.write_audiofile(wav_path)
    return wav_path

# Función para dividir el audio en segmentos más pequeños (menos de 60 segundos)
def split_audio(file_path, chunk_length_ms=60000):
    # Cargamos el archivo de audio usando Pydub
    audio = AudioSegment.from_wav(file_path)
    
    # Dividimos el audio en chunks (pedazos de audio de chunk_length_ms milisegundos)
    chunks = make_chunks(audio, chunk_length_ms)
    
    chunk_filenames = []
    
    for i, chunk in enumerate(chunks):
        chunk_name = f"chunk{i}.wav"
        chunk.export(chunk_name, format="wav")
        chunk_filenames.append(chunk_name)
    
    return chunk_filenames

# Función para transcribir un solo segmento de audio
def transcribe_audio(file_path):
    recognizer = sr.Recognizer()
    
    with sr.AudioFile(file_path) as source:
        audio = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio, language="es-ES")
            return text
        except sr.UnknownValueError:
            return "No se pudo entender el audio."
        except sr.RequestError as e:
            return f"Error en la solicitud al servicio de reconocimiento de voz: {e}"

# Función para transcribir audios largos divididos en segmentos
def transcribe_long_audio(file_path):
    try:
        # Dividimos el archivo de audio en segmentos de 60 segundos
        chunks = split_audio(file_path)
        full_text = ""
        
        for chunk in chunks:
            text = transcribe_audio(chunk)
            full_text += text + " "
            # Eliminamos el archivo chunk después de transcribirlo
            os.remove(chunk)
        
        return full_text
    except Exception as e:
        return f"Error transcribiendo el archivo largo: {e}"

# Función para extraer audio de video y transcribirlo
def transcribe_video(file_path):
    try:
        clip = mp.VideoFileClip(file_path)
        audio_path = "extracted_audio.wav"
        clip.audio.write_audiofile(audio_path)
        
        # Transcribimos el audio extraído
        text = transcribe_long_audio(audio_path)
        
        # Eliminamos el archivo de audio temporal
        os.remove(audio_path)
        
        return text
    except Exception as e:
        return f"Error procesando el archivo de video: {e}"

# Función para manejar la carga del archivo
def handle_file_upload(uploaded_file):
    try:
        if uploaded_file.type.startswith("audio"):
            file_extension = uploaded_file.name.split('.')[-1].lower()

            if file_extension == "m4a":
                with open("temp_audio.m4a", "wb") as f:
                    f.write(uploaded_file.getbuffer())
                wav_path = convert_m4a_to_wav("temp_audio.m4a")
                text = transcribe_long_audio(wav_path)
                os.remove("temp_audio.m4a")
                os.remove(wav_path)
                return text

            else:
                with open("temp_audio.wav", "wb") as f:
                    f.write(uploaded_file.getbuffer())
                return transcribe_long_audio("temp_audio.wav")

        elif uploaded_file.type.startswith("video"):
            with open("temp_video.mp4", "wb") as f:
                f.write(uploaded_file.getbuffer())
            return transcribe_video("temp_video.mp4")

        else:
            return "Por favor, sube un archivo de audio."

    except Exception as e:
        return f"Error al procesar el archivo: {e}"

# Interfaz de usuario con Streamlit
st.title("Transcripción de Voz a Texto")
st.write("Sube un archivo de audio para transcribirlo a texto.")

# Botón para cargar el archivo de audio
uploaded_file = st.file_uploader("Carga tu archivo de audio", type=["wav"])

# Procesar la transcripción solo si se sube un archivo
if uploaded_file is not None:
    if "transcribed_text" not in st.session_state:
        with st.spinner("Transcribiendo el archivo..."):
            st.session_state.transcribed_text = handle_file_upload(uploaded_file)
    
    # Mostramos la transcripción, ya sea el texto correcto o un error
    st.text_area("Texto transcrito", value=st.session_state.transcribed_text, height=300)

    # Botón para copiar al portapapeles
    if st.button("Copiar texto al portapapeles"):
        pyperclip.copy(st.session_state.transcribed_text)
        st.success("Texto copiado al portapapeles.")


# De aqui para abajo es una nueva funcionalidad del boton reset

# Crear un botón de reinicio funcional usando Streamlit
st.write('Antes de cargar un nuevo archivo de audio, elimina en la x el archivo actual y presiona este botón')
if st.button("Reiniciar para nuevo archivo"):
    # Reiniciar el estado de la transcripción para poder subir un nuevo archivo
    if "transcribed_text" in st.session_state:
        del st.session_state.transcribed_text
    # También podemos reiniciar otras variables de sesión si es necesario
    st.session_state.uploaded_file = None  # Reiniciar el archivo cargado
    #st.query_params()  # Resetea los parámetros de la URL, limpiando el estado (pero no funciona ni afecta)

#Cierra los procesos de streamlit y otros para cerrar la pestaña
st.write('Da clic en este botón antes de cerrar la pestaña para cerrar los procesos')

if st.button("Borrar temporales"):
    if os.path.exists("temp_audio.wav"):
        os.remove("temp_audio.wav")
    #os.kill(pid, signal.SIGTERM) descomentar para si se usa con .exe
import streamlit as st
from hashlib import sha256


# Función para cifrar contraseñas
def hash_password(password):
    return sha256(password.encode()).hexdigest()

# Base de datos de usuarios y contraseñas cifradas (se manejarán manualmente)
USER_DB = {
    "user1@example.com": hash_password("password123"),
    "user2@example.com": hash_password("securepass456"),
}

# Función para autenticar usuario
def authenticate(username, password):
    hashed_pw = hash_password(password)
    return USER_DB.get(username) == hashed_pw

# Configuración de Streamlit
st.set_page_config(page_title="Inicio de sesión", page_icon="🔒", layout="wide")


# Página de inicio
def mostrar_inicio():
    st.title("Web de herramientas multipropósitos")
    st.subheader("¿Quién soy?")
    st.write("Soy ingeniero, especializado en energías renovables, incursionando en el mundo del análisis de datos y la programación.")
    #---------------visual de la pagina y complementos-----------
    # Logo
    st.sidebar.image("static/logo av sunglass.png", width=100)

    # Título y descripción
    st.sidebar.title("Aplicaciones")

    # Instrucciones de uso
    st.sidebar.header("Instrucciones")
    st.sidebar.write("""
    Arriba tienes una serie de páginas que te llevará a distintas herramientas disponibles.
    
    Solo da clic en la que quieras usar y te llevará a esa herramienta.
    """)

    st.sidebar.success('Si tienes alguna recomendación o idea para adarme, estaré agradecido de leerte.')

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






# Estado global para manejo de sesión
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# CSS global para ocultar la barra lateral por defecto
hide_sidebar_css = """
    <style>
    [data-testid="stSidebar"] {
        display: none;
    }
    </style>
"""

show_sidebar_css = """
    <style>
    [data-testid="stSidebar"] {
        display: block;
    }
    </style>
"""

# Aplica CSS según el estado de autenticación
if not st.session_state["authenticated"]:
    st.markdown(hide_sidebar_css, unsafe_allow_html=True)
else:
    st.markdown(show_sidebar_css, unsafe_allow_html=True)





if st.session_state["authenticated"]:
    # Carga la aplicación principal
    mostrar_inicio()
else:
    # Interfaz de inicio de sesión
    st.title("Inicio de sesión seguro")
    st.markdown("Por favor, introduce tu nombre de usuario (email) y contraseña para continuar.")

    # Inputs de usuario y contraseña
    username = st.text_input("Nombre de usuario (email):", placeholder="correo@example.com")
    password = st.text_input("Contraseña:", type="password", placeholder="Introduce tu contraseña")

    # Botón de inicio de sesión
    if st.button("Iniciar sesión"):
        if username and password:
            if authenticate(username, password):
                st.session_state["authenticated"] = True
                st.success("Inicio de sesión exitoso. Bienvenido, {}!".format(username))
                st.rerun()  # Recarga para mostrar la aplicación principal
            else:
                st.error("Nombre de usuario o contraseña incorrectos. Por favor, intenta nuevamente.")
        else:
            st.warning("Por favor, completa todos los campos antes de continuar.")




    


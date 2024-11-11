import streamlit as st
from groq import Groq

modelos = ["llama3-8b-8192", "llama3-70b-8192", "mixtral-8x7b-32768"]

def crear_usuario():
    """Crea el cliente de usuario utilizando la clave API almacenada en secretos."""
    clave_secreta = st.secrets["CLAVE_API"]
    return Groq(api_key=clave_secreta)

def configurar_modelo(cliente, modelo, mensaje_de_entrada):
    """Configura y envía una solicitud al modelo seleccionado."""
    respuesta = cliente.chat.completions.create(
        model=modelo,
        messages=[{"role": "user", "content": mensaje_de_entrada}],
        stream=False
    )
    return respuesta.choices[0].message.content

def configurar_pagina():
    """Configura la página principal y el modelo seleccionado en el sidebar."""
    st.set_page_config(page_title="Mi chat IA", page_icon="🤖")
    st.title("Mi Chat IA")
    st.sidebar.title("Panel de Modelos")
    modelo_seleccionado = st.sidebar.selectbox("Modelos", modelos)
    return modelo_seleccionado

def inicializar_estado():
    """Inicializa el estado de los mensajes de chat en la sesión."""
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []

def actualizar_historial(rol, contenido, avatar):
    """Actualiza el historial de chat almacenado en el estado de la sesión."""
    st.session_state.mensajes.append({"role": rol, "content": contenido, "avatar": avatar})

def mostrar_historial():
    """Muestra el historial de chat en la interfaz de usuario."""
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"], avatar=mensaje["avatar"]):
            st.markdown(mensaje["content"])

def main():
    """Función principal que organiza el flujo de la aplicación."""
    inicializar_estado()
    modelo_en_uso = configurar_pagina()
    cliente_usuario = crear_usuario()
    area_chat()

    mensaje = st.chat_input("Escribe tu mensaje aquí...")

    if mensaje:
        actualizar_historial("user", mensaje, "😊")
        try:
            respuesta = configurar_modelo(cliente_usuario, modelo_en_uso, mensaje)
            actualizar_historial("assistant", respuesta, "🤖")
        except Exception as e:
            st.error(f"Error al procesar el mensaje: {e}")
        st.rerun()

def area_chat():
    """Configura y muestra el área del chat."""
    with st.container():
        mostrar_historial()

if __name__ == "__main__":
    main()

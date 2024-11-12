import streamlit as st
from groq import Groq

st.set_page_config(page_title="Mi chat de IA", page_icon="🌎"); #Le damos un itulo a unestra página

#Titulo
st.title("Mi primera aplicación con Streamlit");

#Ingreso de datos
nombre = st.text_input("¿Cuál es tu nombre? ");

MODELO = ['llama3-8b-8192', 'llama3-70b-8192', 'mixtral-8x7b-32768']

#Crear un botón con funcionalidad
if st.button("Saludar"):
    st.write(f"Hola, {nombre}");


def crear_usuario_groq():
    clave_secreta = st.secrets["CLAVE_API"]
    return Groq(api_key = clave_secreta) #*Crea el usuario

def configurar_modelo(cliente, modelo, mensaje):
    return cliente.chat.completions.create(
        model = modelo,
        messages = [{"role":"user", "content": mensaje}],
        stream = False,
    )


def inicializar_estado():
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []

def actualizar_historial(rol, contenido, avatar):
    st.session_state.mensajes.append(
        {"role": rol, "content": contenido, "avatar": avatar}
    )

def mostrar_historial():
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"], avatar=mensaje["avatar"]):
            st.markdown(mensaje["content"])

#Contenedor del chat
def area_chat():
    contenedorDelChat = st.container(height="400", border=True)
    with contenedorDelChat: mostrar_historial()

#? CREANDO FUNCIÓN -> DISEÑO DE PÁGINA
def configurar_pagina():
    st.title("Mi chat de IA");
    st.sidebar.title("Configuración");
    seleccion =st.sidebar.selectbox(
        "Elegí un modelo",
        MODELO,
        index= 2 #datoDefecto,
    )
    return seleccion

def generar_respuesta(chat_completo):
    respuesta_completa = ""
    for frase in chat_completo:
        if frase.choises[0].delta.content:
            respuesta_completa += frase.choises[0].delta.content
            print(respuesta_completa)

#Invocar funciones
modelo = configurar_pagina()
st.write(f"El usuario eligió el modelo {modelo}")
clienteusuario = crear_usuario_groq()
inicializar_estado()
area_chat() #Creamos el sector de los mensajes
mensaje = st.chat_input("Escribí tu mensaje: ")
st.write(f"Usuario: {mensaje}")
if mensaje:
    actualizar_historial("user", mensaje, "👨‍💻")
    chat_completo = configurar_modelo(clienteusuario, modelo, mensaje)
    actualizar_historial("assistant", chat_completo, "🤖")
    st.rerun()
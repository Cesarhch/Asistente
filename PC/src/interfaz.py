import platform
from tkinter import *
from contexto import Contexto

def mostrar_ventana(callback_obtener_texto):
    sistema_operativo = platform.system()
    Contexto.ventana = Tk()
    ventana = Contexto.ventana

    # Obtener dimensiones de la pantalla
    ancho_pantalla = ventana.winfo_screenwidth()
    alto_pantalla = ventana.winfo_screenheight()

    # Definir márgenes (5% del ancho, 8% del alto)
    margen_horizontal = int(ancho_pantalla * 0.05)
    margen_vertical = int(alto_pantalla * 0.08)

    # Calcular tamaño de la ventana con márgenes
    ancho_ventana = ancho_pantalla - 2 * margen_horizontal
    alto_ventana = alto_pantalla - 2 * margen_vertical

    # Configurar tamaño y posición centrada
    ventana.geometry(f"{ancho_ventana}x{alto_ventana}+{margen_horizontal}+{margen_vertical}")
    ventana.title("Interacción con el Asistente")

    # Marco para el área de conversación con scroll
    frame_texto = Frame(ventana)
    frame_texto.pack(pady=20, padx=20, expand=True, fill=BOTH)

    # Scrollbar vertical
    scrollbar = Scrollbar(frame_texto)
    scrollbar.pack(side=RIGHT, fill=Y)

    # Área de texto con scroll
    Contexto.texto_conversacion = Text(
        frame_texto, height=25, width=80, wrap=WORD, font=("Arial", 14), yscrollcommand=scrollbar.set
    )
    Contexto.texto_conversacion.pack(expand=True, fill=BOTH)
    scrollbar.config(command=Contexto.texto_conversacion.yview)  # Conectar el scroll con el área de texto

    # Marco para los controles de entrada
    frame_entrada = Frame(ventana)
    frame_entrada.pack(pady=10, fill=X, padx=20)

    # Campo de entrada de texto
    entrada = Entry(frame_entrada, font=("Arial", 16), width=70)
    entrada.pack(side=LEFT, expand=True, fill=X, padx=10)

    def procesar_y_limpiar(event=None):
        callback_obtener_texto(entrada, ventana)
        entrada.delete(0, END)

    entrada.bind('<Return>', procesar_y_limpiar)

    # Botón para enviar el texto
    boton = Button(frame_entrada, text="Enviar", font=("Arial", 14), command=lambda: (callback_obtener_texto(entrada, ventana), entrada.delete(0, END)))
    boton.pack(side=RIGHT, padx=10)

    # Botón para cerrar la ventana
    #boton_cerrar = Button(ventana, text="Cerrar", font=("Arial", 14), command=ventana.destroy)
    #boton_cerrar.pack(pady=10)

    return ventana

def actualizar_conversacion(texto_usuario, texto_asistente):
    if Contexto.ventana and Contexto.texto_conversacion:
        Contexto.texto_conversacion.insert(END, f"Usuario: {texto_usuario}\n", "usuario")
        Contexto.texto_conversacion.insert(END, f"Asistente: {texto_asistente}\n\n", "asistente")
        Contexto.texto_conversacion.see(END)  # Auto-scroll al final

def cerrar_todo():
    # Cierra la ventana y realiza cualquier limpieza necesaria.
    if Contexto.ventana is not None:
        try:
            Contexto.ventana.quit()  # Detiene el ciclo de eventos
            Contexto.ventana.destroy()  # Cierra la ventana
            Contexto.ventana = None  # Limpia la referencia
            print("Ventana cerrada correctamente desde interfaz.")
        except Exception as e:
            print(f"Error al cerrar la ventana: {e}")
    else:
        print("No hay ventana activa para cerrar.")

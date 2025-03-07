import platform
from tkinter import *
from contexto import Contexto

def mostrar_ventana(callback_obtener_texto):
    # Detectar el sistema operativo
    sistema_operativo = platform.system()

    # Muestra una ventana con una entrada de texto y un botón.
    Contexto.ventana = Tk()
    ventana = Contexto.ventana

    # Configuraciones específicas según el sistema operativo
    if sistema_operativo == "Darwin":  # macOS
        ventana.geometry("+%d+%d" % (ventana.winfo_screenwidth() - 300, 0))
        ventana.title("Lara - macOS")
    elif sistema_operativo == "Windows":
        ventana.geometry("300x150+%d+%d" % (ventana.winfo_screenwidth() - 300, 0))  # Derecha, arriba
        ventana.title("Lara - Windows")
    else:  # Linux o cualquier otro sistema
        ventana.geometry("+%d+%d" % (ventana.winfo_screenwidth() - 300, 0))  # Derecha, arriba
        ventana.title("Lara - Otro SO")

    # Crear un widget de entrada de texto
    entrada = Entry(ventana)
    entrada.pack(pady=10)

    def procesar_y_limpiar(event=None):
        callback_obtener_texto(entrada, ventana)
        entrada.delete(0, END)  # Limpia el campo de entrada

    entrada.bind('<Return>', procesar_y_limpiar)

    # Crear un botón para obtener el texto
    boton = Button(ventana, text="Obtener texto", command=lambda: (callback_obtener_texto(entrada, ventana), entrada.delete(0, END)))
    boton.pack(pady=5)

    return ventana

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

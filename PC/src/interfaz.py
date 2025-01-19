from tkinter import *
from contexto import Contexto

def mostrar_ventana(callback_obtener_texto):
    #Muestra una ventana con una entrada de texto y un botón.
    Contexto.ventana = Tk()
    ventana = Contexto.ventana
    ventana.geometry("+%d+%d" % (ventana.winfo_screenwidth() - 300, 0))
    ventana.title("Asistente")

    # Crear un widget de entrada de texto
    entrada = Entry(ventana)
    entrada.pack()
    #entrada.bind('<Return>', lambda event: callback_obtener_texto(entrada, ventana))
    # Limpiar el campo de entrada después de procesar el texto
    def procesar_y_limpiar(event=None):
        callback_obtener_texto(entrada, ventana)
        entrada.delete(0, END)  # Limpia el campo de entrada

    entrada.bind('<Return>', procesar_y_limpiar)
    # Crear un botón para obtener el texto
    boton = Button(ventana, text="Obtener texto", command=lambda: callback_obtener_texto(entrada, ventana))
    boton.pack()

    return ventana

def cerrar_todo():
    #Cierra la ventana y realiza cualquier limpieza necesaria.
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
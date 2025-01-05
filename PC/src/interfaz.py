from tkinter import *

def mostrar_ventana(callback_obtener_texto):
    """Muestra una ventana con una entrada de texto y un botón."""
    ventana = Tk()
    ventana.geometry("+%d+%d" % (ventana.winfo_screenwidth() - 300, 0))
    ventana.title("Lara")

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
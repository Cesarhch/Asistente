import datetime

# Ruta del archivo a actualizar
ruta_archivo = "C:/ruta/rag/managment.txt"

# Obtener la fecha actual en el formato deseado
fecha_actual = datetime.datetime.now().strftime("Hoy es el día %A %d de %B del %Y")

# Escribir la fecha en el archivo (sobrescribiendo el contenido anterior)
with open(ruta_archivo, "w", encoding="utf-8") as archivo:
    archivo.write(fecha_actual + "\n")

#print("✅ Archivo 'managment.txt' actualizado con la fecha actual.")

import serial
from agentmanager import responder_agente_managment
from voz import play_audio, stop_audio_thread
from modelos import configurar_modelo_remoto
from terminartodo import finalizar_todo

def obtener_texto(entrada, ventana=None):
  # Si entrada es un widget de Tkinter
  if hasattr(entrada, "get"):
    texto_introducido_ventana = entrada.get()
  else:
    # Si entrada es un string directo
    texto_introducido_ventana = entrada
  if texto_introducido_ventana.strip():  
    texto_introducido = texto_introducido_ventana.strip().lower()
    
    # Detener cualquier audio en reproducción
    stop_audio_thread()
    
  if texto_introducido_ventana.lower() == "terminar todo":
    play_audio("ok, cierro sesión")
    finalizar_todo()
    return
  if texto_introducido_ventana.lower() == "terminar ventana":
    play_audio("adios, debes cerrar la ventana en manual")
    return
  if texto_introducido_ventana.lower().startswith("escribir datos "):
    phrase_to_remember = texto_introducido_ventana[len("escribir datos "):].strip()
    #save_cesar(phrase_to_remember)
    play_audio("Información guardada, " + phrase_to_remember)
    return
  if texto_introducido_ventana.lower() == "enciende la luz del comedor":
    play_audio("enciendo el comedor")
    ser = serial.Serial('/dev/tty.usbserial-0001', 9600)
    dato="c1"
    ser.write(dato.encode('utf-8'))
    ser.close()  
    return
  if texto_introducido_ventana.lower() == "apaga la luz del comedor":
    play_audio("apago el comedor")
    ser = serial.Serial('/dev/tty.usbserial-0001', 9600)
    dato="c0"
    ser.write(dato.encode('utf-8'))
    ser.close()
    return
  
  else:
    
    try:
      resultado = configurar_modelo_remoto.chain_remote.run(question=texto_introducido)
      print("\nRespuesta del modelo remoto:\n")
      print(resultado)   
    except Exception as e:
      print(f"Error con el modelo remoto: {e}")
      
      try:
        resultado = responder_agente_managment(texto_introducido)
        if hasattr(resultado, "content") and resultado.content:
          texto_a_reproducir = resultado.content.strip()
        else:
          texto_a_reproducir = resultado
      except Exception as e:
        print(f"Error al usar el modelo local: {e}")
        texto_a_reproducir = "Hubo un error al procesar la solicitud."
        
    if not texto_a_reproducir.strip():
      texto_a_reproducir = "La respuesta está vacía."

    # Reproducir el texto final
    print(f"Respuesta: {texto_a_reproducir}")
    respuesta= texto_a_reproducir

    if respuesta.lower() == " encender comedor":
      play_audio(respuesta)
      ser = serial.Serial('/dev/tty.usbserial-0001', 9600)
      dato="c1"
      ser.write(dato.encode('utf-8'))
      ser.close()
      return
    if respuesta.lower() == " apagar comedor":
      play_audio(respuesta)
      ser = serial.Serial('/dev/tty.usbserial-0001', 9600)
      dato="c0"
      ser.write(dato.encode('utf-8'))
      ser.close()
      return
    if respuesta.lower() == " encender cocina":
      play_audio(respuesta)
      ser = serial.Serial('/dev/tty.usbserial-0001', 9600)
      dato="ci1"
      ser.write(dato.encode())
      ser.close()
    if respuesta.lower() == " apagar cocina":
      play_audio(respuesta)
      ser = serial.Serial('/dev/tty.usbserial-0001', 9600)
      dato="ci0"
      ser.write(dato.encode())
      ser.close()
    if respuesta.lower() == " encender electrovalvula":
      play_audio(respuesta)
      ser = serial.Serial('/dev/tty.usbserial-0001', 9600)
      dato="v1"
      ser.write(dato.encode())
      ser.close()
    if respuesta.lower() == " apagar electrovalvula":
      play_audio(respuesta)
      ser = serial.Serial('/dev/tty.usbserial-0001', 9600)
      dato="v0"
      ser.write(dato.encode())
      ser.close()
    play_audio(respuesta)
    return
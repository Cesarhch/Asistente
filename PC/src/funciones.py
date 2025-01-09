def save_cesar(information):
  with open("/Users/cesarhernandez/Documents/PlatformIO/Projects/RAG-1/prueba2/datoscasa2.txt", "a", newline="") as file:  # Open in append mode
    file.write(information + "\n")
    file.close()
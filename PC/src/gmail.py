from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import pickle

# Permisos requeridos (solo lectura de correos)
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

def gmail_leer():
    """Lee los correos nuevos en Gmail y devuelve la información."""
    
    creds = None
    token_path = "token.pickle"
    
    # Cargar credenciales almacenadas previamente
    if os.path.exists(token_path):
        with open(token_path, "rb") as token:
            creds = pickle.load(token)

    # Si no hay credenciales válidas, solicitar autenticación
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)

        # Guardar credenciales para futuras ejecuciones
        with open(token_path, "wb") as token:
            pickle.dump(creds, token)

    # Conectar con la API de Gmail
    service = build("gmail", "v1", credentials=creds)

    # Obtener los correos no leídos
    results = service.users().messages().list(userId="me", labelIds=["UNREAD"], maxResults=5).execute()
    mensajes = results.get("messages", [])

    if not mensajes:
        return "No tienes correos nuevos."

    correos_nuevos = []
    
    for mensaje in mensajes:
        msg = service.users().messages().get(userId="me", id=mensaje["id"]).execute()
        headers = msg["payload"]["headers"]
        asunto = next((h["value"] for h in headers if h["name"] == "Subject"), "Sin asunto")
        remitente = next((h["value"] for h in headers if h["name"] == "From"), "Desconocido")
        snippet = msg.get("snippet", "")

        correos_nuevos.append(f"De: {remitente}\nAsunto: {asunto}\nMensaje: {snippet}\n")

    return "\n\n".join(correos_nuevos)

# Ejecutar la función y mostrar correos
if __name__ == "__main__":
    print(gmail())

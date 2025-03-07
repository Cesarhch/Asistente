import datetime
import os.path
import pickle
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# Ruta del archivo de token generado previamente
TOKEN_FILE = "token.pickle"

# Permisos necesarios para acceder a Google Calendar y Google Tasks
SCOPES = [
    "https://www.googleapis.com/auth/calendar.readonly",
    "https://www.googleapis.com/auth/tasks.readonly"
]

def obtener_credenciales():
    """Carga las credenciales desde `token.pickle` sin regenerarlas."""
    creds = None

    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            return "Error: El archivo token.pickle no es válido."

    return creds

def obtener_eventos():
    """Obtiene los próximos eventos de Google Calendar."""
    try:
        creds = obtener_credenciales()
        if isinstance(creds, str):  
            return creds

        service = build("calendar", "v3", credentials=creds)

        now = datetime.datetime.utcnow().isoformat() + "Z"

        eventos_result = service.events().list(
            calendarId="primary",
            timeMin=now,
            maxResults=5,
            singleEvents=True,
            orderBy="startTime"
        ).execute()

        eventos = eventos_result.get("items", [])
        respuesta = ""

        if not eventos:
            respuesta += "No hay eventos próximos en tu calendario.\n"
        else:
            respuesta += "Tus próximos eventos son:\n"
            for evento in eventos:
                inicio = evento["start"].get("dateTime", evento["start"].get("date"))
                respuesta += f"- {evento['summary']} el {inicio}\n"

        return respuesta

    except Exception as e:
        return f"Error al obtener eventos: {e}"

def obtener_tareas():
    """Obtiene las tareas pendientes de Google Tasks."""
    try:
        creds = obtener_credenciales()
        if isinstance(creds, str):  
            return creds

        service = build("tasks", "v1", credentials=creds)

        # Obtener la lista de tareas principal
        task_lists = service.tasklists().list().execute().get("items", [])
        if not task_lists:
            return "No hay listas de tareas disponibles."

        tareas = []
        for task_list in task_lists:
            tareas_result = service.tasks().list(tasklist=task_list["id"]).execute()
            tareas.extend(tareas_result.get("items", []))

        if not tareas:
            return "No hay tareas pendientes."

        respuesta = "\nTus próximas tareas son:\n"
        for tarea in tareas:
            fecha_vencimiento = tarea.get("due", "Sin fecha")
            respuesta += f"- {tarea['title']} (Fecha: {fecha_vencimiento})\n"

        return respuesta

    except Exception as e:
        return f"Error al obtener tareas: {e}"

if __name__ == "__main__":
    eventos = obtener_eventos()
    tareas = obtener_tareas()
    print(eventos)
    print(tareas)

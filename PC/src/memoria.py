import sqlite3

class BaseDatos:
    def __init__(self, db_path="memoria.db"):
        self.conexion = sqlite3.connect(db_path)
        self.cursor = self.conexion.cursor()
        self._crear_tabla()

    def _crear_tabla(self):
        """Crear la tabla de la base de datos si no existe."""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS textos_reconocidos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                origen TEXT NOT NULL,  -- 'usuario' o 'asistente'
                texto TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.conexion.commit()

    def guardar_texto(self, origen, texto):
        """Guardar un texto en la base de datos."""
        self.cursor.execute(
            "INSERT INTO textos_reconocidos (origen, texto) VALUES (?, ?)", (origen, texto)
        )
        self.conexion.commit()
        print(f"Texto guardado en la base de datos ({origen}): {texto}")

    def obtener_textos(self, limite=5):
        """Obtener los últimos textos almacenados."""
        self.cursor.execute("SELECT origen, texto, timestamp FROM textos_reconocidos ORDER BY timestamp DESC LIMIT ?", (limite,))
        return self.cursor.fetchall()

    def cerrar(self):
        """Cerrar la conexión con la base de datos."""
        self.conexion.close()

class MemoriaConversacion:
    def __init__(self, max_memoria=5):
        self.max_memoria = max_memoria
        self.memoria_conversacion = []  # Guarda las últimas interacciones

    def actualizar_memoria(self, usuario, asistente):
        if len(self.memoria_conversacion) >= self.max_memoria:
            self.memoria_conversacion.pop(0)  # Elimina la iteración más antigua
        self.memoria_conversacion.append({"usuario": usuario, "asistente": asistente})

    def obtener_memoria(self):
        return self.memoria_conversacion

# Instancia global para ser utilizada en todo el proyecto
memoria_global = MemoriaConversacion()

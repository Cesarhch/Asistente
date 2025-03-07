from newsapi import NewsApiClient
from deep_translator import GoogleTranslator
import sys

# 🔑 API Key de NewsAPI
API_KEY = "kjgfkdsjgkdfhsgkjdfshgkjsdfhgkjsdfk"

def obtener_noticias():
    # Extrae el tema de búsqueda
    if len(sys.argv) > 1:
        tema = " ".join(sys.argv[1:])
    else:
        tema = "tecnología"  # Tema por defecto

    print(f"Buscando noticias sobre: {tema}")

    # Inicializar cliente de NewsAPI
    newsapi = NewsApiClient(api_key=API_KEY)

    try:
        # Obtener noticias sin restricción de idioma
        top_headlines = newsapi.get_everything(q=tema, sort_by="publishedAt", page_size=5)

        if not top_headlines["articles"]:
            return "No se encontraron noticias sobre este tema."

        noticias = []
        for i, article in enumerate(top_headlines["articles"]):
            titulo_original = article['title']
            url = article['url']
            
            # Traducir título al español
            try:
                titulo_traducido = GoogleTranslator(source="auto", target="es").translate(titulo_original)
            except Exception:
                titulo_traducido = titulo_original  # Si hay error, usa el original
            
            noticias.append(f"{i+1}. {titulo_traducido} - {url}")

        return "\n".join(noticias)

    except Exception as e:
        print(f"Error: {e}")
        return f"Error al obtener noticias: {e}"

if __name__ == "__main__":
    print(obtener_noticias())

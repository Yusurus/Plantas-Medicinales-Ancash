import requests


def get_wikipedia_plant_image(scientific_name):
    WIKIPEDIA_API_URL = "https://es.wikipedia.org/w/api.php"

    params = {
        "action": "query",
        "format": "json",
        "prop": "pageimages",
        "pithumbsize": 600,
        "redirects": 1,
        "titles": scientific_name,
    }

    image_url = None

    try:
        response = requests.get(WIKIPEDIA_API_URL, params=params)
        response.raise_for_status()
        data = response.json()

        pages = data.get("query", {}).get("pages", {})

        for page_id, page_data in pages.items():
            if page_data.get("thumbnail") and page_data["thumbnail"].get("source"):
                image_url = page_data["thumbnail"]["source"]
                break

        return image_url

    except requests.exceptions.RequestException as e:
        print(f"Error al comunicarse con la API de Wikipedia: {e}")
        return None
    except Exception as e:
        print(f"Error inesperado al procesar la respuesta de Wikipedia: {e}")
        return None

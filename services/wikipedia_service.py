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
def get_wikipedia_plant_images(scientific_name, max_images=5):
    import requests

    WIKIPEDIA_API_URL = "https://es.wikipedia.org/w/api.php"

    try:
        # Paso 1: Obtener el título real y la lista de imágenes del artículo
        params_images = {
            "action": "query",
            "format": "json",
            "prop": "images",
            "titles": scientific_name,
            "imlimit": max_images,
            "redirects": 1,
        }

        response = requests.get(WIKIPEDIA_API_URL, params=params_images)
        response.raise_for_status()
        data = response.json()

        pages = data.get("query", {}).get("pages", {})
        image_titles = []

        for page_data in pages.values():
            if "images" in page_data:
                for img in page_data["images"]:
                    title = img["title"]
                    if title.lower().endswith(('.jpg', '.jpeg', '.png')):
                        image_titles.append(title)

        # Paso 2: Obtener las URL de las imágenes
        image_urls = []
        for title in image_titles[:max_images]:
            params_info = {
                "action": "query",
                "format": "json",
                "prop": "imageinfo",
                "titles": title,
                "iiprop": "url",
            }
            img_response = requests.get(WIKIPEDIA_API_URL, params=params_info)
            img_response.raise_for_status()
            img_data = img_response.json()
            for page in img_data["query"]["pages"].values():
                if "imageinfo" in page:
                    image_urls.append(page["imageinfo"][0]["url"])

        return image_urls

    except Exception as e:
        print(f"Error al obtener imágenes de Wikipedia: {e}")
        return []
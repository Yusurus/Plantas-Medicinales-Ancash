import requests

API_KEY = '2b10Q1pjh95QnKNGhW1eXZLO'
API_URL = f"https://my-api.plantnet.org/v2/identify/all?api-key={API_KEY}&lang=es&include-related-images=true"

def identificar_planta(filepath, organ='leaf'):
    with open(filepath, 'rb') as img:
        files = {'images': img}
        data = {'organs': organ}

        try:
            response = requests.post(API_URL, files=files, data=data)
            response.raise_for_status()
            result = response.json()

            if not result["results"]:
                return {'message': 'No se encontraron coincidencias'}

            top = result["results"][0]
            species = top["species"]
            images = top.get("images", [])

            image_urls = [img.get("url", {}).get("m") for img in images[:1] if img.get("url")]
            return {
                'identifiedOrgan': images[0].get("organ") if images else 'Desconocido',
                'scientificName': species.get("scientificNameWithoutAuthor", "Desconocido"),
                'authorship': species.get("scientificNameAuthorship", ""),
                'commonNames': species.get("commonNames", []),
                'genus': species.get("genus", {}).get("scientificNameWithoutAuthor", ""),
                'family': species.get("family", {}).get("scientificNameWithoutAuthor", ""),
                'score': round(top.get("score", 0) * 100, 2),
                'imageUrls': image_urls
            }

        except requests.RequestException as e:
            return {'message': f'Error al comunicarse con PlantNet: {str(e)}'}

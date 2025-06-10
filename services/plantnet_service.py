import requests
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("PLANTNET_API_KEY")

API_URL_IDENTIFY = f"https://my-api.plantnet.org/v2/identify/all?api-key={API_KEY}&lang=es&include-related-images=true"
API_URL_SPECIES_SEARCH_PROJECT = f"https://my-api.plantnet.org/v2/projects/k-western-south-america/species?lang=es&api-key={API_KEY}"
API_URL_SPECIES_SEARCH_GLOBAL = f"https://my-api.plantnet.org/v2/species?lang=es&pageSize=1&page=1&type=kt&api-key={API_KEY}"


def identificar_planta(filepath, organ="leaf"):
    with open(filepath, "rb") as img:
        files = {"images": img}
        data = {"organs": organ}

        try:
            response = requests.post(API_URL_IDENTIFY, files=files, data=data)
            response.raise_for_status()
            result = response.json()

            if not result["results"]:
                return {"message": "No se encontraron coincidencias"}

            top = result["results"][0]
            species = top["species"]
            images = top.get("images", [])

            image_urls = [
                img.get("url", {}).get("m") for img in images[:5] if img.get("url")
            ]
            return {
                "identifiedOrgan": images[0].get("organ") if images else "Desconocido",
                "scientificName": species.get(
                    "scientificNameWithoutAuthor", "Desconocido"
                ),
                "authorship": species.get("scientificNameAuthorship", ""),
                "commonNames": species.get("commonNames", []),
                "genus": species.get("genus", {}).get(
                    "scientificNameWithoutAuthor", ""
                ),
                "family": species.get("family", {}).get(
                    "scientificNameWithoutAuthor", ""
                ),
                "score": round(top.get("score", 0) * 100, 2),
                "imageUrls": image_urls,
            }

        except requests.RequestException as e:
            return {"message": f"Error al comunicarse con PlantNet: {str(e)}"}


PERU_PLANTNET_PROJECT_IDS = [
    "k-western-south-america",
    "k-northern-south-america",
    "k-brazil",
    "useful",
    "k-world-flora",
]


def identificar_por_nombre(scientific_name):
    plant_data = {
        "scientificName": scientific_name,
        "authorship": "",
        "commonNames": [],
        "genus": "",
        "family": "",
        "imageUrls": [],
    }
    params = {"prefix": scientific_name}

    for project_id in PERU_PLANTNET_PROJECT_IDS:
        api_url_project = f"https://my-api.plantnet.org/v2/projects/{project_id}/species?lang=es&api-key={API_KEY}"
        print(
            f"Intentando buscar en PlantNet (proyecto: {project_id}) para '{scientific_name}'..."
        )
        try:
            response = requests.get(api_url_project, params=params)
            response.raise_for_status()
            result_project = response.json()

            if result_project:
                top_match_project = result_project[0]
                plant_data["scientificName"] = top_match_project.get(
                    "scientificNameWithoutAuthor", scientific_name
                )
                plant_data["authorship"] = top_match_project.get(
                    "scientificNameAuthorship", ""
                )
                plant_data["commonNames"] = top_match_project.get("commonNames", [])
                plant_data["genus"] = top_match_project.get("genus", "")
                plant_data["family"] = top_match_project.get("family", "")
                print(f"Datos obtenidos del proyecto de PlantNet: {project_id}.")
                return plant_data

        except requests.RequestException as e:
            print(f"Error al comunicarse con PlantNet (proyecto {project_id}): {e}.")
        except IndexError:
            print(
                f"No se encontraron resultados en el proyecto PlantNet ({project_id}) para '{scientific_name}'."
            )
        except Exception as e:
            print(f"Error inesperado con PlantNet (proyecto {project_id}): {e}.")

    print(
        f"Ningún proyecto encontró la planta. Intentando búsqueda global (predeterminada de PlantNet)..."
    )
    try:
        response = requests.get(API_URL_SPECIES_SEARCH_GLOBAL, params=params)
        response.raise_for_status()
        result_global = response.json()

        if result_global:
            top_match_global = result_global[0]
            plant_data["scientificName"] = top_match_global.get(
                "scientificNameWithoutAuthor", scientific_name
            )
            plant_data["authorship"] = top_match_global.get(
                "scientificNameAuthorship", ""
            )
            plant_data["commonNames"] = top_match_global.get("commonNames", [])
            plant_data["genus"] = top_match_global.get("genus", "")
            plant_data["family"] = top_match_global.get("family", "")
            print("Datos obtenidos de la búsqueda global de PlantNet.")
            return plant_data

    except requests.RequestException as e:
        print(f"Error al comunicarse con PlantNet (global): {e}")
        return {"message": f"Error al comunicarse con PlantNet (global): {e}"}
    except IndexError:
        print(
            f"No se encontraron resultados globales en PlantNet para '{scientific_name}'."
        )
    except Exception as e:
        print(f"Error inesperado con PlantNet (global): {e}")

    return {
        "message": "No se encontraron detalles para el nombre científico en PlantNet."
    }

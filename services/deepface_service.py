import os
import cv2
from config.db import DIRECTORIO_ROSTROS
from config.db import get_connection
from flask import session, jsonify


def reconocer_rostro(imagen_cv):
    from deepface import DeepFace

    detector = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )
    gray = cv2.cvtColor(imagen_cv, cv2.COLOR_BGR2GRAY)
    rostros = detector.detectMultiScale(gray, 1.1, 5)

    if len(rostros) == 0:
        return {"success": False, "message": "No se detectó ningún rostro"}

    try:
        resultados = DeepFace.find(
            img_path=imagen_cv,
            db_path=DIRECTORIO_ROSTROS,
            model_name="VGG-Face",
            detector_backend="opencv",
            distance_metric="cosine",
            enforce_detection=False,
        )

        if len(resultados) > 0 and not resultados[0].empty:
            df = resultados[0]
            ruta_identidad = df.iloc[0]["identity"]
            distancia = df.iloc[0]["distance"]
            nombre_usuario = os.path.basename(os.path.dirname(ruta_identidad))
            try:
                conn = get_connection()
                cursor = conn.cursor(dictionary=True)

                # Llamada al procedimiento almacenado con solo el nombre de usuario
                cursor.callproc("obtener_datos_usuario", [nombre_usuario])

                # Recuperar el resultado del procedimiento
                for result in cursor.stored_results():
                    usuario = result.fetchone()

                if usuario:
                    session["usuario"] = {
                        "idUsuario": usuario["idUsuario"],
                        "usuario": usuario["usuario"],
                        "idEmpleado": usuario["idEmpleado"],
                        "correo": usuario["correo"],
                        "idPersona": usuario["idPersona"],
                        "DNI": usuario["DNI"],
                        "nombres": usuario["nombres"],
                        "apellido1": usuario["apellido1"],
                        "apellido2": usuario["apellido2"],
                        "telefono": usuario["telefono"],
                        "direccion": usuario["direccion"],
                        "categoria": usuario["categoria"],
                    }

                else:
                    return jsonify(
                        {"success": False, "message": "Usuario no encontrado"}
                    )
            except Exception as e:
                return jsonify(
                    {
                        "success": False,
                        "message": f"Error al obtener los datos del usuario: {str(e)}",
                    }
                )
            return {
                "success": True,
                "user": nombre_usuario,
                "confidence": round((1 - distancia) * 100, 2),
            }
        return {"success": False, "message": "Rostro no reconocido"}

    except Exception as e:
        print(f"Error con DeepFace: {e}")
        return {"success": False, "message": "Error en el reconocimiento facial"}

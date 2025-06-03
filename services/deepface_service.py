from deepface import DeepFace
import os
import cv2
import pandas as pd
from config.db import DIRECTORIO_ROSTROS

def reconocer_rostro(imagen_cv):
    detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(imagen_cv, cv2.COLOR_BGR2GRAY)
    rostros = detector.detectMultiScale(gray, 1.1, 5)

    if len(rostros) == 0:
        return {'success': False, 'message': 'No se detectó ningún rostro'}

    try:
        resultados = DeepFace.find(
            img_path=imagen_cv,
            db_path=DIRECTORIO_ROSTROS,
            model_name="VGG-Face",
            detector_backend="opencv",
            distance_metric="cosine",
            enforce_detection=True
        )

        if len(resultados) > 0 and not resultados[0].empty:
            df = resultados[0]
            ruta_identidad = df.iloc[0]['identity']
            distancia = df.iloc[0]['distance']
            nombre_usuario = os.path.basename(os.path.dirname(ruta_identidad))
            return {
                'success': True,
                'user': nombre_usuario,
                'confidence': round((1 - distancia) * 100, 2)
            }
        return {'success': False, 'message': 'Rostro no reconocido'}

    except Exception as e:
        print(f"Error con DeepFace: {e}")
        return {'success': False, 'message': 'Error en el reconocimiento facial'}

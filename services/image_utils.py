import base64
import cv2
import numpy as np
from PIL import Image
import io

def procesar_imagen_base64(imagen_base64):
    try:
        if ',' in imagen_base64:
            imagen_base64 = imagen_base64.split(',')[1]

        imagen_bytes = base64.b64decode(imagen_base64)
        imagen_pil = Image.open(io.BytesIO(imagen_bytes))
        imagen_np = np.array(imagen_pil)

        return cv2.cvtColor(imagen_np, cv2.COLOR_RGB2BGR) if len(imagen_np.shape) == 3 else imagen_np
    except Exception as e:
        print(f"Error procesando imagen: {e}")
        return None

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg'}

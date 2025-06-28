# 🌿 Plantas Medicinales de Ancash

![Python](https://img.shields.io/badge/python-3.10.4-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.1.1-green.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)
![MySQL](https://img.shields.io/badge/MySQL-8.0+-orange.svg)

## 📖 Descripción

Sistema web integral para la preservación y consulta de información sobre plantas medicinales de la región de Ancash, Perú. Este proyecto tiene como objetivo conservar el conocimiento tradicional y científico relacionado con la flora medicinal local, funcionando como una biblioteca digital accesible para investigadores, estudiantes y personas interesadas en la medicina tradicional.

## ✨ Características Principales

- 🔍 **Consulta de Base de Datos**: Sistema completo de búsqueda y filtrado de plantas medicinales
- 🤖 **Reconocimiento de Plantas con IA**: API integrada para identificación automática de especies
- 👤 **Reconocimiento Facial**: Sistema de autenticación y control de acceso
- 📝 **Gestión Completa**: Agregar, editar y archivar información de plantas
- 🗺️ **Información Geográfica**: Zonas de distribución y hábitat
- 🧬 **Datos Científicos**: Nombres científicos, morfología, taxonomía
- 🌱 **Usos Medicinales**: Aplicaciones terapéuticas tradicionales y científicas
- 📚 **Saberes Culturales**: Preservación del conocimiento ancestral
- 🖼️ **Galería de Imágenes**: Documentación visual de las especies

## 🛠️ Tecnologías Utilizadas

### Backend
- **Python 3.10.4** - Lenguaje de programación principal
- **Flask 3.1.1** - Framework web
- **MySQL** - Base de datos relacional
- **DeepFace 0.0.93** - Reconocimiento facial
- **TensorFlow 2.19.0** - Machine Learning para reconocimiento de plantas
- **OpenCV 4.11.0.86** - Procesamiento de imágenes

### Frontend
- **HTML5** - Estructura web
- **CSS3** - Estilos y diseño
- **JavaScript** - Interactividad del cliente

### Dependencias Principales
- **Flask-CORS** - Manejo de CORS
- **mysql-connector-python** - Conector MySQL
- **Pandas** - Manipulación de datos
- **NumPy** - Computación científica
- **Pillow** - Procesamiento de imágenes
- **python-dotenv** - Gestión de variables de entorno

## 📋 Requisitos del Sistema

- Python 3.10.4 o superior
- MySQL 8.0 o superior
- 4GB RAM mínimo (recomendado 8GB)
- Espacio en disco: 2GB libres
- Conexión a internet para funcionalidades de IA

## 🚀 Instalación

### 1. Clonar el Repositorio
```bash
git clone https://github.com/tu-usuario/plantas-medicinales-ancash.git
cd plantas-medicinales-ancash
```

### 2. Crear Entorno Virtual
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar Base de Datos

#### Crear base de datos MySQL:
```sql
CREATE DATABASE plantas_ancash;
USE plantas_ancash;
```

#### Configurar variables de entorno:
Crear archivo `.env` en la raíz del proyecto:
```env
DB_HOST=localhost
DB_USER=tu_usuario
DB_PASSWORD=tu_contraseña
DB_NAME=plantas_ancash
MYSQL_PORT=el_puerto

PLANTNET_API_KEY=tu_clave_secreta_de_api_pl@Net
```

### 5. Ejecutar la Aplicación
```bash
python app.py
```

La aplicación estará disponible en `http://localhost:5000`

## 📊 Estructura de la Base de Datos

### Tablas Principales:
- **plantas** - Información básica de especies
- **morfologia** - Características físicas
- **distribucion** - Zonas geográficas
- **usos_medicinales** - Aplicaciones terapéuticas
- **saberes_culturales** - Conocimiento tradicional
- **imagenes** - Galería fotográfica
- **usuarios** - Sistema de autenticación

## 🎯 Uso del Sistema

### Consulta de Plantas
1. Accede a la página principal
2. Utiliza los filtros de búsqueda (nombre, zona, uso medicinal)
3. Explora la información detallada de cada especie

### Reconocimiento con IA
1. Sube una imagen de la planta
2. El sistema procesará la imagen con IA
3. Recibirás identificación automática y especies similares

### Gestión de Contenido (Administradores)
1. Inicia sesión con reconocimiento facial
2. Accede al panel de administración
3. Agrega, edita o archiva información de plantas

## 🧪 Funcionalidades de IA

### Reconocimiento de Plantas
- Identificación automática de especies
- Análisis de características morfológicas
- Sugerencias de especies similares
- Confianza en la predicción

### Reconocimiento Facial
- Autenticación biométrica
- Control de acceso seguro
- Registro de actividad de usuarios


## 📁 Estructura del Proyecto

```
plantas-medicinales-ancash/
├── app.py                 # Aplicación principal Flask
├── requirements.txt       # Dependencias Python
├── .env                  # Variables de entorno
├── README.md             # Este archivo
├── static/
│   ├── css/             # Estilos CSS
│   ├── js/              # Scripts JavaScript
│   └── images/          # Imágenes del proyecto
├── templates/           # Templates HTML
├── models/             # Modelos de IA entrenados
├── database/           # Scripts SQL
└── uploads/            # Imágenes subidas por usuarios
```

## 🤝 Contribución

Las contribuciones son bienvenidas. Para contribuir:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 👥 Autores

- **Yusurus** - *Desarrollo inicial* - [Mi GitHub](https://github.com/Yusurus)

## 🙏 Agradecimientos

- Comunidades indígenas de Ancash por compartir su conocimiento tradicional
- Universidad/Institución colaboradora
- Expertos en botánica y medicina tradicional
- Desarrolladores de las librerías open source utilizadas

## 📞 Contacto

- **Email**: yjru_at@hotmail.com
- **LinkedIn**: [Mi Perfil](www.linkedin.com/in/yuri-jaime-rondan-ubaldo-a770aa372)
- **Proyecto**: [https://github.com/Yusurus/plantas-medicinales-ancash](https://github.com/Yusurus/Plantas-Medicinales-Ancash)

## 🔮 Próximas Características

- [ ] App móvil nativa
- [ ] API REST completa
- [ ] Sistema de geolocalización GPS
- [ ] Integración con herbarios digitales
- [ ] Modo offline para consultas
- [ ] Sistema de alertas de conservación
- [ ] Integración con redes sociales científicas

---

*Este proyecto contribuye a la preservación del patrimonio cultural y medicinal de Ancash, promoviendo el diálogo entre el conocimiento ancestral y la ciencia moderna.*

---

*Desarrollado con ❤️ para la preservación del conocimiento ancestral de Ancash*
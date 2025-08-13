# Consulta API KDBC Util

Aplicación web para consultar CMCs del KCDB (Key Comparison Database) del BIPM, con funcionalidades de búsqueda en cascada y búsqueda de incertidumbre.

## 🚀 Características

- **Búsqueda en Cascada**: 8 niveles de filtrado para CMCs
- **Fuente Dual**: API del BIPM o archivos JSON locales
- **Búsqueda de Incertidumbre**: Interfaz para consultar tablas de incertidumbre
- **Visualización JSON**: Visor interactivo de resultados con colores y expansión
- **Búsqueda Avanzada**: Formulario completo para consultas personalizadas

## 🛠️ Instalación Local

### Prerrequisitos
- Python 3.8+
- pip

### Pasos de instalación

1. **Clonar el repositorio:**
```bash
git clone <tu-repositorio>
cd CONSULTA_API_KDBC_UTIL
```

2. **Crear entorno virtual:**
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

4. **Ejecutar la aplicación:**
```bash
python app.py
```

5. **Abrir en el navegador:**
```
http://localhost:5000
```

## 🌐 Deploy en Render

### Configuración Automática

1. **Conectar repositorio en Render:**
   - Ir a [render.com](https://render.com)
   - Crear nueva cuenta o iniciar sesión
   - Click en "New +" → "Web Service"
   - Conectar tu repositorio de GitHub

2. **Configuración automática:**
   - El archivo `render.yaml` configurará automáticamente el servicio
   - Render detectará que es una aplicación Python
   - Se instalará gunicorn automáticamente

### Configuración Manual (si es necesario)

- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `gunicorn app:app`
- **Environment Variables:**
  - `PYTHON_VERSION`: `3.9.16`
  - `PORT`: Render lo configura automáticamente

### Variables de Entorno (opcionales)

```bash
# Para desarrollo local
FLASK_ENV=development
FLASK_DEBUG=1

# Para producción
FLASK_ENV=production
FLASK_DEBUG=0
```

## 📁 Estructura del Proyecto

```
CONSULTA_API_KDBC_UTIL/
├── app.py                 # Aplicación principal Flask
├── todojunto.py          # Funciones de búsqueda de incertidumbre
├── requirements.txt       # Dependencias de Python
├── render.yaml           # Configuración de Render
├── Procfile             # Comando de inicio para Render
├── runtime.txt          # Versión de Python
├── .gitignore           # Archivos a ignorar en Git
├── templates/           # Plantillas HTML
│   ├── index.html      # Página principal
│   └── advanced_search.html  # Búsqueda avanzada
├── responses/           # Respuestas guardadas de la API
├── cmc_category_tree.json    # Árbol de categorías CMC
└── CMC_EM_MUNDIAL.json      # Datos de CMC locales
```

## 🔧 Uso

### Búsqueda Básica
1. Cargar estructura del árbol de categorías
2. Seleccionar criterios en los selects en cascada
3. Elegir fuente de datos (API o JSON local)
4. Ejecutar consulta
5. Visualizar resultados en formato JSON interactivo

### Búsqueda de Incertidumbre
1. Después de obtener resultados, usar la sección de lookup
2. Seleccionar tabla específica
3. Ingresar voltaje y frecuencia
4. Obtener valor de incertidumbre

### Búsqueda Avanzada
1. Ir a `/advanced_search`
2. Usar formulario completo con múltiples parámetros
3. Ejecutar consulta personalizada

## 📊 API Endpoints

- `GET /` - Página principal
- `GET /advanced_search` - Página de búsqueda avanzada
- `POST /api/query_bipm` - Consulta a la API del BIPM
- `POST /api/lookup` - Búsqueda de incertidumbre
- `POST /api/advanced_search` - Búsqueda avanzada

## 🚀 Deploy Rápido

### Opción 1: Render (Recomendado)
1. Fork/Clone este repositorio
2. Conectar en Render
3. Deploy automático

### Opción 2: Heroku
```bash
heroku create tu-app
git push heroku main
```

### Opción 3: Vercel
```bash
vercel --python
```

## 🔍 Troubleshooting

### Error de puerto
- Verificar que el puerto 5000 esté libre
- Usar `PORT` environment variable

### Error de dependencias
- Verificar Python 3.8+
- Reinstalar: `pip install -r requirements.txt --force-reinstall`

### Error de archivos JSON
- Verificar que `cmc_category_tree.json` y `CMC_EM_MUNDIAL.json` existan
- Verificar formato JSON válido

## 📝 Licencia

Este proyecto está bajo la licencia MIT.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:
1. Fork el proyecto
2. Crear rama para feature (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request

## 📞 Soporte

Para soporte técnico o preguntas:
- Crear un issue en GitHub
- Contactar al equipo de desarrollo

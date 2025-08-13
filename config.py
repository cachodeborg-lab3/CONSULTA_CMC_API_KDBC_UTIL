# Configuración de la aplicación
import os

class Config:
    # Rutas de archivos por defecto
    DEFAULT_TREE_FILE = 'cmc_category_tree.json'
    DEFAULT_LOCAL_JSON = 'CMC_EM_MUNDIAL.json'
    
    # Configuración de la API
    BIPM_API_URL = "https://www.bipm.org/api/kcdb/cmc/searchData/physics"
    
    # Configuración del servidor
    HOST = '0.0.0.0'
    PORT = int(os.environ.get('PORT', 5000))
    DEBUG = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    
    # Configuración de archivos
    RESPONSES_FOLDER = 'responses'
    
    # Configuración de logging
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    
    @classmethod
    def get_tree_url(cls):
        """Obtiene la URL del archivo del árbol"""
        return f"/{cls.DEFAULT_TREE_FILE}"
    
    @classmethod
    def get_local_json_url(cls):
        """Obtiene la URL del archivo JSON local"""
        return f"/{cls.DEFAULT_LOCAL_JSON}"
    
    @classmethod
    def ensure_responses_folder(cls):
        """Asegura que la carpeta de respuestas exista"""
        if not os.path.exists(cls.RESPONSES_FOLDER):
            os.makedirs(cls.RESPONSES_FOLDER)

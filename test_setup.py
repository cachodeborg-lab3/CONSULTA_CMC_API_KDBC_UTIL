#!/usr/bin/env python3
"""
Script de prueba para verificar la configuración del proyecto
"""

import os
import json
from config import Config

def test_config():
    """Prueba la configuración básica"""
    print("🔧 Probando configuración...")
    
    # Verificar archivos de configuración
    print(f"📁 Carpeta de respuestas: {Config.RESPONSES_FOLDER}")
    print(f"🌐 Host: {Config.HOST}")
    print(f"🔌 Puerto: {Config.PORT}")
    print(f"🐛 Debug: {Config.DEBUG}")
    
    # Verificar archivos JSON
    tree_file = Config.DEFAULT_TREE_FILE
    json_file = Config.DEFAULT_LOCAL_JSON
    
    print(f"\n📄 Verificando archivos JSON...")
    
    if os.path.exists(tree_file):
        size = os.path.getsize(tree_file) / (1024 * 1024)  # MB
        print(f"✅ {tree_file}: {size:.2f} MB")
    else:
        print(f"❌ {tree_file}: No encontrado")
    
    if os.path.exists(json_file):
        size = os.path.getsize(json_file) / (1024 * 1024)  # MB
        print(f"✅ {json_file}: {size:.2f} MB")
    else:
        print(f"❌ {json_file}: No encontrado")
    
    # Verificar carpeta de respuestas
    print(f"\n📁 Verificando carpeta de respuestas...")
    Config.ensure_responses_folder()
    if os.path.exists(Config.RESPONSES_FOLDER):
        print(f"✅ Carpeta {Config.RESPONSES_FOLDER} creada/verificada")
    else:
        print(f"❌ Error al crear carpeta {Config.RESPONSES_FOLDER}")
    
    # Verificar archivos de templates
    print(f"\n🎨 Verificando templates...")
    templates_dir = "templates"
    if os.path.exists(templates_dir):
        templates = [f for f in os.listdir(templates_dir) if f.endswith('.html')]
        print(f"✅ Templates encontrados: {len(templates)}")
        for template in templates:
            print(f"   - {template}")
    else:
        print(f"❌ Carpeta templates no encontrada")
    
    # Verificar archivos de configuración
    print(f"\n⚙️ Verificando archivos de configuración...")
    config_files = [
        'app.py',
        'config.py',
        'requirements.txt',
        'render.yaml',
        'Procfile',
        'runtime.txt'
    ]
    
    for config_file in config_files:
        if os.path.exists(config_file):
            print(f"✅ {config_file}")
        else:
            print(f"❌ {config_file}")

def test_json_files():
    """Prueba la validez de los archivos JSON"""
    print(f"\n🔍 Probando validez de archivos JSON...")
    
    tree_file = Config.DEFAULT_TREE_FILE
    json_file = Config.DEFAULT_LOCAL_JSON
    
    # Probar árbol de categorías
    if os.path.exists(tree_file):
        try:
            with open(tree_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            print(f"✅ {tree_file}: JSON válido")
            if isinstance(data, dict):
                print(f"   - Claves principales: {list(data.keys())[:5]}")
        except json.JSONDecodeError as e:
            print(f"❌ {tree_file}: Error de JSON - {e}")
        except Exception as e:
            print(f"❌ {tree_file}: Error - {e}")
    
    # Probar JSON local
    if os.path.exists(json_file):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            print(f"✅ {json_file}: JSON válido")
            if isinstance(data, dict):
                print(f"   - Claves principales: {list(data.keys())[:5]}")
        except json.JSONDecodeError as e:
            print(f"❌ {json_file}: Error de JSON - {e}")
        except Exception as e:
            print(f"❌ {json_file}: Error - {e}")

def main():
    """Función principal"""
    print("🚀 Iniciando pruebas de configuración...\n")
    
    try:
        test_config()
        test_json_files()
        
        print(f"\n✅ Pruebas completadas exitosamente!")
        print(f"🌐 Para ejecutar la aplicación: python app.py")
        print(f"🧪 Para probar archivos: http://localhost:5000/test")
        
    except Exception as e:
        print(f"\n❌ Error durante las pruebas: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())

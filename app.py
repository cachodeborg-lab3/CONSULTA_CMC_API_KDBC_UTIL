import os
import json
import requests
from flask import Flask, request, jsonify, render_template
from datetime import datetime

# Importa la función de búsqueda de tu script original
from todojunto import lookup_tableContents_raw

# Inicializa la aplicación Flask
app = Flask(__name__)

# Asegúrate de que la carpeta 'responses' exista
if not os.path.exists('responses'):
    os.makedirs('responses')

@app.route('/')
def index():
    """Sirve la página HTML principal."""
    return render_template('index.html')

@app.route('/advanced_search')
def advanced_search():
    """Sirve la página de búsqueda avanzada."""
    return render_template('advanced_search.html')

@app.route('/api/query_bipm', methods=['POST'])
def query_bipm_api():
    """
    Recibe los parámetros de consulta, llama a la API del BIPM,
    guarda la respuesta y devuelve la lista de tablas encontradas.
    """
    payload = request.get_json()
    bipm_url = "https://www.bipm.org/api/kcdb/cmc/searchData/physics"
    headers = {"Content-Type": "application/json"}

    try:
        # 1. Realizar la consulta a la API del BIPM
        response = requests.post(bipm_url, headers=headers, json=payload)
        response.raise_for_status()  # Lanza un error si la respuesta no es 2xx
        data = response.json()

        # 2. Guardar la respuesta en un archivo con timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"responses/kcdb_response_{timestamp}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        # 3. Buscar tablas de incertidumbre en la respuesta
        tables_found = []
        if 'data' in data and isinstance(data['data'], list):
            for record in data['data']:
                if (isinstance(record, dict) and 
                    'uncertaintyTable' in record and 
                    record['uncertaintyTable'].get('tableContents') and
                    record['uncertaintyTable']['tableContents'] != '<masked>'):
                    
                    tables_found.append({
                        "id": record.get('id'),
                        "kcdbCode": record.get('kcdbCode', 'N/A'),
                        "quantityValue": record.get('quantityValue', 'N/A')
                    })
        
        return jsonify({
            "success": True,
            "message": f"Respuesta guardada en '{filename}'",
            "filename": filename,
            "tables": tables_found
        })

    except requests.exceptions.RequestException as e:
        return jsonify({"success": False, "message": f"Error de red o API: {e}"}), 500
    except Exception as e:
        return jsonify({"success": False, "message": f"Error inesperado: {e}"}), 500

@app.route('/api/lookup', methods=['POST'])
def lookup_uncertainty():
    """
    Recibe una solicitud para buscar un valor en una tabla específica
    de un archivo JSON guardado.
    """
    req_data = request.get_json()
    filename = req_data.get('filename')
    table_id = int(req_data.get('table_id'))
    voltage_query = req_data.get('voltage')
    frequency_query = req_data.get('frequency')

    if not all([filename, table_id, voltage_query, frequency_query]):
        return jsonify({"success": False, "message": "Faltan parámetros en la solicitud."}), 400

    try:
        # 1. Cargar el archivo JSON guardado
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # 2. Encontrar la tabla correcta por su ID
        target_record = None
        for record in data.get('data', []):
            if record.get('id') == table_id:
                target_record = record
                break
        
        if not target_record:
            return jsonify({"success": False, "message": f"No se encontró la tabla con ID {table_id}"}), 404

        table_contents_str = target_record['uncertaintyTable']['tableContents']

        # 3. Ejecutar la función de búsqueda de todojunto.py
        result = lookup_tableContents_raw(voltage_query, frequency_query, table_contents_str)

        return jsonify({"success": True, "result": result})

    except FileNotFoundError:
        return jsonify({"success": False, "message": f"Archivo no encontrado: {filename}"}), 404
    except Exception as e:
        return jsonify({"success": False, "message": f"Error durante la búsqueda: {e}"}), 500

@app.route('/api/advanced_search', methods=['POST'])
def advanced_search_api():
    """
    Endpoint para búsqueda avanzada con múltiples parámetros.
    """
    payload = request.get_json()
    bipm_url = "https://www.bipm.org/api/kcdb/cmc/searchData/physics"
    headers = {"Content-Type": "application/json"}

    try:
        # 1. Realizar la consulta a la API del BIPM con parámetros avanzados
        response = requests.post(bipm_url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

        # 2. Guardar la respuesta en un archivo con timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"responses/advanced_search_{timestamp}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        # 3. Buscar tablas de incertidumbre en la respuesta
        tables_found = []
        if 'data' in data and isinstance(data['data'], list):
            for record in data['data']:
                if (isinstance(record, dict) and 
                    'uncertaintyTable' in record and 
                    record['uncertaintyTable'].get('tableContents') and
                    record['uncertaintyTable']['tableContents'] != '<masked>'):
                    
                    tables_found.append({
                        "id": record.get('id'),
                        "kcdbCode": record.get('kcdbCode', 'N/A'),
                        "quantityValue": record.get('quantityValue', 'N/A')
                    })
        
        return jsonify({
            "success": True,
            "message": f"Búsqueda avanzada completada. Respuesta guardada en '{filename}'",
            "filename": filename,
            "tables": tables_found
        })

    except requests.exceptions.RequestException as e:
        return jsonify({"success": False, "message": f"Error de red o API: {e}"}), 500
    except Exception as e:
        return jsonify({"success": False, "message": f"Error inesperado: {e}"}), 500

if __name__ == '__main__':
    # Configuración para desarrollo local
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
else:
    # Configuración para producción (Render)
    # El puerto se obtiene de la variable de entorno PORT
    port = int(os.environ.get('PORT', 5000))

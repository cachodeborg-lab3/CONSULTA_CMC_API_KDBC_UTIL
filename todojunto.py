import json
from typing import Optional, Union, Any, Dict, Tuple

QuantityLike = Union[float, int, str, Tuple[Union[float, int], str], Dict[str, Any]]

SI_PREFIX = {
    "y": 1e-24, "z": 1e-21, "a": 1e-18, "f": 1e-15, "p": 1e-12, "n": 1e-9,
    "u": 1e-6, "µ": 1e-6, "μ": 1e-6, "m": 1e-3, "c": 1e-2, "d": 1e-1,
    "": 1.0, "da": 1e1, "h": 1e2, "k": 1e3, "M": 1e6, "G": 1e9, "T": 1e12
}
BASE_UNITS = {"V", "Hz"}

def _coerce_number(x: Union[str, float, int]) -> float:
    if isinstance(x, (int, float)):
        return float(x)
    return float(x.replace(",", "."))

def convert_with_unit(value: float, unit: str, expected_base: str) -> float:
    unit = unit.strip()
    if unit.endswith("hz"):
        unit = unit[:-2] + "Hz"
    if unit.endswith("v"):
        unit = unit[:-1] + "V"
    if unit.endswith("Hz") or unit.endswith("V"):
        base = "V" if unit.endswith("V") else "Hz"
        prefix = unit[: -len(base)]
    else:
        base = expected_base
        prefix = unit
    if base != expected_base:
        raise ValueError(f"Unidad base {base!r} no coincide con esperada {expected_base!r}")
    if prefix not in SI_PREFIX:
        raise ValueError(f"Prefijo SI desconocido: {prefix!r}")
    return value * SI_PREFIX[prefix]

def parse_quantity(q: QuantityLike, expected_base: str) -> float:
    if expected_base not in BASE_UNITS:
        raise ValueError(f"expected_base debe ser 'V' o 'Hz'")
    if isinstance(q, (int, float)):
        return float(q)
    if isinstance(q, tuple) and len(q) == 2:
        return convert_with_unit(_coerce_number(q[0]), str(q[1]), expected_base)
    if isinstance(q, dict):
        return convert_with_unit(_coerce_number(q.get("value")), str(q.get("unit")), expected_base)
    if isinstance(q, str):
        s = q.strip().replace(" ", "")
        i = 0
        while i < len(s) and (s[i].isdigit() or s[i] in "+-.,"):
            i += 1
        num = _coerce_number(s[:i])
        unit = s[i:] or expected_base
        return convert_with_unit(num, unit, expected_base)
    raise TypeError(f"Tipo no soportado: {type(q)}")

def tableContents_to_cells(tableContents_str: str):
    """Convierte un string JSON del campo tableContents en una lista de celdas formateadas."""
    table = json.loads(tableContents_str)

    def parse_value_with_unit(s: str) -> float:
        s = s.strip()
        if " " in s:
            value_str, unit_str = s.split()
        else:
            value_str = ''.join(ch for ch in s if (ch.isdigit() or ch in ".,"))
            unit_str = s.replace(value_str, "")
        value = float(value_str.replace(",", "."))
        multipliers = {
            "Hz": 1.0, "kHz": 1e3, "MHz": 1e6,
            "V": 1.0, "mV": 1e-3, "kV": 1e3
        }
        if unit_str not in multipliers:
            raise ValueError(f"Unidad desconocida: {unit_str}")
        return value * multipliers[unit_str]

    frequencies = []
    for col_idx in range(2, len(table["row_1"]) + 1):
        freq_label = table["row_1"][f"col_{col_idx}"]
        frequencies.append(parse_value_with_unit(freq_label))

    cells = []
    num_cols = len(frequencies)
    for row_idx in range(2, len(table) + 1):
        voltage_label = table[f"row_{row_idx}"]["col_1"]
        if "to" in voltage_label:
            v_start_str, v_end_str = voltage_label.split("to")
            v_start = parse_value_with_unit(v_start_str.strip())
            v_end = parse_value_with_unit(v_end_str.strip())
        else:
            v_start = v_end = parse_value_with_unit(voltage_label.strip())

        for col_idx in range(2, num_cols + 2):
            z_str = table[f"row_{row_idx}"][f"col_{col_idx}"]
            if z_str.strip() == "-":
                continue
            z_val = float(z_str)
            f_start = frequencies[col_idx - 2]
            f_end = f_start
            cells.append({
                "x": {"start": v_start, "end": v_end, "left_closed": True, "right_closed": True},
                "y": {"start": f_start, "end": f_end, "left_closed": True, "right_closed": True},
                "z": z_val,
                "priority": 0
            })
        
    return cells

def lookup_tableContents_raw(x: QuantityLike, y: QuantityLike, tableContents_str: str) -> Optional[float]:
    """
    Consulta directamente un campo tableContents (string JSON original),
    con x (voltaje) y y (frecuencia) con soporte de unidades. Si hay múltiples
    coincidencias, devuelve el valor 'z' (incertidumbre) más bajo.
    """
    cells = tableContents_to_cells(tableContents_str)
    xv = parse_quantity(x, "V")
    yv = parse_quantity(y, "Hz")

    matching_results = []
    for cell in cells:
        if cell["x"]["start"] <= xv <= cell["x"]["end"] and cell["y"]["start"] <= yv <= cell["y"]["end"]:
            matching_results.append(cell["z"])

    if not matching_results:
        return None
    return min(matching_results)

if __name__ == "__main__":
    # --- Sección de Pruebas Exhaustivas ---

    # 1. Cargar el JSON de ejemplo
    json_file_path = "CMC_EM_AR_ACVSOURCE.json"
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            cmc_data = json.load(f)
        # Extraer el campo 'tableContents' que es un string JSON
        table_contents_str = cmc_data['data'][0]['uncertaintyTable']['tableContents']
        print(f"Tabla de incertidumbre cargada desde '{json_file_path}'.\n")
    except (FileNotFoundError, KeyError, IndexError) as e:
        print(f"Error crítico al cargar el JSON de prueba: {e}")
        print("No se pueden ejecutar las pruebas.")
        exit()

    # 2. Definir casos de prueba
    # Formato: (descripcion, voltage_query, frequency_query, expected_result)
    test_cases = [
        # --- Casos básicos y formatos de entrada ---
        ("String: Valor dentro de rango", "0.5 V", "10 kHz", 30.0),
        ("String: Sin espacio", "500mV", "200kHz", 80.0),
        ("Tupla: Límite inferior de rango", (1, "V"), (50, "kHz"), 8.0),
        ("Diccionario: Límite superior de rango", {"value": 10, "unit": "V"}, {"value": 70, "unit": "kHz"}, 15.0),
        ("Número (float/int): Asume unidad base (V y Hz)", 500, 10000, 25.0),

        # --- Casos de borde y múltiples coincidencias ---
        ("Borde (1V): Múltiples coincidencias, elige el mínimo", "1V", "10 kHz", 7.0),
        ("Borde (10V): Múltiples coincidencias, elige el mínimo", "10 V", "20 kHz", 7.0),
        
        # --- Casos con diferentes prefijos SI ---
        ("Prefijo 'k' en V", "0.5 kV", "20 kHz", 30.0),
        ("Prefijo 'M' en Hz", "2 V", "0.7 MHz", 45.0),
        ("Prefijo 'µ' en V", "500 µV", "10 kHz", 30.0),
        
        # --- Casos sin resultado esperado (fuera de rango) ---
        ("Fuera de rango (Voltaje bajo)", "0.05 V", "10 kHz", None),
        ("Fuera de rango (Voltaje alto)", "1200 V", "10 kHz", None),
        ("Fuera de rango (Frecuencia alta)", "1 V", "2 MHz", None),
        ("Celda vacía ('-') en la tabla", "50 V", "500 kHz", None),
    ]

    # 3. Ejecutar pruebas y mostrar resultados
    print("--- Ejecutando Casos de Prueba ---")
    passed_count = 0
    failed_count = 0

    for i, (desc, v_query, f_query, expected) in enumerate(test_cases):
        print(f"\n[{i+1}/{len(test_cases)}] Test: {desc}")
        print(f"    Consulta: V={v_query}, F={f_query}")
        try:
            result = lookup_tableContents_raw(v_query, f_query, table_contents_str)
            if result == expected:
                print(f"    ✅ PASSED. Resultado: {result}")
                passed_count += 1
            else:
                print(f"    ❌ FAILED. Resultado: {result}, Esperado: {expected}")
                failed_count += 1
        except Exception as e:
            print(f"    💥 ERROR durante la ejecución: {e}")
            failed_count += 1

    # 4. Resumen final
    print("\n--- Resumen de Pruebas ---")
    print(f"Total: {len(test_cases)}")
    print(f"✅ Pasaron: {passed_count}")
    print(f"❌ Fallaron: {failed_count}")
    print("--------------------------")

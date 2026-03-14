# persisntecia de datos de archivos 
from pathlib import Path
import json
from json import JSONDecodeError
import csv

DATA_DIR = Path(__file__).parent / "data"
TXT_FILE = DATA_DIR / "datos.txt"
CSV_FILE = DATA_DIR / "datos.csv"
JSON_FILE = DATA_DIR / "datos.json"
# ASEGURAR LA DATA 
def asegurar_data_dir():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

# Guardar datos en un archivo de texto

def guardar_txt(registro: str):
    asegurar_data_dir()
    with open(TXT_FILE, 'a', encoding="utf-8") as f:
        f.write(registro + '\n')

# leer datos de un archivo de texto
def leer_txt():
    asegurar_data_dir()
    if not TXT_FILE.exists():
        return []
    with open(TXT_FILE, 'r', encoding="utf-8") as f:
        return [line.strip() for line in f.readlines() if line.strip()] 
    
# JSON
def guardar_json(dic):
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    data = leer_json()   # <- ahora leer_json ya es seguro
    data.append(dic)

    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# leer json 
def leer_json():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    if not JSON_FILE.exists():
        return []

    # Si el archivo existe pero está vacío
    if JSON_FILE.stat().st_size == 0:
        return []

    with open(JSON_FILE, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
            return data if isinstance(data, list) else []
        except JSONDecodeError:
            return []
        
# CSV
def guardar_csv(dic: dict):
    """
    Guarda 1 registro en datos.csv con cabecera.
    dic esperado: {'nombre':..., 'descripcion':..., 'cantidad':..., 'precio':...}
    """
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    campos = ["nombre", "descripcion", "precio", "cantidad"]
    existe = CSV_FILE.exists()

    with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=campos)

        # Si es nuevo, escribe encabezados
        if not existe:
            writer.writeheader()

        # Escribe la fila (solo con campos esperados)
        writer.writerow({
            "nombre": dic.get("nombre", ""),
            "descripcion": dic.get("descripcion", ""),
            "precio": dic.get("precio", ""),
            "cantidad": dic.get("cantidad", "")
        })

def leer_csv():
    """
    Lee datos.csv y devuelve lista de diccionarios.
    """
    if not CSV_FILE.exists():
        return []

    with open(CSV_FILE, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)

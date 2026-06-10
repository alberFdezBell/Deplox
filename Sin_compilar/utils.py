import json
import os

CONFIG_FILE = "config.json"


def load_config():
    """Carga config de forma segura (evita crashes por JSON vacío o corrupto)."""
    if not os.path.exists(CONFIG_FILE):
        return {"apps": []}

    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            content = f.read().strip()

            if not content:
                return {"apps": []}

            return json.loads(content)

    except json.JSONDecodeError:
        return {"apps": []}
    except Exception:
        return {"apps": []}


def save_config(data):
    """Guarda configuración en JSON."""
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def add_app(data, name, url):
    """Añade una app a la lista."""
    data["apps"].append({
        "name": name,
        "url": url
    })
    return data


def remove_app(data, name):
    """Elimina app por nombre."""
    data["apps"] = [a for a in data["apps"] if a["name"] != name]
    return data


def export_config(path):
    """Exporta config a archivo externo."""
    data = load_config()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def import_config(path):
    """Importa config desde archivo externo."""
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    save_config(data)
    return data
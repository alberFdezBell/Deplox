# DeploX

DeploX es una herramienta portátil para técnicos IT que permite crear paquetes de despliegue de software personalizados. Mediante una interfaz intuitiva, puedes añadir instaladores locales o URLs, generar configuraciones reutilizables y desplegar aplicaciones en cualquier equipo desde un USB de forma rápida, sencilla y centralizada.

<img width="900" height="292" alt="deplox" src="https://github.com/user-attachments/assets/0ca45bde-d187-4cce-900d-fc03ce676a98" />

---

## - Tabla de contenidos

- Características
- Estructura del proyecto
- Requisitos
- Instalación
- Compilación a EXE
- Uso del sistema
- Configuración avanzada
- Solución de problemas

---

## - Características

- **Configurador intuitivo**: Añade aplicaciones por URL o archivos locales
- **Descarga inteligente**: Detecta automáticamente si es URL o archivo local
- **Empaquetado en ZIP**: Descarga múltiples apps y crea un ZIP listo para distribuir
- **Selector de ubicación**: El usuario elige dónde guardar el paquete (por defecto Descargas)
- **Portabilidad**: Funciona en pendrives sin necesidad de instalación
- **Sin dependencias externas** (excepto PySide6 y requests para compilación)

---

## - Estructura del proyecto

```
DeploX/
├── config.py          # Configurador de aplicaciones
├── download.py        # Descargador y empaquetador
├── utils.py          # Funciones auxiliares compartidas
├── config.spec       # Configuración de compilación (PyInstaller)
├── download.spec     # Configuración de compilación (PyInstaller)
├── config.json       # Base de datos de configuración (se genera automáticamente)
├── README.md         # Este archivo
└── [carpetas generadas en tiempo de ejecución]
    ├── downloads/    # Archivos descargados temporales
    └── local_files/  # Archivos copiados desde el disco
```

---

## - Requisitos

### Desarrollo (Python 3.8+)

```bash
pip install PySide6>=6.0.0
pip install requests>=2.25.0
```

### Ejecución (EXE compilado)

- Windows 7 o superior
- No requiere Python instalado
- ~150-200 MB de espacio libre (varía según las apps)

---

## - Instalación

### Opción 1: Ejecutar desde Python

1. **Clonar o descargar el proyecto**

2. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

3. **Ejecutar**
```bash
# Configurador
python config.py

# Descargador
python download.py
```

### Opción 2: Usar EXE compilados

Solo necesitas los archivos `.exe` generados.

---

## - Compilación a EXE

(En este repositorio están los archivos .exe)

### Requisitos previos

```bash
pip install pyinstaller>=5.0.0
```

### Compilar ambas aplicaciones

#### Opción A: Script automático (si existe)

```bash
pyinstaller config.spec
pyinstaller download.spec
```

#### Opción B: Comandos manuales

**Configurador (config.py)**
```bash
python -m PyInstaller --onefile --windowed --name config --icon=deploX.ico config.py
```

**Descargador (download.py)**
```bash
python -m PyInstaller --onefile --windowed --name download --icon=deploX.ico download.py
```

### Resultado

Los ejecutables se generarán en la carpeta `dist/`:
- `dist/ConfigITTool.exe` - Configurador
- `dist/ITInstaller.exe` - Descargador

### Opciones de PyInstaller

- `--onefile`: Crea un único EXE
- `--windowed`: Sin consola (interfaz gráfica)
- `--icon=deployX.ico`: Icono personalizado (opcional)
- `--name`: Nombre del ejecutable

---

## - Uso del sistema

### Flujo de trabajo

```
1. CONFIGURAR (config.py)
   ↓
2. DESCARGAR (download.py)
   ↓
3. EMPAQUETAR (ZIP automático)
```

### Paso 1: Configurador (config.exe)


1. **Nombre de la app**
   - Escribe el nombre de la aplicación
   - Ej: "Visual Studio Code", "7-Zip", etc.

2. **URL o archivo**
   - Opción A: Pega una URL directa
     ```
     https://example.com/installer.exe
     ```
   - Opción B: Selecciona un archivo local con el botón "Seleccionar archivo"

3. **Guardar configuración**
   - Click en "Guardar configuración"
   - Se añade automáticamente a la lista
   - Los campos se limpian para la siguiente entrada

4. **Gestionar lista**
   - Selecciona una app y haz click en "Eliminar seleccionado" para quitarla
   - La lista se actualiza automáticamente

**Archivo generado**: `config.json`
```json
{
    "apps": [
        {
            "name": "Visual Studio Code",
            "type": "url",
            "source": "https://code.visualstudio.com/download"
        },
        {
            "name": "7-Zip",
            "type": "file",
            "source": "local_files/7z2401-x64.exe"
        }
    ]
}
```

### Paso 2: Descargador (download.exe)


1. **Seleccionar aplicaciones**
   - Marca las apps que quieres descargar
   - Puedes seleccionar una, varias o todas

2. **Iniciar descarga**
   - Click en botón "Instalar"
   - Se abre diálogo "Guardar como"

3. **Elegir ubicación**
   - Por defecto apunta a carpeta "Descargas"
   - Puedes cambiar la ubicación
   - Puedes cambiar el nombre del ZIP

4. **Resultado**
   - Se descarga todo
   - Se empaqueta en un ZIP
   - Opción de abrir la carpeta automáticamente

**Archivo generado**: `paquete_instalacion_YYYYMMDD_HHMMSS.zip`

---

## - Configuración avanzada

### Archivo config.json

Edita directamente si necesitas ajustes avanzados:

```json
{
    "apps": [
        {
            "name": "Nombre visible",
            "type": "url",
            "source": "https://..."
        },
        {
            "name": "Nombre visible",
            "type": "file",
            "source": "ruta/al/archivo.exe"
        }
    ]
}
```

### Tipos soportados

| Tipo | Descripción | Ejemplo |
|------|------------|---------|
| `url` | Descarga desde internet | `https://example.com/file.exe` |
| `file` | Archivo local | `local_files/installer.exe` |

### Ejecutar desde un pendrive

1. Copia los archivos `.exe` al pendrive
2. El programa detecta automáticamente la ubicación y creará el archivo `config.json`
3. Los archivos se descargan a la carpeta elegida por el usuario (no en el pendrive)

---

## - Solución de problemas

### "No se puede encontrar config.json"

**Causa**: El configurador no se ha ejecutado nunca
**Solución**: 
1. Ejecuta primero `config.exe`
2. Añade al menos una aplicación
3. Ahora `download.exe` funcionará

### "Error al descargar URL"

**Causa**: URL inválida o servidor no disponible
**Solución**:
1. Verifica que la URL sea correcta
2. Prueba en el navegador
3. Comprueba tu conexión a internet

### "ZIP corrupto"

**Causa**: Descarga incompleta o problema de espacio
**Solución**:
1. Verifica espacio libre en disco
2. Intenta con menos apps
3. Usa otra ubicación de descarga

---

## - Estructura de archivos generados

### En tiempo de ejecución

```
DeploX/
├── config.json          # Guardado automático de configuraciones
├── local_files/         # Archivos copiados desde el disco
│   ├── ej.exe
│   └── ej.msi
└── downloads/           # Archivos temporales (se limpian)
    └── temp_pack/
```

---

## - Tips 

1. **Compartir configuración**:
   - Distribuye el `config.json` a otros usuarios
   - Todos obtendrán las mismas apps al descargar


---

## - Licencia

Proyecto de uso interno. Redistribución permitida siempre que se mantenga esta documentación.

---

**Versión**: 1.0  
**Última actualización**: Junio 2026  
**-Alberto Fernández Bellido-**
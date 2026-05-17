import os
import re
import glob

def extraer_librerias(archivo):
    librerias = set()
    
    # Expresiones regulares para capturar el nombre principal de la librería
    patron_import = re.compile(r'^\s*import\s+([a-zA-Z0-9_]+)')
    patron_from = re.compile(r'^\s*from\s+([a-zA-Z0-9_]+)')
    
    es_qmd = archivo.endswith('.qmd')
    dentro_de_codigo = not es_qmd

    try:
        with open(archivo, 'r', encoding='utf-8') as f:
            for linea in f:
                linea_strip = linea.strip()
                # Detectar inicio de bloque de código Python
                if es_qmd:
                    if linea_strip.startswith('```python') or linea_strip.startswith('```{python}'):
                        dentro_de_codigo = True
                        continue
                    # Detectar fin de bloque de código
                    elif linea_strip.startswith('```') and dentro_de_codigo:
                        dentro_de_codigo = False
                        continue
                
                # Si estamos dentro de un bloque de código, buscar imports
                if dentro_de_codigo:
                    match_import = patron_import.match(linea)
                    if match_import:
                        librerias.add(match_import.group(1))
                    
                    match_from = patron_from.match(linea)
                    if match_from:
                        librerias.add(match_from.group(1))
                        
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{archivo}'")
        return set()

    return librerias

def main():
    # Rutas relativas: asume que el script está en Documentación_plantilla/scripts
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    directorio_raiz = os.path.abspath(os.path.join(directorio_actual, '..', '..'))
    ruta_req = os.path.join(directorio_actual, 'requirements.txt')
    
    # Buscar todos los archivos .qmd y .py en la raíz
    archivos_qmd = glob.glob(os.path.join(directorio_raiz, '*.qmd'))
    archivos_py = glob.glob(os.path.join(directorio_raiz, '*.py'))
    archivos_a_analizar = archivos_qmd + archivos_py
    
    todas_las_librerias = set()
    
    for archivo in archivos_a_analizar:
        librerias_archivo = extraer_librerias(archivo)
        todas_las_librerias.update(librerias_archivo)
    
    if todas_las_librerias:
        print("Librerías extraídas del proyecto:")
        for lib in sorted(list(todas_las_librerias)):
            print(f"  - {lib}")
        
        # Librerías base necesarias para que Quarto ejecute Python
        base_libs = {'jupyter', 'ipykernel', 'PyYAML'}
        
        # Librerías estándar de Python que no se instalan por pip o librerías locales
        builtins = {'os', 'sys', 're', 'math', 'time', 'datetime', 'json', 'csv', 'random', 'pathlib', 'collections', 'itertools', 'io', 'typing', 'base64', '__future__', 'init'}
        
        # Unir base + extraídas y restar built-ins
        todas_libs = base_libs.union(todas_las_librerias)
        libs_a_instalar = sorted(list(todas_libs - builtins))
        
        # Crear/Sobrescribir el archivo requirements.txt
        with open(ruta_req, 'w', encoding='utf-8') as f:
            f.write("# Librerías base para Quarto/Jupyter\n")
            for lib in sorted(list(base_libs)):
                f.write(f"{lib}\n")
            
            f.write("\n# Librerías extraídas del análisis\n")
            for lib in sorted(list(set(libs_a_instalar) - base_libs)):
                f.write(f"{lib}\n")
                
        print(f"\nArchivo 'requirements.txt' generado exitosamente en la carpeta de scripts.")
        print("Para instalarlas manualmente, ejecuta: pip install -r requirements.txt")
    else:
        print("No se encontraron importaciones de librerías en el proyecto.")

if __name__ == '__main__':
    main()

import os
import re
import sys
import subprocess
import glob

# Dependencias base necesarias para que PyQuarto funcione
CORE_DEPS = ["jupyter", "jupyterlab", "notebook"]

def get_stdlib_modules():
    if sys.version_info >= (3, 10):
        return sys.stdlib_module_names
    else:
        # Fallback básico para versiones antiguas
        return {"os", "sys", "re", "math", "time", "datetime", "json", "csv", "random", "subprocess", "glob", "shutil"}

def extract_imports_from_python(code):
    imports = set()
    # Coincide con 'import modulo' o 'import modulo.algo' o 'import modulo as alias'
    for match in re.finditer(r'^\s*import\s+([a-zA-Z0-9_]+)', code, re.MULTILINE):
        imports.add(match.group(1))
    # Coincide con 'from modulo import algo'
    for match in re.finditer(r'^\s*from\s+([a-zA-Z0-9_]+)', code, re.MULTILINE):
        imports.add(match.group(1))
    return imports

def extract_imports_from_qmd(content):
    # Encuentra bloques de código de Python (tanto ```python como ```{python})
    python_blocks = re.findall(r'```(?:\{python\}|python)\s*(.*?)\s*```', content, re.DOTALL | re.IGNORECASE)
    imports = set()
    for block in python_blocks:
        imports.update(extract_imports_from_python(block))
    return imports

def get_all_project_imports(project_dir):
    all_imports = set()
    
    # Procesar archivos .py
    for filepath in glob.glob(os.path.join(project_dir, '**', '*.py'), recursive=True):
        if '.venv' in filepath or 'env' in filepath or 'instalar_dependencias.py' in filepath:
            continue
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                all_imports.update(extract_imports_from_python(f.read()))
        except Exception:
            pass
            
    # Procesar archivos .qmd
    for filepath in glob.glob(os.path.join(project_dir, '**', '*.qmd'), recursive=True):
        if '.venv' in filepath or 'env' in filepath:
            continue
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                all_imports.update(extract_imports_from_qmd(f.read()))
        except Exception:
            pass
            
    return all_imports

def main():
    print("Iniciando escaneo dinámico de dependencias...")
    # El script está en Documentación_plantilla/scripts/, el root es 2 niveles arriba
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(os.path.dirname(script_dir))
    
    # 1. Instalar dependencias base
    print(f"\n[1/3] Instalando dependencias base de PyQuarto: {', '.join(CORE_DEPS)}")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install"] + CORE_DEPS)
    except subprocess.CalledProcessError:
        print("Advertencia: Hubo un problema instalando las dependencias base.")

    # 2. Extraer dependencias del código
    print(f"\n[2/3] Escaneando archivos .py y .qmd en: {project_dir}")
    found_imports = get_all_project_imports(project_dir)
    stdlib_modules = get_stdlib_modules()
    
    # Mapeos comunes de nombre de import a nombre de paquete en pip
    package_mappings = {
        'bs4': 'beautifulsoup4',
        'sklearn': 'scikit-learn',
        'PIL': 'Pillow',
        'cv2': 'opencv-python',
        'yaml': 'PyYAML',
        'dotenv': 'python-dotenv',
        'dateutil': 'python-dateutil',
        'win32com': 'pywin32'
    }
    
    deps_to_install = set()
    for imp in found_imports:
        if imp in stdlib_modules or imp in sys.builtin_module_names:
            continue
        pkg_name = package_mappings.get(imp, imp)
        if pkg_name not in CORE_DEPS: # No instalar dos veces
            deps_to_install.add(pkg_name)
        
    if not deps_to_install:
        print("\n[3/3] No se encontraron dependencias externas adicionales en el código.")
        print("\nProceso de instalación finalizado.")
        return
        
    print(f"\n[3/3] Dependencias encontradas para instalar: {', '.join(deps_to_install)}")
    
    # 3. Instalar dependencias extraídas
    for dep in sorted(deps_to_install):
        print(f"-> Instalando {dep}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", dep], 
                                  stdout=subprocess.DEVNULL, 
                                  stderr=subprocess.DEVNULL)
            print(f"   [OK] {dep} instalado correctamente.")
        except subprocess.CalledProcessError:
            print(f"   [ERROR] No se pudo instalar {dep}. Es posible que el nombre en pip sea distinto al del import.")

    print("\nProceso de instalación finalizado exitosamente.")

if __name__ == "__main__":
    main()

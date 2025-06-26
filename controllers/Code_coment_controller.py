from flask import render_template, Blueprint
###----------
import os
import json
from flask import jsonify, request

comendt_bd = Blueprint('comendt_bd', __name__)

# Configuración personalizable
CUSTOM_TEMPLATES_FOLDER = 'templates/help'  # Cambia esto por tu carpeta deseada
ALLOWED_FILES = []  # Lista vacía = todos los archivos HTML, o especifica: ['archivo1.html', 'archivo2.html']
EXCLUDED_FILES = ['base.html', 'layout.html']  # Archivos que quieres excluir

@comendt_bd.route('/help_coment')
def coment_page():
    """
    Página de ayuda dinámica
    """
    return render_template('help_coment.html')

##------

@comendt_bd.route('/api/html-files-tree')
def get_html_files_tree():
    """
    Obtiene la estructura de archivos HTML en formato árbol desde carpeta personalizada
    """
    try:
        # Usar carpeta personalizada en lugar de 'templates'
        custom_path = os.path.join(os.getcwd(), CUSTOM_TEMPLATES_FOLDER)
        
        # Verificar si la carpeta existe
        if not os.path.exists(custom_path):
            return jsonify({'error': f'La carpeta {CUSTOM_TEMPLATES_FOLDER} no existe'}), 404
        
        tree_structure = build_html_tree(custom_path)
        return jsonify({
            'tree': tree_structure,
            'base_folder': CUSTOM_TEMPLATES_FOLDER,
            'total_files': count_html_files(tree_structure)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@comendt_bd.route('/api/html-files-tree/<path:custom_folder>')
def get_html_files_tree_custom(custom_folder):
    """
    Obtiene la estructura de archivos HTML desde una carpeta específica por parámetro
    """
    try:
        custom_path = os.path.join(os.getcwd(), custom_folder)
        
        # Verificar si la carpeta existe
        if not os.path.exists(custom_path):
            return jsonify({'error': f'La carpeta {custom_folder} no existe'}), 404
        
        tree_structure = build_html_tree(custom_path)
        return jsonify({
            'tree': tree_structure,
            'base_folder': custom_folder,
            'total_files': count_html_files(tree_structure)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@comendt_bd.route('/api/html-file-content')
def get_html_file_content():
    """
    Obtiene el contenido de un archivo HTML específico desde carpeta personalizada
    """
    try:
        file_path = request.args.get('path')
        custom_folder = request.args.get('folder', CUSTOM_TEMPLATES_FOLDER)
        
        if not file_path:
            return jsonify({'error': 'Path del archivo requerido'}), 400
        
        # Validar que el archivo esté dentro de la carpeta personalizada
        base_path = os.path.join(os.getcwd(), custom_folder)
        full_path = os.path.join(base_path, file_path)
        
        # Verificar que el archivo existe y es HTML
        if not os.path.exists(full_path) or not full_path.endswith('.html'):
            return jsonify({'error': 'Archivo no encontrado o no es HTML'}), 404
        
        # Verificar si el archivo está en la lista de permitidos (si se especifica)
        filename = os.path.basename(file_path)
        if not is_file_allowed(filename):
            return jsonify({'error': 'Archivo no permitido'}), 403
        
        # Leer el contenido del archivo
        with open(full_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Extraer funciones JavaScript del archivo
        functions = extract_javascript_functions(content)
        
        return jsonify({
            'content': content,
            'functions': functions,
            'path': file_path,
            'folder': custom_folder,
            'filename': filename,
            'size': os.path.getsize(full_path)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@comendt_bd.route('/api/config')
def get_config():
    """
    Obtiene la configuración actual del controlador
    """
    return jsonify({
        'custom_folder': CUSTOM_TEMPLATES_FOLDER,
        'allowed_files': ALLOWED_FILES,
        'excluded_files': EXCLUDED_FILES,
        'filter_active': len(ALLOWED_FILES) > 0
    })

@comendt_bd.route('/api/config', methods=['POST'])
def update_config():
    """
    Actualiza la configuración del controlador
    """
    try:
        data = request.get_json()
        
        global CUSTOM_TEMPLATES_FOLDER, ALLOWED_FILES, EXCLUDED_FILES
        
        if 'custom_folder' in data:
            CUSTOM_TEMPLATES_FOLDER = data['custom_folder']
        
        if 'allowed_files' in data:
            ALLOWED_FILES = data['allowed_files']
        
        if 'excluded_files' in data:
            EXCLUDED_FILES = data['excluded_files']
        
        return jsonify({
            'success': True,
            'message': 'Configuración actualizada',
            'config': {
                'custom_folder': CUSTOM_TEMPLATES_FOLDER,
                'allowed_files': ALLOWED_FILES,
                'excluded_files': EXCLUDED_FILES
            }
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def build_html_tree(root_path, current_path=''):
    """
    Construye la estructura de árbol de archivos HTML con filtros personalizados
    """
    tree = []
    
    try:
        full_current_path = os.path.join(root_path, current_path) if current_path else root_path
        
        if not os.path.exists(full_current_path):
            return tree
        
        items = sorted(os.listdir(full_current_path))
        
        for item in items:
            item_path = os.path.join(full_current_path, item)
            relative_path = os.path.join(current_path, item) if current_path else item
            
            # Ignorar archivos y carpetas ocultas
            if item.startswith('.'):
                continue
            
            if os.path.isdir(item_path):
                # Es una carpeta
                children = build_html_tree(root_path, relative_path)
                if children:  # Solo incluir carpetas que tengan archivos HTML permitidos
                    tree.append({
                        'name': item,
                        'type': 'folder',
                        'path': relative_path.replace('\\', '/'),
                        'children': children
                    })
            elif item.endswith('.html'):
                # Es un archivo HTML - aplicar filtros
                if is_file_allowed(item):
                    tree.append({
                        'name': item,
                        'type': 'file',
                        'path': relative_path.replace('\\', '/'),
                        'size': os.path.getsize(item_path),
                        'modified': os.path.getmtime(item_path)
                    })
    
    except Exception as e:
        print(f"Error building tree for {current_path}: {e}")
    
    return tree

def is_file_allowed(filename):
    """
    Verifica si un archivo está permitido según la configuración
    """
    # Si está en la lista de excluidos, no permitir
    if filename in EXCLUDED_FILES:
        return False
    
    # Si hay lista de permitidos y el archivo no está en ella, no permitir
    if ALLOWED_FILES and filename not in ALLOWED_FILES:
        return False
    
    return True

def count_html_files(tree_structure):
    """
    Cuenta el total de archivos HTML en la estructura del árbol
    """
    count = 0
    for item in tree_structure:
        if item['type'] == 'file':
            count += 1
        elif item['type'] == 'folder':
            count += count_html_files(item['children'])
    return count

def extract_javascript_functions(html_content):
    """
    Extrae las funciones JavaScript de un archivo HTML
    """
    import re
    
    functions = []
    
    # Buscar bloques de script
    script_pattern = r'<script[^>]*>(.*?)</script>'
    scripts = re.findall(script_pattern, html_content, re.DOTALL | re.IGNORECASE)
    
    for script in scripts:
        # Buscar funciones (function nombre() y async function nombre())
        function_patterns = [
            r'function\s+(\w+)\s*\([^)]*\)\s*{',
            r'async\s+function\s+(\w+)\s*\([^)]*\)\s*{',
            r'const\s+(\w+)\s*=\s*(?:async\s+)?function\s*\([^)]*\)\s*=>\s*{',
            r'let\s+(\w+)\s*=\s*(?:async\s+)?function\s*\([^)]*\)\s*=>\s*{',
            r'var\s+(\w+)\s*=\s*(?:async\s+)?function\s*\([^)]*\)\s*=>\s*{',
            r'const\s+(\w+)\s*=\s*\([^)]*\)\s*=>\s*{',
        ]
        
        for pattern in function_patterns:
            matches = re.findall(pattern, script, re.IGNORECASE)
            for match in matches:
                if match not in functions:
                    functions.append(match)
    
    return sorted(list(set(functions)))  # Eliminar duplicados y ordenar
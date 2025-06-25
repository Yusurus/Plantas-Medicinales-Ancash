from flask import Flask, jsonify, request, render_template, Blueprint
import os
import re
from pathlib import Path

help_bp = Blueprint('help_bp', __name__)

class HelpSystemBackend:
    def __init__(self, html_directories):
        """
        Inicializa el sistema de ayuda con las carpetas a escanear
        html_directories: lista de carpetas donde buscar archivos HTML
        """
        self.html_directories = html_directories
    
    def scan_html_files(self):
        """
        Escanea todas las carpetas especificadas buscando archivos HTML
        Retorna una estructura de árbol
        """
        file_tree = {}
        
        for directory in self.html_directories:
            if not os.path.exists(directory):
                continue
                
            dir_name = os.path.basename(directory)
            file_tree[dir_name] = self._scan_directory(directory)
        
        return file_tree
    
    def _scan_directory(self, directory):
        """
        Escanea recursivamente un directorio
        """
        result = {'type': 'folder', 'children': {}}
        
        try:
            for item in sorted(os.listdir(directory)):
                item_path = os.path.join(directory, item)
                
                if os.path.isdir(item_path):
                    # Es una carpeta
                    result['children'][item] = self._scan_directory(item_path)
                elif item.endswith('.html'):
                    # Es un archivo HTML
                    result['children'][item] = {
                        'type': 'file',
                        'path': item_path
                    }
        except PermissionError:
            pass
        
        return result
    
    def get_file_content(self, file_path):
        """
        Obtiene el contenido de un archivo HTML
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                
            # Procesar el contenido para extraer información útil
            processed_content = self._process_html_content(content, file_path)
            return processed_content
            
        except Exception as e:
            return f"Error leyendo archivo: {str(e)}"
    
    def _process_html_content(self, content, file_path):
        """
        Procesa el contenido HTML para mostrar información útil
        """
        # Extraer título
        title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
        title = title_match.group(1) if title_match else "Sin título"
        
        # Extraer comentarios de ayuda
        help_comments = re.findall(r'<!--\s*HELP:\s*(.*?)\s*-->', content, re.DOTALL)
        
        # Extraer meta descripción
        meta_desc = re.search(r'<meta\s+name=[\"\']description[\"\']\s+content=[\"\'](.*?)[\"\']', content, re.IGNORECASE)
        description = meta_desc.group(1) if meta_desc else "Sin descripción"
        
        # Crear HTML procesado
        processed_html = f"""
        <div class="file-info">
            <h2>{title}</h2>
            <p><strong>Archivo:</strong> {file_path}</p>
            <p><strong>Descripción:</strong> {description}</p>
        </div>
        """
        
        if help_comments:
            processed_html += "<div class='help-comments'><h3>Comentarios de Ayuda:</h3><ul>"
            for comment in help_comments:
                processed_html += f"<li>{comment.strip()}</li>"
            processed_html += "</ul></div>"
        
        # Mostrar el contenido HTML original con resaltado
        escaped_content = content.replace('<', '&lt;').replace('>', '&gt;')
        processed_html += f"""
        <div class="source-code">
            <h3>Código Fuente:</h3>
            <pre style="background: #f8f9fa; padding: 15px; border-radius: 5px; overflow-x: auto; white-space: pre-wrap;">{escaped_content}</pre>
        </div>
        """
        
        return processed_html
    
    def extract_javascript_functions(self, file_path):
        """
        Extrae las funciones JavaScript de un archivo HTML
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            functions = []
            
            # Buscar bloques de script
            script_blocks = re.findall(r'<script[^>]*>(.*?)</script>', content, re.DOTALL | re.IGNORECASE)
            
            for script_content in script_blocks:
                # Buscar funciones JavaScript
                function_patterns = [
                    r'function\s+(\w+)\s*\([^)]*\)\s*{',  # function nombre()
                    r'(\w+)\s*=\s*function\s*\([^)]*\)\s*{',  # nombre = function()
                    r'(\w+)\s*:\s*function\s*\([^)]*\)\s*{',  # nombre: function()
                    r'const\s+(\w+)\s*=\s*\([^)]*\)\s*=>', # const nombre = () =>
                    r'let\s+(\w+)\s*=\s*\([^)]*\)\s*=>', # let nombre = () =>
                    r'var\s+(\w+)\s*=\s*\([^)]*\)\s*=>', # var nombre = () =>
                ]
                
                lines = script_content.split('\n')
                for line_num, line in enumerate(lines, 1):
                    for pattern in function_patterns:
                        matches = re.finditer(pattern, line)
                        for match in matches:
                            func_name = match.group(1)
                            
                            # Extraer comentario de descripción si existe
                            desc = "Función JavaScript"
                            if line_num > 1:
                                prev_line = lines[line_num - 2].strip()
                                if prev_line.startswith('//'):
                                    desc = prev_line[2:].strip()
                                elif prev_line.startswith('/*') and prev_line.endswith('*/'):
                                    desc = prev_line[2:-2].strip()
                            
                            functions.append({
                                'name': f"{func_name}()",
                                'desc': desc,
                                'line': line_num
                            })
            
            # Buscar funciones en eventos onclick, onload, etc.
            event_functions = re.findall(r'on\w+=["\']([^"\']*)["\']', content)
            for event_func in event_functions:
                if '(' in event_func:
                    func_name = event_func.split('(')[0].strip()
                    if func_name and func_name not in [f['name'].replace('()', '') for f in functions]:
                        functions.append({
                            'name': f"{func_name}()",
                            'desc': "Función de evento",
                            'line': 0
                        })
            
            return functions
            
        except Exception as e:
            print(f"Error extrayendo funciones: {str(e)}")
            return []

# Inicializar el sistema de ayuda
# Especifica aquí las carpetas donde están tus archivos HTML
HTML_DIRECTORIES = [
    'templates',
    'static',
    'templates/help/'
    # Agrega más carpetas según necesites
]

help_system = HelpSystemBackend(HTML_DIRECTORIES)
'''
@help_bp.route('/')
def index():
    """
    Página principal del sistema de ayuda
    """
    # Aquí renderizarías el HTML que creamos anteriormente
    # Por simplicidad, retornamos un mensaje
    return "help.html"
'''

@help_bp.route('/help')
def help_page():
    """
    Página de ayuda dinámica
    """
    # Aquí deberías servir el HTML del sistema de ayuda
    # Por ejemplo, podrías guardarlo como template y usar render_template
    return render_template('help.html')

@help_bp.route('/api/get-html-files')
def get_html_files():
    """
    API para obtener la estructura de archivos HTML
    """
    try:
        file_tree = help_system.scan_html_files()
        return jsonify(file_tree)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@help_bp.route('/api/get-file-content')
def get_file_content():
    """
    API para obtener el contenido de un archivo HTML
    """
    file_path = request.args.get('path')
    if not file_path:
        return jsonify({'error': 'Path requerido'}), 400
    
    try:
        content = help_system.get_file_content(file_path)
        return jsonify({'content': content})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@help_bp.route('/api/get-file-functions')
def get_file_functions():
    """
    API para obtener las funciones JavaScript de un archivo
    """
    file_path = request.args.get('path')
    if not file_path:
        return jsonify({'error': 'Path requerido'}), 400
    
    try:
        functions = help_system.extract_javascript_functions(file_path)
        return jsonify(functions)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@help_bp.route('/api/search-files')
def search_files():
    """
    API para buscar archivos por nombre
    """
    query = request.args.get('q', '').lower()
    if not query:
        return jsonify([])
    
    try:
        file_tree = help_system.scan_html_files()
        matches = []
        
        def search_recursive(tree, path=""):
            for name, item in tree.items():
                current_path = f"{path}/{name}" if path else name
                
                if item['type'] == 'file' and query in name.lower():
                    matches.append({
                        'name': name,
                        'path': item['path'],
                        'full_path': current_path
                    })
                elif item['type'] == 'folder':
                    search_recursive(item['children'], current_path)
        
        search_recursive(file_tree)
        return jsonify(matches)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
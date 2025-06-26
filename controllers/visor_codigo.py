from flask import Blueprint, render_template, jsonify, request
import os
import ast
import re
from pathlib import Path
import markdown
from pygments import highlight
from pygments.lexers import get_lexer_by_name, guess_lexer_for_filename
from pygments.formatters import HtmlFormatter
from pygments.util import ClassNotFound

visorcodigo_bp = Blueprint('visorcodigo_bp', __name__)

class FileSystemController:
    def __init__(self):
        self.ignored_files = {'.pyc', '.pyo', '__pycache__', '.git', '.gitignore', 
                             '.DS_Store', 'node_modules', '.env', '.venv', 'venv'}
        self.ignored_dirs = {'__pycache__', '.git', 'node_modules', '.env', '.venv', 'venv'}
        
    def set_ignored_patterns(self, files=None, dirs=None):
        """Configura archivos y directorios a ignorar"""
        if files:
            self.ignored_files.update(files)
        if dirs:
            self.ignored_dirs.update(dirs)
    
    def should_ignore(self, path):
        """Determina si un archivo o directorio debe ser ignorado"""
        name = os.path.basename(path)
        return name in self.ignored_files or name in self.ignored_dirs
    
    def get_file_tree(self, root_path):
        """Genera el árbol de directorios con archivos Python, HTML y Markdown"""
        if not os.path.exists(root_path):
            return {"error": "La ruta no existe"}
        
        def build_tree(path, name=""):
            if self.should_ignore(path):
                return None
                
            if os.path.isfile(path):
                ext = os.path.splitext(path)[1].lower()
                if ext in ['.py', '.html', '.htm', '.md', '.markdown']:
                    return {
                        "name": name or os.path.basename(path),
                        "type": "file",
                        "path": path,
                        "extension": ext
                    }
                return None
            
            elif os.path.isdir(path):
                children = []
                try:
                    for item in sorted(os.listdir(path)):
                        item_path = os.path.join(path, item)
                        child = build_tree(item_path, item)
                        if child:
                            children.append(child)
                except PermissionError:
                    return None
                
                if children:  # Solo incluir directorios que tengan archivos válidos
                    return {
                        "name": name or os.path.basename(path),
                        "type": "directory",
                        "path": path,
                        "children": children
                    }
            
            return None
        
        tree = build_tree(root_path)
        return tree if tree else {"error": "No se encontraron archivos válidos"}
    
    def extract_python_functions(self, file_path):
        """Extrae funciones y clases de un archivo Python"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            tree = ast.parse(content)
            functions = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    # Extraer docstring si existe
                    docstring = ast.get_docstring(node)
                    
                    # Extraer parámetros
                    params = []
                    for arg in node.args.args:
                        params.append(arg.arg)
                    
                    functions.append({
                        "name": node.name,
                        "type": "function",
                        "line": node.lineno,
                        "params": params,
                        "docstring": docstring,
                        "is_private": node.name.startswith('_')
                    })
                
                elif isinstance(node, ast.ClassDef):
                    # Extraer métodos de la clase
                    methods = []
                    for item in node.body:
                        if isinstance(item, ast.FunctionDef):
                            method_params = []
                            for arg in item.args.args:
                                method_params.append(arg.arg)
                            
                            methods.append({
                                "name": item.name,
                                "params": method_params,
                                "line": item.lineno,
                                "docstring": ast.get_docstring(item),
                                "is_private": item.name.startswith('_')
                            })
                    
                    functions.append({
                        "name": node.name,
                        "type": "class",
                        "line": node.lineno,
                        "docstring": ast.get_docstring(node),
                        "methods": methods,
                        "is_private": node.name.startswith('_')
                    })
            
            return functions
        
        except Exception as e:
            return [{"error": f"Error al analizar el archivo: {str(e)}"}]
    
    def extract_html_functions(self, file_path):
        """Extrae funciones JavaScript de un archivo HTML"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Buscar funciones JavaScript en el HTML
            js_functions = []
            
            # Patrón para funciones JavaScript
            function_pattern = r'function\s+(\w+)\s*\([^)]*\)\s*{'
            matches = re.finditer(function_pattern, content, re.IGNORECASE)
            
            for match in matches:
                js_functions.append({
                    "name": match.group(1),
                    "type": "javascript_function",
                    "line": content[:match.start()].count('\n') + 1
                })
            
            # Buscar funciones arrow
            arrow_pattern = r'(?:const|let|var)\s+(\w+)\s*=\s*\([^)]*\)\s*=>'
            matches = re.finditer(arrow_pattern, content, re.IGNORECASE)
            
            for match in matches:
                js_functions.append({
                    "name": match.group(1),
                    "type": "javascript_arrow_function",
                    "line": content[:match.start()].count('\n') + 1
                })
            
            return js_functions
        
        except Exception as e:
            return [{"error": f"Error al analizar el archivo HTML: {str(e)}"}]
    
    def get_file_content(self, file_path):
        """Obtiene el contenido de un archivo con syntax highlighting"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            ext = os.path.splitext(file_path)[1].lower()
            
            if ext == '.md' or ext == '.markdown':
                # Convertir Markdown a HTML
                html_content = markdown.markdown(content, extensions=['codehilite', 'fenced_code'])
                return {
                    "content": html_content,
                    "type": "markdown",
                    "raw_content": content
                }
            else:
                # Aplicar syntax highlighting
                try:
                    lexer = guess_lexer_for_filename(file_path, content)
                except ClassNotFound:
                    if ext == '.py':
                        lexer = get_lexer_by_name('python')
                    elif ext in ['.html', '.htm']:
                        lexer = get_lexer_by_name('html')
                    else:
                        lexer = get_lexer_by_name('text')
                
                formatter = HtmlFormatter(
                    style='github-dark',
                    linenos=True,
                    cssclass='highlight',
                    linenostart=1
                )
                
                highlighted_content = highlight(content, lexer, formatter)
                
                return {
                    "content": highlighted_content,
                    "type": "code",
                    "raw_content": content,
                    "css": formatter.get_style_defs('.highlight')
                }
        
        except Exception as e:
            return {"error": f"Error al leer el archivo: {str(e)}"}

# Instancia del controlador
fs_controller = FileSystemController()

@visorcodigo_bp.route('/visorcodigo')
def index():
    """Página principal"""
    return render_template('visor_codigo.html')

@visorcodigo_bp.route('/api/configure', methods=['POST'])
def configure_ignored():
    """Configura archivos y directorios a ignorar"""
    data = request.get_json()
    ignored_files = data.get('ignored_files', [])
    ignored_dirs = data.get('ignored_dirs', [])
    
    fs_controller.set_ignored_patterns(ignored_files, ignored_dirs)
    
    return jsonify({"status": "success", "message": "Configuración actualizada"})

@visorcodigo_bp.route('/api/tree')
def get_tree():
    """Obtiene el árbol de directorios"""
    root_path = request.args.get('path', '.')
    tree = fs_controller.get_file_tree(root_path)
    return jsonify(tree)

@visorcodigo_bp.route('/api/file/<path:file_path>')
def get_file(file_path):
    """Obtiene el contenido de un archivo"""
    content = fs_controller.get_file_content(file_path)
    return jsonify(content)

@visorcodigo_bp.route('/api/functions/<path:file_path>')
def get_functions(file_path):
    """Obtiene las funciones de un archivo"""
    ext = os.path.splitext(file_path)[1].lower()
    
    if ext == '.py':
        functions = fs_controller.extract_python_functions(file_path)
    elif ext in ['.html', '.htm']:
        functions = fs_controller.extract_html_functions(file_path)
    elif ext in ['.md', '.markdown']:
        functions = []  # Los archivos markdown no tienen funciones
    else:
        functions = []
    
    return jsonify(functions)
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
    def __init__(self, project_root=None, allowed_folders=None):
        self.ignored_files = {'.pyc', '.pyo', '__pycache__', '.git', '.gitignore', 
                             '.DS_Store', 'node_modules', '.env', '.venv', 'venv'}
        self.ignored_dirs = {'__pycache__', '.git', 'node_modules', '.env', '.venv', 'venv'}
        
        # Configuración de seguridad
        self.project_root = os.path.abspath(project_root) if project_root else os.getcwd()
        self.allowed_folders = set(allowed_folders) if allowed_folders else set()
        
        # Extensiones de archivo soportadas
        self.supported_extensions = {'.py', '.html', '.htm', '.md', '.markdown', '.js', '.css', '.json', '.xml', '.yml', '.yaml', '.txt'}
        
    def set_project_root(self, root_path):
        """Establece la raíz del proyecto"""
        self.project_root = os.path.abspath(root_path)
    
    def set_allowed_folders(self, folders):
        """Configura las carpetas permitidas dentro del proyecto"""
        self.allowed_folders = set(folders)
    
    def set_ignored_patterns(self, files=None, dirs=None):
        """Configura archivos y directorios a ignorar"""
        if files:
            self.ignored_files.update(files)
        if dirs:
            self.ignored_dirs.update(dirs)
    
    def is_path_allowed(self, path):
        """Verifica si la ruta está dentro del proyecto y carpetas permitidas"""
        abs_path = os.path.abspath(path)
        
        # Verificar que esté dentro del proyecto
        if not abs_path.startswith(self.project_root):
            return False
        
        # Si no hay carpetas permitidas específicas, permitir todo dentro del proyecto
        if not self.allowed_folders:
            return True
        
        # Verificar si está en una carpeta permitida
        relative_path = os.path.relpath(abs_path, self.project_root)
        path_parts = Path(relative_path).parts
        
        # Si es la raíz del proyecto, permitir
        if relative_path == '.':
            return True
        
        # Verificar si alguna parte del path está en las carpetas permitidas
        for allowed_folder in self.allowed_folders:
            if path_parts[0] == allowed_folder or any(part == allowed_folder for part in path_parts):
                return True
        
        return False
    
    def should_ignore(self, path):
        """Determina si un archivo o directorio debe ser ignorado"""
        name = os.path.basename(path)
        return name in self.ignored_files or name in self.ignored_dirs
    
    def get_file_tree(self, root_path=None):
        """Genera el árbol de directorios con archivos soportados - CARPETAS PRIMERO"""
        if root_path is None:
            root_path = self.project_root
        
        abs_root = os.path.abspath(root_path)
        
        # Verificar que la ruta esté permitida
        if not self.is_path_allowed(abs_root):
            return {"error": "Acceso denegado: ruta fuera del proyecto o carpetas permitidas"}
        
        if not os.path.exists(abs_root):
            return {"error": "La ruta no existe"}
        
        def build_tree(path, name=""):
            if not self.is_path_allowed(path) or self.should_ignore(path):
                return None
                
            if os.path.isfile(path):
                ext = os.path.splitext(path)[1].lower()
                if ext in self.supported_extensions:
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
                    # Obtener todos los elementos del directorio
                    items = os.listdir(path)
                    
                    # Separar directorios y archivos
                    directories = []
                    files = []
                    
                    for item in items:
                        item_path = os.path.join(path, item)
                        if os.path.isdir(item_path):
                            directories.append(item)
                        else:
                            files.append(item)
                    
                    # Ordenar directorios y archivos por separado
                    directories.sort()
                    files.sort()
                    
                    # Procesar directorios primero
                    for directory in directories:
                        item_path = os.path.join(path, directory)
                        child = build_tree(item_path, directory)
                        if child:
                            children.append(child)
                    
                    # Procesar archivos después
                    for file in files:
                        item_path = os.path.join(path, file)
                        child = build_tree(item_path, file)
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
        
        tree = build_tree(abs_root)
        return tree if tree else {"error": "No se encontraron archivos válidos"}
    
    def extract_python_functions(self, file_path):
        """Extrae funciones, clases, variables globales y decoradores de un archivo Python"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            tree = ast.parse(content)
            elements = []
            
            # Variables globales
            for node in ast.walk(tree):
                if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name):
                    # Solo considerar asignaciones en el nivel superior
                    if hasattr(node, 'col_offset') and node.col_offset == 0:
                        var_name = node.targets[0].id
                        if not var_name.startswith('_'):  # Evitar variables privadas por defecto
                            elements.append({
                                "name": var_name,
                                "type": "variable",
                                "line": node.lineno,
                                "is_private": var_name.startswith('_')
                            })
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    # Extraer docstring si existe
                    docstring = ast.get_docstring(node)
                    
                    # Extraer parámetros
                    params = []
                    for arg in node.args.args:
                        params.append(arg.arg)
                    
                    # Extraer decoradores
                    decorators = []
                    for decorator in node.decorator_list:
                        if isinstance(decorator, ast.Name):
                            decorators.append(decorator.id)
                        elif isinstance(decorator, ast.Attribute):
                            decorators.append(f"{decorator.value.id}.{decorator.attr}")
                    
                    elements.append({
                        "name": node.name,
                        "type": "function",
                        "line": node.lineno,
                        "params": params,
                        "docstring": docstring,
                        "decorators": decorators,
                        "is_private": node.name.startswith('_'),
                        "is_async": isinstance(node, ast.AsyncFunctionDef)
                    })
                
                elif isinstance(node, ast.ClassDef):
                    # Extraer métodos de la clase
                    methods = []
                    for item in node.body:
                        if isinstance(item, ast.FunctionDef):
                            method_params = []
                            for arg in item.args.args:
                                method_params.append(arg.arg)
                            
                            method_decorators = []
                            for decorator in item.decorator_list:
                                if isinstance(decorator, ast.Name):
                                    method_decorators.append(decorator.id)
                                elif isinstance(decorator, ast.Attribute):
                                    method_decorators.append(f"{decorator.value.id}.{decorator.attr}")
                            
                            methods.append({
                                "name": item.name,
                                "params": method_params,
                                "line": item.lineno,
                                "docstring": ast.get_docstring(item),
                                "decorators": method_decorators,
                                "is_private": item.name.startswith('_'),
                                "is_async": isinstance(item, ast.AsyncFunctionDef)
                            })
                    
                    # Extraer decoradores de clase
                    class_decorators = []
                    for decorator in node.decorator_list:
                        if isinstance(decorator, ast.Name):
                            class_decorators.append(decorator.id)
                        elif isinstance(decorator, ast.Attribute):
                            class_decorators.append(f"{decorator.value.id}.{decorator.attr}")
                    
                    elements.append({
                        "name": node.name,
                        "type": "class",
                        "line": node.lineno,
                        "docstring": ast.get_docstring(node),
                        "methods": methods,
                        "decorators": class_decorators,
                        "is_private": node.name.startswith('_')
                    })
            
            return elements
        
        except Exception as e:
            return [{"error": f"Error al analizar el archivo Python: {str(e)}"}]
    
    def extract_javascript_functions(self, file_path):
        """Extrae funciones, clases, variables y objetos JavaScript de archivos .js o HTML"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            js_elements = []
            
            # Patrón para funciones JavaScript tradicionales
            function_pattern = r'function\s+(\w+)\s*\(([^)]*)\)\s*{'
            matches = re.finditer(function_pattern, content, re.IGNORECASE)
            
            for match in matches:
                params = [p.strip() for p in match.group(2).split(',') if p.strip()]
                js_elements.append({
                    "name": match.group(1),
                    "type": "function",
                    "params": params,
                    "line": content[:match.start()].count('\n') + 1
                })
            
            # Patrón para funciones arrow
            arrow_pattern = r'(?:const|let|var)\s+(\w+)\s*=\s*\(([^)]*)\)\s*=>'
            matches = re.finditer(arrow_pattern, content, re.IGNORECASE)
            
            for match in matches:
                params = [p.strip() for p in match.group(2).split(',') if p.strip()]
                js_elements.append({
                    "name": match.group(1),
                    "type": "arrow_function",
                    "params": params,
                    "line": content[:match.start()].count('\n') + 1
                })
            
            # Patrón para métodos de objetos
            method_pattern = r'(\w+)\s*:\s*function\s*\(([^)]*)\)\s*{'
            matches = re.finditer(method_pattern, content, re.IGNORECASE)
            
            for match in matches:
                params = [p.strip() for p in match.group(2).split(',') if p.strip()]
                js_elements.append({
                    "name": match.group(1),
                    "type": "method",
                    "params": params,
                    "line": content[:match.start()].count('\n') + 1
                })
            
            # Patrón para clases ES6
            class_pattern = r'class\s+(\w+)(?:\s+extends\s+(\w+))?\s*{'
            matches = re.finditer(class_pattern, content, re.IGNORECASE)
            
            for match in matches:
                js_elements.append({
                    "name": match.group(1),
                    "type": "class",
                    "extends": match.group(2) if match.group(2) else None,
                    "line": content[:match.start()].count('\n') + 1
                })
            
            # Patrón para variables globales (const, let, var)
            var_pattern = r'(?:const|let|var)\s+(\w+)\s*='
            matches = re.finditer(var_pattern, content, re.IGNORECASE)
            
            for match in matches:
                js_elements.append({
                    "name": match.group(1),
                    "type": "variable",
                    "line": content[:match.start()].count('\n') + 1
                })
            
            # Patrón para funciones async
            async_function_pattern = r'async\s+function\s+(\w+)\s*\(([^)]*)\)\s*{'
            matches = re.finditer(async_function_pattern, content, re.IGNORECASE)
            
            for match in matches:
                params = [p.strip() for p in match.group(2).split(',') if p.strip()]
                js_elements.append({
                    "name": match.group(1),
                    "type": "async_function",
                    "params": params,
                    "line": content[:match.start()].count('\n') + 1
                })
            
            # Patrón para event listeners
            event_pattern = r'addEventListener\s*\(\s*[\'"](\w+)[\'"]'
            matches = re.finditer(event_pattern, content, re.IGNORECASE)
            
            for match in matches:
                js_elements.append({
                    "name": f"Event: {match.group(1)}",
                    "type": "event_listener",
                    "line": content[:match.start()].count('\n') + 1
                })
            
            return js_elements
        
        except Exception as e:
            return [{"error": f"Error al analizar el archivo JavaScript: {str(e)}"}]
    
    def extract_css_selectors(self, file_path):
        """Extrae selectores CSS, media queries, keyframes y variables de archivos .css"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            css_elements = []
            
            # Patrón para selectores CSS
            selector_pattern = r'([.#]?[\w-]+(?:\s*[>+~]\s*[\w-]+)*(?:\s*:\s*[\w-]+)?)\s*{'
            matches = re.finditer(selector_pattern, content, re.MULTILINE)
            
            for match in matches:
                selector = match.group(1).strip()
                if selector and not selector.startswith('@'):
                    css_elements.append({
                        "name": selector,
                        "type": "selector",
                        "line": content[:match.start()].count('\n') + 1
                    })
            
            # Patrón para media queries
            media_pattern = r'@media\s+([^{]+)\s*{'
            matches = re.finditer(media_pattern, content, re.IGNORECASE)
            
            for match in matches:
                css_elements.append({
                    "name": f"@media {match.group(1).strip()}",
                    "type": "media_query",
                    "line": content[:match.start()].count('\n') + 1
                })
            
            # Patrón para keyframes
            keyframes_pattern = r'@keyframes\s+(\w+)\s*{'
            matches = re.finditer(keyframes_pattern, content, re.IGNORECASE)
            
            for match in matches:
                css_elements.append({
                    "name": match.group(1),
                    "type": "keyframe",
                    "line": content[:match.start()].count('\n') + 1
                })
            
            # Patrón para variables CSS (custom properties)
            css_var_pattern = r'(--[\w-]+)\s*:'
            matches = re.finditer(css_var_pattern, content, re.IGNORECASE)
            
            for match in matches:
                css_elements.append({
                    "name": match.group(1),
                    "type": "css_variable",
                    "line": content[:match.start()].count('\n') + 1
                })
            
            # Patrón para imports
            import_pattern = r'@import\s+[\'"]([^\'\"]+)[\'"]'
            matches = re.finditer(import_pattern, content, re.IGNORECASE)
            
            for match in matches:
                css_elements.append({
                    "name": f"Import: {match.group(1)}",
                    "type": "import",
                    "line": content[:match.start()].count('\n') + 1
                })
            
            return css_elements
        
        except Exception as e:
            return [{"error": f"Error al analizar el archivo CSS: {str(e)}"}]
    
    def extract_html_elements(self, file_path):
        """Extrae elementos HTML importantes como scripts, estilos, forms, etc."""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            html_elements = []
            
            # Patrón para elementos con ID
            id_pattern = r'<(\w+)[^>]*\s+id\s*=\s*[\'"]([^\'"]+)[\'"]'
            matches = re.finditer(id_pattern, content, re.IGNORECASE)
            
            for match in matches:
                html_elements.append({
                    "name": f"#{match.group(2)} ({match.group(1)})",
                    "type": "element_id",
                    "line": content[:match.start()].count('\n') + 1
                })
            
            # Patrón para elementos con clase
            class_pattern = r'<(\w+)[^>]*\s+class\s*=\s*[\'"]([^\'"]+)[\'"]'
            matches = re.finditer(class_pattern, content, re.IGNORECASE)
            
            for match in matches:
                classes = match.group(2).split()
                for cls in classes:
                    html_elements.append({
                        "name": f".{cls} ({match.group(1)})",
                        "type": "element_class",
                        "line": content[:match.start()].count('\n') + 1
                    })
            
            # Patrón para formularios
            form_pattern = r'<form[^>]*>'
            matches = re.finditer(form_pattern, content, re.IGNORECASE)
            
            for match in matches:
                html_elements.append({
                    "name": "Form",
                    "type": "form",
                    "line": content[:match.start()].count('\n') + 1
                })
            
            # Patrón para scripts
            script_pattern = r'<script[^>]*(?:\s+src\s*=\s*[\'"]([^\'"]+)[\'"])?'
            matches = re.finditer(script_pattern, content, re.IGNORECASE)
            
            for match in matches:
                src = match.group(1) if match.group(1) else "inline"
                html_elements.append({
                    "name": f"Script: {src}",
                    "type": "script",
                    "line": content[:match.start()].count('\n') + 1
                })
            
            return html_elements
        
        except Exception as e:
            return [{"error": f"Error al analizar el archivo HTML: {str(e)}"}]
    
    def extract_markdown_elements(self, file_path):
        """Extrae headers, links e imágenes de archivos Markdown"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            md_elements = []
            
            # Patrón para headers
            header_pattern = r'^(#{1,6})\s+(.+)$'
            matches = re.finditer(header_pattern, content, re.MULTILINE)
            
            for match in matches:
                level = len(match.group(1))
                html_elements.append({
                    "name": match.group(2).strip(),
                    "type": f"header_h{level}",
                    "line": content[:match.start()].count('\n') + 1
                })
            
            # Patrón para links
            link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
            matches = re.finditer(link_pattern, content)
            
            for match in matches:
                md_elements.append({
                    "name": f"Link: {match.group(1)}",
                    "type": "link",
                    "url": match.group(2),
                    "line": content[:match.start()].count('\n') + 1
                })
            
            # Patrón para imágenes
            image_pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
            matches = re.finditer(image_pattern, content)
            
            for match in matches:
                md_elements.append({
                    "name": f"Image: {match.group(1) or 'No alt text'}",
                    "type": "image",
                    "url": match.group(2),
                    "line": content[:match.start()].count('\n') + 1
                })
            
            return md_elements
        
        except Exception as e:
            return [{"error": f"Error al analizar el archivo Markdown: {str(e)}"}]
    
    def get_file_content(self, file_path):
        """Obtiene el contenido de un archivo con syntax highlighting"""
        # Verificar que el archivo esté permitido
        if not self.is_path_allowed(file_path):
            return {"error": "Acceso denegado: archivo fuera del proyecto o carpetas permitidas"}
        
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
                    elif ext == '.js':
                        lexer = get_lexer_by_name('javascript')
                    elif ext == '.css':
                        lexer = get_lexer_by_name('css')
                    elif ext == '.json':
                        lexer = get_lexer_by_name('json')
                    elif ext in ['.yml', '.yaml']:
                        lexer = get_lexer_by_name('yaml')
                    elif ext == '.xml':
                        lexer = get_lexer_by_name('xml')
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

# Instancia del controlador - CONFIGURA AQUÍ TU PROYECTO
fs_controller = FileSystemController(
    project_root="./",  # Cambia esta ruta
    allowed_folders=["controllers", "templates", "static", "config", "app.py", "README.md"]  # Cambia estas carpetas
)

@visorcodigo_bp.route('/visorcodigo')
def index():
    """Página principal"""
    return render_template('visor_codigo.html')

@visorcodigo_bp.route('/api/configure', methods=['POST'])
def configure_system():
    """Configura el sistema de archivos"""
    data = request.get_json()
    
    # Configurar archivos y directorios ignorados
    ignored_files = data.get('ignored_files', [])
    ignored_dirs = data.get('ignored_dirs', [])
    fs_controller.set_ignored_patterns(ignored_files, ignored_dirs)
    
    # Configurar carpetas permitidas
    allowed_folders = data.get('allowed_folders', [])
    if allowed_folders:
        fs_controller.set_allowed_folders(allowed_folders)
    
    # Configurar raíz del proyecto
    project_root = data.get('project_root')
    if project_root:
        fs_controller.set_project_root(project_root)
    
    return jsonify({"status": "success", "message": "Configuración actualizada"})

@visorcodigo_bp.route('/api/tree')
def get_tree():
    """Obtiene el árbol de directorios"""
    path = request.args.get('path')
    tree = fs_controller.get_file_tree(path)
    return jsonify(tree)

@visorcodigo_bp.route('/api/file/<path:file_path>')
def get_file(file_path):
    """Obtiene el contenido de un archivo"""
    content = fs_controller.get_file_content(file_path)
    return jsonify(content)

@visorcodigo_bp.route('/api/functions/<path:file_path>')
def get_functions(file_path):
    """Obtiene las funciones/elementos de un archivo según su tipo"""
    # Verificar que el archivo esté permitido
    if not fs_controller.is_path_allowed(file_path):
        return jsonify({"error": "Acceso denegado"})
    
    ext = os.path.splitext(file_path)[1].lower()
    
    if ext == '.py':
        elements = fs_controller.extract_python_functions(file_path)
    elif ext == '.js':
        elements = fs_controller.extract_javascript_functions(file_path)
    elif ext in ['.html', '.htm']:
        # Para HTML, combinar elementos HTML y JavaScript
        html_elements = fs_controller.extract_html_elements(file_path)
        js_elements = fs_controller.extract_javascript_functions(file_path)
        elements = html_elements + js_elements
    elif ext == '.css':
        elements = fs_controller.extract_css_selectors(file_path)
    elif ext in ['.md', '.markdown']:
        elements = fs_controller.extract_markdown_elements(file_path)
    elif ext == '.json':
        elements = []  # JSON no tiene funciones per se
    elif ext in ['.yml', '.yaml', '.xml', '.txt']:
        elements = []  # Estos formatos no tienen elementos extraíbles
    else:
        elements = []
    
    return jsonify(elements)

@visorcodigo_bp.route('/api/project-info')
def get_project_info():
    """Obtiene información del proyecto configurado"""
    return jsonify({
        "project_root": fs_controller.project_root,
        "allowed_folders": list(fs_controller.allowed_folders),
        "supported_extensions": list(fs_controller.supported_extensions),
        "ignored_files": list(fs_controller.ignored_files),
        "ignored_dirs": list(fs_controller.ignored_dirs)
    })
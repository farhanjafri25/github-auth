import os
from tree_sitter import Language, Parser


Language.build_library('build/python.so', ['tree-sitter-python'])
PY_LANGUAGE = Language('build/python.so', 'python')

    
def get_function_and_class_details(node, code, file_name, class_name=None):
    if node.type == 'function_definition':
        function_name = node.child_by_field_name('name').text.decode('utf-8')
        function_start = node.start_byte
        function_end = node.end_byte
        function_code = code[function_start:function_end].decode('utf-8')
        return {
            "function_name": function_name,
            "class_name": class_name,
            "code": function_code,
            "file_name": file_name
        }
    elif node.type == 'class_definition':
        class_name = node.child_by_field_name('name').text.decode('utf-8')
    
    functions = []
    for child in node.children:
        result = get_function_and_class_details(child, code, file_name, class_name)
        if result:
            functions.append(result)
    return functions



def parse_codebase(repo_path: str):
    parser = Parser()
    parser.set_language(PY_LANGUAGE)
    
    metadata = []
    
    for root, _, files in os.walk(repo_path):
        for file in files:
            if file.endswith(".py"):
                print('File Name', file)
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    code = f.read()
                    tree = parser.parse(bytes(code, "utf8"))
                    root_node = tree.root_node
                    functions = get_function_and_class_details(root_node, bytes(code, 'utf8'), file)
                    metadata.extend(functions)
    return metadata




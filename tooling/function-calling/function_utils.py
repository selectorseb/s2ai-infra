# function_utils.py

import json
import os
import inspect
from typing import get_type_hints
import importlib.util

def python_type_to_schema_type(python_type):
    """Map Python type hints to schema-compatible type strings."""
    # Adjusted to handle both type objects directly and their names as strings
    type_mapping = {
        'str': "string",
        'int': "integer",
        'float': "number",
        'bool': "boolean",
        'list': "array",
        'dict': "object",
        'Any': "any"  # Adjust as needed for handling 'Any' or unspecified types
    }
    # If the input is a type object, get its name; otherwise, assume it's already a string
    type_name = python_type.__name__ if not isinstance(python_type, str) else python_type
    return type_mapping.get(type_name, "any")

def function_to_metadata(func):
    """Generate metadata from a function, including correct type representation."""
    sig = inspect.signature(func)
    type_hints = get_type_hints(func)

    parameters = {}
    required = []
    for name, param in sig.parameters.items():
        # Use the __name__ attribute of the type hint for direct types,
        # adjust if handling more complex types like Union, Optional, etc.
        param_type = type_hints.get(name, type(None))
        # Ensure we get just the type name if it's a direct type
        schema_type = python_type_to_schema_type(param_type.__name__ if hasattr(param_type, '__name__') else param_type)

        param_info = {"type": schema_type}
        # Additional handling as before
        parameters[name] = param_info
        if param.default is inspect.Parameter.empty:
            required.append(name)
        else:
            param_info['default'] = param.default

    # Handling for return type
    return_type = sig.return_annotation
    schema_return_type = python_type_to_schema_type(return_type.__name__ if hasattr(return_type, '__name__') else return_type)

    metadata = {
        "type": "function",
        "function": {
            "name": func.__name__,
            "description": func.__doc__.strip(),
            "parameters": {
                "type": "object",
                "properties": parameters,
                "required": required
            },
            "returns": schema_return_type
        }
    }

    return metadata

# # TEST: Generate and print metadata for the get_function function
# metadata_json = function_to_metadata(get_function)
# print(metadata_json)

def prepare_function_tools(functions_directory='functions'):
    """
    Scan all Python files in the functions directory, generate metadata for each,
    and compile this into a tools.json file.
    """
    functions_directory_full_path = os.path.join(os.getcwd(), functions_directory)
    function_files = [f for f in os.listdir(functions_directory_full_path) if f.endswith('.py') and f != '__init__.py']
    tools = []

    if not function_files:
        print("No functions found.")
        return

    for filename in function_files:
        # Build the path to the function file
        file_path = os.path.join(functions_directory_full_path, filename)
        module_name = filename[:-3]  # Remove '.py' extension
        
        # Import the module from the given file path
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        for name, obj in inspect.getmembers(module, inspect.isfunction):
            # Filter out functions not meant for metadata generation if necessary
            # Generate and append the metadata
            tools.append(function_to_metadata(obj))

    # Write the tools list to tools.json in the current working directory
    tools_json_path = os.path.join(os.getcwd(), functions_directory, 'tools.json')
    with open(tools_json_path, 'w') as f:
        json.dump(tools, f, indent=4)

    print("Function tools.json generated.")

if __name__ == "__main__":
    prepare_function_tools()
import os
import importlib.util


def get_all_worlds():
    world_classes = []

    current_dir = os.path.dirname(__file__)

    for filename in os.listdir(current_dir):
        if filename.endswith('.py') and filename not in ('__init__.py', 'handle_worlds.py'):
            module_name = os.path.splitext(filename)[0]
            module_path = os.path.join(current_dir, filename)

            spec = importlib.util.spec_from_file_location(module_name, module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            if hasattr(module, 'World'):
                world_classes.append([module_name.replace('.py', ''), module.World])

    return world_classes

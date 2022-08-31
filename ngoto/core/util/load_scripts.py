import importlib
import os


def load_scripts(folder: str) -> None:
    """ Loads all py files in folder as classes except init files,
        returns list of instansiated obj """
    files = []
    files_paths = []
    for c in os.listdir(folder):
        if c.endswith('.py') and not c.startswith('__'):
            files_paths.append(c)
    for files_path in files_paths:
        module = folder.replace('/', '.') + '.' + files_path[:-3]
        mod = importlib.import_module(module)
        # get module name from path and capitalize
        # first letter to get class name
        module_name = module.split(".")[2]
        class_ = getattr(mod, module_name[0].upper() + module_name[1:])
        files.append(class_())
    return files
import importlib
import os


def _load_from_folder(folder: str) -> list:
    """ Loads all py files in folder as classes except init files,
        returns list of instansiated obj"""
    files = []
    # get command file paths
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


def test_command_names():
    """Test there are no conflicting command names"""
    commands = _load_from_folder('ngoto/commands')
    command_names = []
    for command in commands:
        command_names.append(command.get_name())
    result = len(command_names) == len(set(command_names))
    assert result
    return result

from ngoto.core.clt import CLT


# recursive function to get all plugins from node
def get_all_plugins(node):
    plugins = []
    for plugin in node.get_plugins():
        plugins.append(plugin)
    for child in node.get_children():
        plugins += get_all_plugins(child)
    return plugins


def test_plugin_dup_name():
    """
        Check there are no duplicate plugin names
    """
    ngotoCLT = CLT()
    # get list of all plugin names
    plugins = get_all_plugins(ngotoCLT.curr_pos)
    names = []
    for plugin in plugins:
        names.append(plugin.name)
    # check for duplicates
    if len(names) == len(set(names)):
        assert True
    else:
        duplicates = []
        for name in names:
            if names.count(name) > 1:
                duplicates.append(name)
        print('Duplicate plugins found: ' + str(duplicates))
        assert False

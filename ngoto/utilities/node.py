
class Node:
    def __init__(self, name):
        self.name = name
        self.children = [] # list of children nodes
        self.plugins = [] # List Plugin objs
        self.parent = None # Parent node

    def __str__(self):
        return self.name

    @property
    def num_children(self): 
        return len(self.children)
    @property
    def num_plugins(self):
        return len(self.children)

    def add_child(self, child):
        self.children.append(child)
    def get_children(self):
        return self.children
    def get_child(self, index):
        return self.children[index]

    def add_plugin(self, plugin):
        self.plugins.append(plugin)
    def get_plugins(self):
        return self.plugins
    def get_plugin(self, index):
        return self.plugins[index]

    def get_parent(self):
        return self.parent
    def set_parent(self, parent):
        self.parent = parent

    @property
    def is_parent(self):
        if self.children:
            return True
        return False
    @property
    def has_parent(self):
        if self.parent:
            return True
        return False


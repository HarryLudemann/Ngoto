# script contains class of node for plugins tree
class Node:
    def __init__(self, name):
        self.name = name
        self.children = [] # list of children nodes
        self.plugins = [] # List Plugin objs
        self.parent = None # Parent node

    def __str__(self):
        return self.name

    def add_child(self, child): # given Node obj
        self.children.append(child)
    def get_children(self) -> list:
        return self.children
    def get_child(self, index: int): # returns Node obj
        return self.children[index]

    def add_plugin(self, plugin): # given Plugin obj
        self.plugins.append(plugin)
    def get_plugins(self) -> list:
        return self.plugins
    def get_plugin(self, index): # returns Plugin obj
        return self.plugins[index]

    def get_parent(self):
        return self.parent # returns Node
    def set_parent(self, parent): # given Node
        self.parent = parent

    @property
    def is_parent(self) -> bool:
        if self.children:
            return True
        return False
    @property
    def has_parent(self) -> bool: 
        if self.parent:
            return True
        return False

    @property
    def num_children(self) -> int:
        return len(self.children)
    @property
    def num_plugins(self) -> int:
        return len(self.plugins)

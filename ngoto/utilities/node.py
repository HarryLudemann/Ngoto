
class Node:
    children = [] # list of children nodes
    plugin = None # Nodes plugin
    parent = None # Parent node

    def get_plugin_name(self):
        return self.plugin.get_name()

    def add_child(self, child):
        self.children.append(child)
    def get_children(self):
        return self.children
    def get_child(self, index):
        return self.children[index]

    def set_plugin(self, plugin):
        self.plugin = plugin
    def get_plugin(self):
        return self.plugin

    def get_parent(self):
        return self.parent
    def set_parent(self, parent):
        self.parent = parent

    def is_parent(self):
        if self.children:
            return True
        return False
    def is_root(self):
        if self.plugin == None:
            return True
        return False

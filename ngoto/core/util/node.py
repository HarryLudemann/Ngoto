# script contains class of node for plugins tree

class Node:
    """
    A abstract class used to represent a plugin node, this is used to display and navigate a tree
    of plugins in the clt version. 

    ...

    Attributes
    ----------
    name : str
        a formatted string with no spaces to represent the plugin node name
    children : list[Node]
        a list of children nodes
    plugins : list[Plugin]
        a list of plugins
    parent : Node
        the parent node of the current node
    Methods
    -------
    __str__() --> str
        returns the name of the node
    get_name() --> str
        returns the name of the node
    add_child(child: Node)
        adds a child node to the current node
    get_children() --> list[Node]
        returns the children of the current node
    get_child(index: int) --> Node
        returns the child at the given index
    add_plugin(plugin: Plugin)
        adds a plugin to the current node
    get_plugins() --> list[Plugin]
        returns the plugins of the current node
    get_plugin(index: int) --> Plugin
        returns the plugin at the given index
    get_parent() --> Node
        returns the parent of the current node
    set_parent(parent: Node)   
        sets the parent of the current node
    is_parent() --> bool
        returns True if the current node is a parent, False otherwise
    has_parent() --> bool
        returns True if the current node has a parent, False otherwise
    num_children() --> int
        returns the number of children of the current node
    num_plugins() --> int
        returns the number of plugins of the current node
    """
    def __init__(self, name):
        self.name = name
        self.children = [] # list of children nodes
        self.plugins = [] # List Plugin objs
        self.parent = None # Parent node

    def __str__(self) -> str:
        return self.name

    def get_name(self):
        return self.name

    def add_child(self, child) -> None: # given Node 
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

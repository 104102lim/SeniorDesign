class Node:
    def __init__(self, name, children, parent):
        self.children = children
        self.name = name
        self.parent = parent

    def __str__(self):
        return str(self.name)
from Node import Node
import AssociationFunctions as AF

class Tree:
    def __init__(self, rt, ti):
        self.root = Node(rt, [], None)
        leaves = self.getLeaves()
        while True:
            for l in leaves:
                children = AF.getChildren(l.name, ti)
                for c in children:
                    child = Node(c, [], l)
                    if not self.contains(child):
                        l.children.append(child)
            newLeaves = self.getLeaves()
            if newLeaves == leaves:
                break
            else:
                leaves = newLeaves

    def __str__(self):
        ret = ""
        nodes = [self.root]
        while len(nodes) > 0:
            children = []
            for n in nodes:
                ret += (str(n) + " ")
                children += n.children
            ret += "\n"
            nodes = children.copy()
        return ret

    def contains(self, node):
        return self.containsHelper(node, self.root)

    def containsHelper(self, node1, node2):
        if node1.name == node2.name:
            return True
        else:
            ret = False
            for c in node2.children:
                ret = ret or self.containsHelper(node1, c)
            return ret

    def getLeaves(self):
        return self.getLeavesHelper(self.root)

    def getLeavesHelper(self, node):
        if len(node.children) == 0:
            return [node]
        else:
            ret = []
            for c in node.children:
                ret += self.getLeavesHelper(c)
            return ret

    def getPathToRoot(self, node):
        if node == None:
            return []
        ret = [node]
        return ret + self.getPathToRoot(node.parent)

    def getPathsToAncestor(self, nodes):
        paths = {}
        for n in nodes:
            paths[n] = self.getPathToRoot(n)
        ancestor = self.root
        for n in paths[nodes[0]]:
            exists = True
            for p in paths:
                if n not in paths[p]:
                    exists = False
            if exists:
                ancestor = n
                break
        lessPaths = {}
        for p in paths:
            lessPath = []
            for n in paths[p]:
                lessPath.append(n)
                if n == ancestor:
                    break
            lessPaths[p] = lessPath.copy()
        return lessPaths

    def onkeysSQL(self, ti, left, right):
        PK = ti[1][right]
        SQL = "("
        for k in range(len(PK)):
            if k == 0:
                SQL += (left + "." + PK[k] + "=" + right + "." + PK[k])
            else:
                SQL += (" AND " + left + "." + PK[k] + "=" + right + "." + PK[k])
        SQL += ") "
        return SQL

    def getNodeHelper(self, table, node):
        if str(node) == table:
            return node
        elif node.children is None:
            return None
        else:
            for c in node.children:
                ret = self.getNodeHelper(table, c)
                if ret is not None:
                    return ret
            return None

    def getNode(self, table):
        return self.getNodeHelper(table, self.root)

    def writeSQL(self, ti, tables):
        nodes = []
        for t in tables:
            nodes.append(self.getNode(t))
        paths = self.getPathsToAncestor(nodes)
        SQL = "SELECT * FROM "
        SQL += str(paths[nodes[0]][len(paths[nodes[0]]) - 1])
        SQL += " "
        for p in paths:
            for n in reversed(range(len(paths[p]) - 1)):
                SQL += ("LEFT JOIN " + str(paths[p][n]) + " ON ")
                SQL += self.onkeysSQL(ti, str(paths[p][n].parent), str(paths[p][n]))
        return SQL
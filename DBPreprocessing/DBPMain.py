import pyodbc
import pandas as pd
import EnumerateDescriptions as ED

GETPRIMARYKEYSQLCODE = "SELECT Col.Column_Name from " +  \
                           "INFORMATION_SCHEMA.TABLE_CONSTRAINTS Tab, " +  \
                           "INFORMATION_SCHEMA.CONSTRAINT_COLUMN_USAGE Col " +  \
                       "WHERE " +  \
                           "Col.Constraint_Name = Tab.Constraint_Name " +  \
                           "AND Col.Table_Name = Tab.Table_Name " +  \
                           "AND Constraint_Type = 'PRIMARY KEY' " +  \
                           "AND Col.Table_Name = '"

GETFOREIGNKEYSQLCODE = GETPRIMARYKEYSQLCODE.replace("PRIMARY KEY", "FOREIGN KEY")

GETFEATURESSQLCODE = "SELECT COLUMN_NAME " +  \
                     "FROM INFORMATION_SCHEMA.COLUMNS " +  \
                     "WHERE TABLE_NAME = '"

#connect to sql server
def connect():
    cnxn = pyodbc.connect("DRIVER={SQL Server}; SERVER=MYPC\SQLEXPRESS; DATABASE=BHBackupRestore; UID = SQLDummy; PWD = bushdid9/11")
    cursor = cnxn.cursor()
    return cursor

def getTableNames():
    tbNamesDf = pd.read_csv('FilteredDictionary.csv')
    tableNames = []
    for index, row in tbNamesDf.iterrows():
        tableNames.append(row[0])
    return tableNames

# gets features, FKs, PKs, etc...
def getTableInfo(tableNames, cursor, sqlCode):
    infoListByName = {}
    for name in tableNames:
        cursor.execute(sqlCode + name + "'")
        rawInfo = cursor.fetchall()
        infoInList = []
        for k in rawInfo:
            infoInList.append(k[0])
        infoListByName[name] = infoInList
    return infoListByName

def getValidDescriptions():
    namesFrame = ED.getValidNamesFrame(connect(), getTableNames())
    names = []
    for i in range(len(namesFrame.index)):
        names.append(namesFrame["feat_description"][i])
    return names

def printTable(name, ti):
    print("Name: " + name + " PK: " + str(ti[1][name]) + " FKs: " +
          str(ti[2][name]))


###############################################
# returns true if child's PK is in parent's FKs
def relationHolds(child, parent, ti):
    if child == parent:
        return False
    #accounts for the BHAC cycles
    if "BHAC_IDENTIFIER" in ti[1][child] and "BHAC_IDENTIFIER" in ti[1][parent]:
        return False
    matches = 0
    PK = ti[1][child]
    FK = ti[2][parent]
    for p in PK:
        for f in FK:
            if p == f:
                matches += 1
    return matches == len(PK)

def getParents(name, ti):
    parents = []
    for n in ti[0]:
        if relationHolds(name, n, ti):
            parents.append(n)
    return parents

def getChildren(name, ti):
    children = []
    for n in ti[0]:
        if relationHolds(n, name, ti):
            children.append(n)
    return children

def getRootParents(ti):
    roots = []
    for name in ti[0]:
        if len(getParents(name, ti)) == 0:
            roots.append(name)
    return roots

def getData(trees, features, chosen, ti, cursor):

    bestTree = trees[0]  #decide which tree is best if one exists
    cursor.execute(bestTree.writeSQL)
    #transform into dataframe and return


###############################################
class Node:
    def __init__(self, name, children, parent):
        self.children = children
        self.name = name
        self.parent = parent

    def __str__(self):
        return str(self.name)

class Tree:
    def __init__(self, rt, ti):
        self.root = Node(rt, [], None)
        leaves = self.getLeaves()
        while True:
            for l in leaves:
                children = getChildren(l.name, ti)
                for c in children:
                    child = Node(c, [], l)
                    if not self.contains(child):
                        l.children.append(child)
            newLeaves = self.getLeaves()
            if newLeaves == leaves:
                break
            else:
                leaves = newLeaves

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
            if exists == True:
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

    def writeSQL(self, ti):
        return

########## main ##########
if __name__ == "__main__":
    cursor = connect()
    tableNames = getTableNames()
    PKs = getTableInfo(tableNames, cursor, GETPRIMARYKEYSQLCODE)
    FKs = getTableInfo(tableNames, cursor, GETFOREIGNKEYSQLCODE)
    ti = {}
    ti[0] = tableNames
    ti[1] = PKs
    ti[2] = FKs
    roots = getRootParents(ti)
    trees = []
    for r in roots:
        trees.append(Tree(r, ti))
    features = ED.getValidNamesFrame(cursor, tableNames)
    chosen = ???
    data = getData(trees, features, chosen, ti, cursor)


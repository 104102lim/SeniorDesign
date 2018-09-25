import pyodbc
import pandas as pd
import os
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

class Tree:
    def __init__(self, root):
        self.root = root

    def contains(self, node):
        return self.containsHelper(node, self.root)

    def containsHelper(self, node1, node2):
        if node1.name == node2.name:
            return True
        else:
            ret = False
            for c in node2.children:
                ret = ret or self.containsHelper(node1, c)

    def getLeaves(self):
        return self.getLeavesHelper(self, self.root)

    def getLeavesHelper(self, node):
        if len(node.children) == 0:
            return [node]
        else:
            ret = []
            for c in node.children:
                ret += self.getLeavesHelper(c)
            return ret

    def __str__(self):
        return

    def findCommonAncestor(self, nodes):
        return

    def getAncestorTree(self, nodes):
        return
        #use findCommonAncestor

    def writeSQL(self, ti):
        return

class Node:
    def __init__(self, name, children, parent):
        self.children = children
        self.name = name
        self.parent = parent

    def __str__(self):
        return


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

def makeTree(rt, ti):
    tree = Tree(Node(rt, [], None))
    leaves = tree.getLeaves()
    while True:
        for l in leaves:
            children = getChildren(l.name, ti)
            for c in children:
                child = Node(c, [], l)
                if not tree.contains(child):
                    l.children.append(child)
        newLeaves = tree.getLeaves()
        if newLeaves == leaves:
            break
        else:
            leaves = newLeaves
    return tree

def getData(trees, features, ti, cursor):
    newTrees = []
    for t in trees:
        newTrees.append(t.getAncestorTree(features))
    bestTree = trees[0]  #decide which tree is best if one exists
    cursor.execute(bestTree.writeSQL)
    #transform into dataframe and return

def getValidDescriptions():
    namesFrame = ED.getValidNamesFrame(connect(), getTableNames())
    names = []
    for i in range(len(namesFrame.index)):
        names.append(namesFrame["feat_description"][i])
    return names











    def createComd(root, ti):
        included = []
        included.append(root)
        cmd = "SELECT * FROM " + root
        #lists of children indexed by parents
        children = {}
        children[root] = getChildren(root, ti)
        numChildren = len(children[root])
        while numChildren > 0:    # No no no lol
            newChildren = {}
            for p in children:
                for c in children[p]:
                    if c not in included:
                        included.append(c)
                        newChildren[c] = getChildren(c, ti)
                        # Potential problem with multi column keys
                        cmd += "\nFULL JOIN " + c + "\nON " + c + "." + ti[1][c][0] + \
                               "=" + p + "." + ti[1][c][0]
            children = newChildren
            numChildren = 0
            for p in children:
                numChildren += len(children[p])
        return cmd

    def getFrame(cmd, cursor):
        cursor.execute(cmd)
        raw = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        dictArr = []
        for row in raw:
            entry = {}
            for col in columns:
                entry[columns.index(col)] = row[columns.index(col)]
            dictArr.append(entry)
        frame = pd.DataFrame(dictArr)
        if len(frame.columns) == 0:
            for col in columns:
                frame[col] = [None]
        else:
            frame.columns = columns
        return frame

    def createOneTable(ti, cursor):
        roots = getRootParents(ti)
        cmds = {}
        frames = {}
        for r in roots:
            cmds[r] = createComd(r, ti)
            #frames[r] = getFrame(cmds[r], cursor)
        return cmds

    def printTable(name, ti):
        print("Name: " + name + " PK: " + str(ti[1][name]) + " FKs: " +
              str(ti[2][name]))

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
    descs = getValidDescriptions()
    for d in descs:
        print(d)
    print(len(descs))


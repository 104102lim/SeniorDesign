import pyodbc
import pandas as pd
import numpy as np

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

# returns true if child's PK is in parent's FKs
def relationHolds(child, parent, ti):
    if child == parent:
        return False
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

def getRootParents(ti):
    roots = []
    for name in ti[0]:
        if len(getParents(name, ti)) == 0:
            roots.append(name)
    return roots

def createOneTable(ti):
    roots = getRootParents(ti)
    cmds = {}
    for r in roots:
        cmds[r] = "SELECT * FROM " + r
    return roots

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
    roots = createOneTable(ti)
    for n1 in tableNames:
        if "BHAC_IDENTIFIER" in PKs[n1]:
            printTable(n1, ti)



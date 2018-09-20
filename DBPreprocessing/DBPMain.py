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

# returns true if PK matches FK
def relationHolds(child, parent, PKs, FKs):
    if child == parent:
        return False
    matches = 0
    tablePK = PKs[child]
    tableFK = FKs[parent]
    for p in tablePK:
        for f in tableFK:
            if p == f:
                matches += 1
    return (matches == len(tablePK))






#@@@@@@@@@@@SHOULD START AT ROOT AND END AT CHILDREN@@@@@@@@@@@@@@@@@@@

def getChildlessTable(tableNames, PKs, FKs):
    for name1 in tableNames:
        hasParent = False
        for name2 in tableNames:
            if relationHolds(name1, name2, PKs, FKs):
                hasParent = True
                break
        if hasParent == False:
            return name1
    return None

def getParents(name, tableNames, PKs, FKs):
    parents = []
    for n in tableNames:
        if relationHolds(name, n, PKs, FKs):
            parents.append(n)
    return parents

def joinTables(child, parent, PKs, FKs, SQL):
    return

def handleBHAC(tableNames, PKs, FKs, SQL):
    return

def createOneTable(tableNames, PKs, FKs):
    while True:
        child = getChildlessTable(tableNames, PKs, FKs)
        if child is None:
            SQL = handleBHAC(tableNames, PKs, FKs, SQL)

        parents = getParents(child, tableNames, PKs, FKs)
        if len(parents) == 0:
            termParents.append(child)
        else:
            for parent in parents:

########## main ##########
if __name__ == "__main__":
    cursor = connect()
    tableNames = getTableNames()
    PKs = getTableInfo(tableNames, cursor, GETPRIMARYKEYSQLCODE)
    FKs = getTableInfo(tableNames, cursor, GETFOREIGNKEYSQLCODE)


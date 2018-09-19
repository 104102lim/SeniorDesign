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

# gets featurese, FKs, PKs, etc...
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

# returns names of tables that contain tableName as a foreign table
def findParentTables(tableName, tablePK, FKs):
    parentNames = []
    for name, tableFK in FKs.items():
        if (tableName != name) and keyContains(tablePK, tableFK):
            parentNames.append(name)
    return parentNames

# returns true if PK matches FK
def keyContains(tablePK, tableFK):
    matches = 0
    for p in tablePK:
        for f in tableFK:
            if p == f:
                matches += 1
    return (matches == len(tablePK))

#This method is all wrong. Need to do DFS the other way where number of items preserved at each step is the cost of the step.
#DFS should start from terminal parents instead of end at terminal parents.
#returns dictionary indexed by table name with lists of paths from table to terminal parent 
def createPaths(tableNames, PKs, FKs):
    paths = {}
    for name in tableNames:
        pathGroup = []
        paths[name] = pathGroup
        directParents = findParentTables(name, PKs[name], FKs)
        if len(directParents) == 0:
            continue
        for parent in directParents:
            path = []
            path.append(parent)
            pathGroup.append(path)   
        pathsCompleted = False
        while not pathsCompleted:
            pathsToAdd = []
            pathToRemove = []
            for path in pathGroup:
                nextParents = findParentTables(path[len(path) - 1], PKs[path[len(path) - 1]], FKs)
                nextParentsHold = nextParents.copy()
                for parent in nextParentsHold:
                    if parent in path:
                       nextParents.remove(parent)
                if len(nextParents) != 0:
                    pathToRemove = path.copy()
                    for parent in nextParents:
                        addHold = path.copy()
                        addHold.append(parent)
                        pathsToAdd.append(addHold.copy())
                    break
            if (len(pathsToAdd) == 0) and (len(pathToRemove) == 0):
                pathsCompleted = True
            else:
                pathGroup.remove(pathToRemove)
                for path in pathsToAdd:
                    pathGroup.append(path.copy())
        paths[name] = pathGroup
    return paths

########## main ##########
if __name__ == "__main__":
    cursor = connect()
    tableNames = getTableNames()
    PKs = getTableInfo(tableNames, cursor, GETPRIMARYKEYSQLCODE)
    FKs = getTableInfo(tableNames, cursor, GETFOREIGNKEYSQLCODE)
    features = getTableInfo(tableNames, cursor, GETFEATURESSQLCODE)
    allPaths = createPaths(tableNames, PKs, FKs)
    print()

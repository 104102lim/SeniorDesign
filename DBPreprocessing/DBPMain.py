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

def findParentTables(tableName, tablePK, features):
    parentNames = []
    for name, featureList in features.items():
        if (tableName != name) and keyContains(tablePK, featureList):
            parentNames.append(name)
    return parentNames

def keyContains(key, featureList):
    matches = 0
    for k in key:
        for feature in featureList:
            if k == feature:
                matches += 1
    return (matches == len(key))

#returns dictionary indexed by table name with lists of paths from table to terminal parent 
def createPaths(tableNames, PKs, features):
    paths = {}
    for name in tableNames:
        pathGroup = []
        paths[name] = pathGroup
        #@@@@@@@@GIVES KEY ERROR CHECK THAT ORIGINAL TABLE IS NOT TERMINAL TABLE@@@@@@@@
        directParents = findParentTables(name, PKs[name], features)
        for parent in directParents:
            path = []
            path.append(parent)
            pathGroup.append(path)   
        pathsCompleted = False
        while not pathsCompleted:
            pathsToAdd = []
            pathToRemove = []
            for path in pathGroup:
                nextParents = findParentTables(path[len(path) - 1], PKs[len(path) - 1], features)
                if len(nextParents) != 0:
                    pathToRemove = path.copy()
                    for parent in nextParents:
                        pathsToAdd.apend(path.copy().append(parent))
                    break
            if (len(pathsToAdd) == 0) and (len(pathToRemove) == 0):
                pathsCompleted = True
            else:
                pathGroup.remove(pathToRemove)
                for path in pathsToAdd:
                    pathGroup.append(path)
        paths[name] = pathGroup
    return paths

########## main ##########
if __name__ == "__main__":
    cursor = connect()
    tableNames = getTableNames()
    PKs = getTableInfo(tableNames, cursor, GETPRIMARYKEYSQLCODE)
    features = getTableInfo(tableNames, cursor, GETFEATURESSQLCODE)
    print(createPaths(tableNames, PKs, features))
    
#    for name in tableNames:
#        print(findParentTables(name, PKs[name], features))
#        print()
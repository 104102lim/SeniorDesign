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

# returns true if PK matches FK
def keyContains(tablePK, tableFK):
    matches = 0
    for p in tablePK:
        for f in tableFK:
            if p == f:
                matches += 1
    return (matches == len(tablePK))

#TODO
def getChildlessTables(tableNames, PKs, FKs):
    childlessTables = []
    for name1 in tableNames:
        hasParent = False
        tablefks = FKs[name1]
        for name2 in tableNames:
            tablepk = PKs[name2]
            if keyContains(tablepk, tablefks) and name1 != name2:
                hasParent = True
                break
        if hasParent == False:
            childlessTables.append(name1)
    return childlessTables

########## main ##########
if __name__ == "__main__":
    cursor = connect()
    tableNames = getTableNames()
    PKs = getTableInfo(tableNames, cursor, GETPRIMARYKEYSQLCODE)
    FKs = getTableInfo(tableNames, cursor, GETFOREIGNKEYSQLCODE)
    features = getTableInfo(tableNames, cursor, GETFEATURESSQLCODE)
    while True:    
        childlessTables = getChildlessTables(tableNames, PKs, FKs)
        if len(childlessTables) == 0:
            print(len(tableNames))
            print()
            for name in tableNames:
                print(name + " PKs: " + str(PKs[name]) + " FKs: " + str(FKs[name]))
            print()
            for name in tableNames:
                holdTN = tableNames.copy()
                holdFKs = FKs.copy()
                holdPKs = PKs.copy()
                holdTN.remove(name)
                holdFKs.pop(name)
                holdPKs.pop(name)
                holdCT = getChildlessTables(holdTN, holdFKs, holdPKs)
                if len(holdCT) != 0:
                    print(name + " PKs: " + str(PKs[name]) + " FKs: " + str(FKs[name]))
                    print()
                    break
            break
        for name in childlessTables:
            tableNames.remove(name)
            PKs.pop(name)
            FKs.pop(name)


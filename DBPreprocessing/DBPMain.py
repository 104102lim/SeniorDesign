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

def getFrames(tableNames, cursor):
    frames = {}
    for name in tableNames:
        cursor.execute('SELECT * FROM [dbo].[' + name + ']');
        table = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        dictArr = []
        for row in table:
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
        frames[name] = frame
    return frames

def getKeys(tableNames, cursor):
    keys = {}
    for name in tableNames:
        cursor.execute("SELECT Col.Column_Name from " +  
                           "INFORMATION_SCHEMA.TABLE_CONSTRAINTS Tab, " +
                           "INFORMATION_SCHEMA.CONSTRAINT_COLUMN_USAGE Col " + 
                       "WHERE " +
                           "Col.Constraint_Name = Tab.Constraint_Name " +
                           "AND Col.Table_Name = Tab.Table_Name " + 
                           "AND Constraint_Type = 'PRIMARY KEY' " +
                           "AND Col.Table_Name = '" + name + "'")
        table = cursor.fetchall()
        tableKeys = []
        for key in table:
            tableKeys.append(key[0])
        keys[name] = tableKeys
    return keys

def getFeatures(tableNames, cursor):
    features = {}
    for name in tableNames:
        cursor.execute("SELECT COLUMN_NAME " +
                       "FROM INFORMATION_SCHEMA.COLUMNS " +
                       "WHERE TABLE_NAME = '" + name + "'")
        table = cursor.fetchall()
        tableFeatures = []
        for feature in table:
            tableFeatures.append(feature[0])
        features[name] = tableFeatures
    return features

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
    

########## main ##########
if __name__ == "__main__":
    cursor = connect()
    tableNames = getTableNames()
    PKs = getTableInfo(tableNames, cursor, GETPRIMARYKEYSQLCODE)
    features = getTableInfo(tableNames, cursor, GETFEATURESSQLCODE)
    print(PKs)
    print(features)

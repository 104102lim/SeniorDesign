import pyodbc
import pandas as pd
import numpy as np

def mergeFrames(frames, keys, framesToMerge):
    for mergeToIdx in range(1, len(framesToMerge)):
        mergeFromIdx = framesToMerge[0]
        #create new columns
        for col in frames[mergeFromIdx].columns.values:
            if col != keys[mergeFromIdx]:
                frames[mergeToIdx][col] = np.nan
                for idxTo in range(len(frames[mergeToIdx].index)):
                    for idxFrm in range(len(frames[mergeFromIdx].index)):
                        if frames[mergeToIdx].loc[idxTo][keys[mergeFromIdx]] == frames[mergeFromIdx].loc[idxFrm][keys[mergeFromIdx]]:
                            frames[mergeToIdx].set_value(idxTo, col, frames[mergeFromIdx].loc[idxFrm][col])
    del frames[mergeFromIdx]
    del keys[mergeFromIdx]
 
def idFramesToMerge(frames, keys):
    ret = []
    for idx in range(len(frames)): 
        commonKeys = []
        for col in list(frames[idx].columns.values):
            for key in keys:
                if key == col:
                    commonKeys.append(key)
        if len(commonKeys) == 1:
            frameWithOneKey = idx
            break
    ret.append(frameWithOneKey)

    for idx in range(len(frames)):
        for col in list(frames[idx].columns.values):
            if (col == commonKeys[0]) and (idx != ret[0]):
                ret.append(idx)
                break
    return ret
 
    

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
    frames = []
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
        frames.append(frame)
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

########## main ##########
if __name__ == "__main__":
    cursor = connect()
    tableNames = getTableNames()
    frames = getFrames(tableNames, cursor)
    keys = getKeys(tableNames, cursor)
    print(keys)


#while len(keys) > 1:
#    framesToMerge = idFramesToMerge(frames, keys)
#    mergeFrames(frames, keys, framesToMerge)  
#print(frames)
   


 
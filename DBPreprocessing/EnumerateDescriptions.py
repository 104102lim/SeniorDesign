#Indexed in dictionary by table name:
#    All features in the table
#    All paths from table to the origin
#    
#The common index for two or more tables will be the primary key of the first common ancestor between all tables

import pyodbc
import pandas as pd
from DBPMain import getTableNames

SQLCODEHEAD = "SELECT [class_name], [attr_name], [attr_descript] " + \
                "FROM [dbo].[DICTIONARY] " + \
                "WHERE ("
SQLCODETAIL = "AND attr_descript IS NOT NULL " + \
                  "AND attr_descript NOT LIKE 'Internal identifier for %' " + \
                  "AND attr_descript NOT LIKE 'Row timestamp' " + \
                  "AND attr_descript NOT LIKE 'Set of %' " + \
                  "AND attr_descript NOT LIKE 'Date/time row was updated' " + \
                  "AND attr_descript NOT LIKE 'Name of user who updated row' " + \
                  "AND attr_descript NOT LIKE 'Autotrak specific data'"        

cnxn = pyodbc.connect("DRIVER={SQL Server}; SERVER=MYPC\SQLEXPRESS; DATABASE=BHBackupRestore; UID = SQLDummy; PWD = bushdid9/11")
cursor = cnxn.cursor()
tableNames = getTableNames()
SQLCODE = SQLCODEHEAD
for name in tableNames:
    if tableNames.index(name) != (len(tableNames) - 1):    
        SQLCODE += "class_name = '" + name + "' OR \n" 
    else:
        SQLCODE += "class_name = '" + name + "') "
SQLCODE += SQLCODETAIL
print(SQLCODE)      
cursor.execute(SQLCODE)
table = cursor.fetchall()
columns = [column[0] for column in cursor.description]
dictArr = []
for row in table:
    entry = {}
    for col in columns:
        entry[columns.index(col)] = row[columns.index(col)]
        dictArr.append(entry)
frame = pd.DataFrame(dictArr)
print(frame)
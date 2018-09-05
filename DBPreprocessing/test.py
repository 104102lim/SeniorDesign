#Indexed in dictionary by table name:
#    All paths from table to the origin
#    All features in the table
#    
#The common index for two or more tables will be the primary key of the first common ancestor between all tables

import pyodbc

cnxn = pyodbc.connect("DRIVER={SQL Server}; SERVER=MYPC\SQLEXPRESS; DATABASE=BHBackupRestore; UID = SQLDummy; PWD = bushdid9/11")
cursor = cnxn.cursor()
cursor.execute("SELECT Col.Column_Name from " +  
                   "INFORMATION_SCHEMA.TABLE_CONSTRAINTS Tab, " +
                   "INFORMATION_SCHEMA.CONSTRAINT_COLUMN_USAGE Col " + 
                "WHERE " +
                        "Col.Constraint_Name = Tab.Constraint_Name " +
                        "AND Col.Table_Name = Tab.Table_Name " + 
                        "AND Constraint_Type = 'PRIMARY KEY' " +
                        "AND Col.Table_Name = 'ANNULUS' ")
table = cursor.fetchall()
print(table)
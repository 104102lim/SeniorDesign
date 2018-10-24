import pyodbc
import pandas as pd
from Tree import Tree
import EnumerateDescriptions as ED
import AssociationFunctions as AF
from TableNames import getTableNames

class Init:
    __GETPRIMARYKEYSQLCODE = "SELECT Col.Column_Name from " + \
                           "INFORMATION_SCHEMA.TABLE_CONSTRAINTS Tab, " + \
                           "INFORMATION_SCHEMA.CONSTRAINT_COLUMN_USAGE Col " + \
                           "WHERE " + \
                           "Col.Constraint_Name = Tab.Constraint_Name " + \
                           "AND Col.Table_Name = Tab.Table_Name " + \
                           "AND Constraint_Type = 'PRIMARY KEY' " + \
                           "AND Col.Table_Name = '"

    __GETFOREIGNKEYSQLCODE = __GETPRIMARYKEYSQLCODE.replace("PRIMARY KEY", "FOREIGN KEY")

    __GETFEATURESSQLCODE = "SELECT COLUMN_NAME " + \
                         "FROM INFORMATION_SCHEMA.COLUMNS " + \
                         "WHERE TABLE_NAME = '"

    cursor = None
    ti = None
    validDescriptions = None
    validDescriptionsRaw = None
    trees = None

    @classmethod
    def __connect(cls, server, port, dbName, UID, PWD):
        if port == "":
            try:
                cntstr = ("DRIVER={SQL Server}; SERVER=" + server + ";" +
                    " DATABASE=" + dbName + "; UID=" + UID + "; PWD=" + PWD)
                print(cntstr)
                cnxn = pyodbc.connect(cntstr)
            except pyodbc.Error as ex:
                pass
        else:
            cnxn = pyodbc.connect("DRIVER={SQL Server}; SERVER=" + server + "," + port + ";" +
                " DATABASE=" + dbName + "; UID= " + UID + "; PWD= " + PWD)
        cursor = cnxn.cursor()
        return cursor

    @classmethod
    # gets features, FKs, PKs, etc...
    def __getTableInfo(cls, sqlCode):
        infoListByName = {}
        for name in cls.ti[0]:
            cls.cursor.execute(sqlCode + name + "'")
            rawInfo = cls.cursor.fetchall()
            infoInList = []
            for k in rawInfo:
                infoInList.append(k[0])
            infoListByName[name] = infoInList
        return infoListByName

    @classmethod
    def __getValidDescriptions(cls):
        cls.validDescriptionsRaw = ED.getValidNamesFrame(cls.cursor, cls.ti[0])
        names = []
        for i in range(len(cls.validDescriptionsRaw.index)):
            names.append(cls.validDescriptionsRaw["feat_description"][i])
        return names

    @classmethod
    def init(cls, server, port, dbName, UID, PWD):
        cls.cursor = cls.__connect(server, port, dbName, UID, PWD)
        cls.ti = {}
        cls.ti[0] = getTableNames()
        cls.ti[1] = cls.__getTableInfo(cls.__GETPRIMARYKEYSQLCODE)
        cls.ti[2] = cls.__getTableInfo(cls.__GETFOREIGNKEYSQLCODE)
        cls.validDescriptions = cls.__getValidDescriptions()
        roots = AF.getRootParents(cls.ti)
        cls.trees = []
        for r in roots:
            cls.trees.append(Tree(r, cls.ti))
        return


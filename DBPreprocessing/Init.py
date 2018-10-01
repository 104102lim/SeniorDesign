import pyodbc
import pandas as pd
import Tree
import EnumerateDescriptions as ED
import AssociationFunctions as AF

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
    trees = None

    @classmethod
    def __connect(cls):
        cnxn = pyodbc.connect(
            "DRIVER={SQL Server}; SERVER=MYPC\SQLEXPRESS; DATABASE=BHBackupRestore; UID = SQLDummy; PWD = bushdid9/11")
        cursor = cnxn.cursor()
        return cursor

    @classmethod
    def __getTableNames(cls):
        tbNamesDf = pd.read_csv('FilteredDictionary.csv')
        tableNames = []
        for index, row in tbNamesDf.iterrows():
            tableNames.append(row[0])
        return tableNames

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
        namesFrame = ED.getValidNamesFrame(cls.cursor, cls.ti[0])
        names = []
        for i in range(len(namesFrame.index)):
            names.append(namesFrame["feat_description"][i])
        return names

    @classmethod
    def init(cls):
        cls.cursor = cls.__connect()
        tableNames = cls.__getTableNames()
        PKs = cls.__getTableInfo(cls.__GETPRIMARYKEYSQLCODE)
        FKs = cls.__getTableInfo(cls.__GETFOREIGNKEYSQLCODE)
        cls.ti = {}
        cls.ti[0] = tableNames
        cls.ti[1] = PKs
        cls.ti[2] = FKs
        cls.validDescriptions = cls.__getValidDescriptions()
        roots = AF.getRootParents()
        cls.trees = []
        for r in roots:
            cls.trees.append(Tree(r, cls.ti))


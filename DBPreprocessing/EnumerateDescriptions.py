import pandas as pd

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

def getValidNamesFrame(cursor, tableNames):
    SQLCODE = SQLCODEHEAD
    for name in tableNames:
        if tableNames.index(name) != (len(tableNames) - 1):
            SQLCODE += "class_name = '" + name + "' OR \n"
        else:
            SQLCODE += "class_name = '" + name + "') "
    SQLCODE += SQLCODETAIL
    cursor.execute(SQLCODE)
    table = cursor.fetchall()
    cols = [column[0] for column in cursor.description]
    dict = []
    toDrop = []
    for col in cols:
        entry = []
        for row in table:
            if row[cols.index(col)] in entry and col == 'attr_descript':
                toDrop.append(table.index(row))
            entry.append(row[cols.index(col)])
        dict.append(entry.copy())
    frame = pd.DataFrame(dict)
    frame = frame.T
    cols = ["table_name", "feature_name", "feat_description"]
    frame.columns = cols
    frame = frame.drop(0)
    for d in toDrop:
        frame = frame.drop(d)
    frame = frame.reset_index()
    return frame

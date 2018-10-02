# Call Init.init() before you call these! Preferable call it at the very start of the program

import pandas as pd
from Node import Node
from Init import Init

# Call this with a list of feature names (strings).
# If the features can be related, then a dataframe is returned
# Else, an error string is returned
def getData(features):
    # assign features to tables
    tables = []
    for f in features:
        set = Init.validDescriptionsRaw["table_name"].where(
            Init.validDescriptionsRaw["feat_description"] == f)
        set = set.dropna()
        tables.append(set.iloc[0])

    # find if all tables belong in a single tree, if not return error
    tree = None
    for tr in Init.trees:
        allBelong = True
        for tb in tables:
            if not tr.contains(Node(tb, None, None)):
                allBelong = False
        if allBelong:
            tree = tr
            break
    if tree == None:
        return "ERROR NO COMMON PARENT INDEX"

    # generate SQL to retrieve features from database
    SQL = tree.writeSQL(Init.ti)
    Init.cursor.execute(SQL)
    data = Init.cursor.fetchall()
    cols = [column[0] for column in Init.cursor.description]

    # format result into dataframe

    return

# Call this to get a list valid feature descriptions
def getDescriptions():
    return Init.validDescriptions.copy()

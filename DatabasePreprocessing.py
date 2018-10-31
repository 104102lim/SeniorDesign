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
    feat_names = {}
    for f in features:
        set = Init.validDescriptionsRaw["table_name"].where(
            Init.validDescriptionsRaw["feat_description"] == f)
        set = set.dropna()
        tables.append(set.iloc[0])
        set = Init.validDescriptionsRaw["feature_name"].where(
            Init.validDescriptionsRaw["feat_description"] == f)
        set = set.dropna()
        feat_names[set.iloc[0]] = f

    indexedtables = tables.copy()
    tables = []
    for t in indexedtables:
        if t not in tables:
            tables.append(t)

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
        return "Analysis is impossible - data is not related"

    # generate SQL to retrieve features from database
    SQL = tree.writeSQL(Init.ti, tables)
    Init.cursor.execute(SQL)
    data = Init.cursor.fetchall()

    # format result into dataframe
    cols = [column[0] for column in Init.cursor.description]
    dict = {}
    for c in range(len(cols)):
        if cols[c] not in dict:
            dict[cols[c]] = []
            for row in data:
                dict[cols[c]].append(row[c])
    df = pd.DataFrame(dict)
    df = df[list(feat_names.keys())]
    goodColumns = []
    for c in df.columns:
        goodColumns.append(feat_names[c])
    df.columns = goodColumns
    return df

# Call this to get a list valid feature descriptions
def getDescriptions():
    return Init.validDescriptions.copy()

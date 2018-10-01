# Call Init.init() before you call these! Preferable call it at the very start of the program

import Node
import Init

def getData(features):
    # assign features to tables
    tables = []

    # find if all tables belong in a single tree, if not return error
    tree = None
    allBelong = None
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

def getDescriptions():
    return Init.validDescriptions.copy()

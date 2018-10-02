import pandas as pd
from time import time
from Init import Init
import DatabasePreprocessing as dp

server = "MYPC\SQLEXPRESS"
dbName = "BHBackupRestore"
UID = "SQLDummy"
PWD = "bushdid9/11"

server = "HEATHPC\SQLEXPRESS"
dbName = "newBackupTest"
UID = "SQLDummy"
PWD = "bushdid9/11"

def printTable(name, ti):
    print("Name: " + name + " PK: " + str(ti[1][name]) + " FKs: " +
          str(ti[2][name]))

########## main ##########
if __name__ == "__main__":
    start = time()
    Init.init(server, dbName, UID, PWD)
    end = time()
    print(end - start)

    Init.validDescriptionsRaw.to_csv('valid_features.csv')

    # features = []
    # features.append(Init.validDescriptions[3])
    # features.append(Init.validDescriptions[6])
    # data = dp.getData(features)


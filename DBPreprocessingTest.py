import pandas as pd
from time import time
from Init import Init
import DatabasePreprocessing as dp

LAPTOP = True

serverL = "MYPC\SQLEXPRESS"
dbNameL = "BHBackupRestore"
UIDL = "SQLDummy"
PWDL = "bushdid9/11"

serverP = "HEATHPC\SQLEXPRESS"
dbNameP = "newBackupTest"
UIDP = "SQLDummy"
PWDP = "bushdid9/11"

def printTable(name, ti):
    print("Name: " + name + " PK: " + str(ti[1][name]) + " FKs: " +
          str(ti[2][name]))

########## main ##########
if __name__ == "__main__":
    start = time()
    if LAPTOP:
        Init.init(serverL, dbNameL, UIDL, PWDL)
    else:
        Init.init(serverP, dbNameP, UIDP, PWDP)
    end = time()
    print(Init.ti[1])
    print(end - start)


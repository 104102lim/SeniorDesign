import pandas as pd
import Init

def printTable(name, ti):
    print("Name: " + name + " PK: " + str(ti[1][name]) + " FKs: " +
          str(ti[2][name]))

########## main ##########
if __name__ == "__main__":
    Init.init()


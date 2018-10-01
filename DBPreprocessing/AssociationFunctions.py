# returns true if child's PK is in parent's FKs
def relationHolds(child, parent, ti):
    if child == parent:
        return False
    #accounts for the BHAC cycles
    if "BHAC_IDENTIFIER" in ti[1][child] and "BHAC_IDENTIFIER" in ti[1][parent]:
        return False
    matches = 0
    PK = ti[1][child]
    FK = ti[2][parent]
    for p in PK:
        for f in FK:
            if p == f:
                matches += 1
    return matches == len(PK)

def getParents(name, ti):
    parents = []
    for n in ti[0]:
        if relationHolds(name, n, ti):
            parents.append(n)
    return parents

def getChildren(name, ti):
    children = []
    for n in ti[0]:
        if relationHolds(n, name, ti):
            children.append(n)
    return children

def getRootParents(ti):
    roots = []
    for name in ti[0]:
        if len(getParents(name, ti)) == 0:
            roots.append(name)
    return roots
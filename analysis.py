import math

fns = {} # Table of functions, defined by user
debug = True # Set to true to enable debugging options

def listAssign(index,lst,item):
    """Assigns item to lst at index, returns result."""
    lst[index] = item
    return lst

def listInsert(index,lst,item):
    """Inserts item to lst at index, returns result."""
    if index == 'end':
        lst.append(item)
        return lst
    else:
        lst.insert(index,item)
        return lst

def listSurgery(f,indices,lst,*args):
    """Does f at depth with *args in lst, using each successive item in indices as the index of the next lowest list. Returns result."""
    if len(indices) == 1:
        return f(indices[0],lst,*args)
    else:
        sublist = lst
        for index in indices[:-1]:
            sublist = sublist[index]
        sublist = f(indices[-1],sublist,*args)
        return listSurgery(listAssign,indices[:-1],lst,sublist)

def listAppendAtDepth(level,lst,item):
    """Appends item to list in end of lists in lst at depth level. Returns result."""
    return listSurgery(listInsert,[-1]*level+['end'],lst,item)

def listAddToLastItemAtDepth(level,lst,addend):
    """Adds addend to last item in lst at depth lvl. Returns result."""
    return listSurgery(lambda x,y,z:listAssign(x,y,y[x]+z),[-1]*(level+1),lst,addend)

def rankOperator(op):
    """Numerically ranks the level of an operator."""
    if debug:
        print "rankOperator("+str(op)+")"
    if op in ('+','-'):
        rank = 0
    elif op in ('*','/'):
        rank = 1
    elif op == '^':
        rank = 2
    elif op == '=':
        rank = 3
    else:
        rank = 4
    if debug:
        print "returned",rank
    return rank

def parseStringToList(s):
    """Parses an input string to an intermediate list."""
    for char in s:
        if char == ' ':
            s = s[1:]
        else:
            break
    for char in s[::-1]:
        if char == ' ':
            s = s[:-1]
        else:
            break
    l = [] # List that will eventually be returned
    charState = 0 # Tracks whether the last character was a separator (0), non-alphanumeric (1), number (2), or letter (3)
    level = 0 # Level in list at which to perform operations
    for char in s:
        if char == ' ':
            charState = 0
        elif char in ('(','[','{'):
            listAppendAtDepth(level,l,[])
            level += 1
            charState = 0
            listAppendAtDepth(level,l,char)
        elif char in (')',']','}'):
            listAppendAtDepth(level,l,char)
            level -= 1
            charState = 0
        elif not char.isalnum():
            if charState != 1:
                listAppendAtDepth(level,l,'')
            listAddToLastItemAtDepth(level,l,char)
            charState = 1
        else:
            if not charState in (2,3) or (char.isalpha() and charState == 2):
                listAppendAtDepth(level,l,'')
            listAddToLastItemAtDepth(level,l,char)
            if char.isalpha() or charState == 3:
                charState = 3
            else:
                charState = 2
    return l

def parseListToExpression(l):
    """Parses list from parseStringToList to an evaluatable expression. (UNDER CONSTRUCTION)"""
    lcopy = []
    hadOp = True # Tracks whether previous item was an operator (False for no and True for yes)
    for item in l:
        if isinstance(item,list):
            if item[0] == '[':
                if item[-1] == ']':
                    lcopy.append(item)
                    hadOp = False
                    continue
                else:
                    return Error # Error: mismatched parentheses
        if not hadOp and (isinstance(item,list) or item.isalnum()):
            lcopy.append('*')
        lcopy.append(item)
        if isinstance(item,list) or item.isalnum():
            hadOp = False
        else:
            hadOp = True
    l = lcopy
    del hadOp,lcopy
    print l
    e = [] # The list that will be the expression that will be returned
    lowestRank = 4 # The rank of the lowest-ranking operator in l
    opIndex =  0 # Index of lowest-ranking operator in l
    for item in enumerate(l):
        if rankOperator(item[1]) < lowestRank:
            lowestRank = rankOperator(item[1])
            opIndex = item[0]
    if lowestRank < 4:
        e = [l[opIndex],parseListToExpression(l[:opIndex]),parseListToExpression(l[opIndex+1:])]
    else:
        e = l
    return e

print "MAT (Michael's Analysis Tool), version 0.0.0\nAll rights reserved"
while True:
    expression = raw_input("> ")
    if expression == 'quit':
        break
    else:
        print parseListToExpression(parseStringToList(expression))

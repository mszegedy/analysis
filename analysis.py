import math
from arithmeticOperations import *

fns = {} # Table of functions, defined by user

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
    if op in ('=','<','>','<=','>=','->'):
        rank = 0
    elif op in ('+','-'):
        rank = 1
    elif op in ('*','/'):
        rank = 2
    elif op == '^':
        rank = 3
    else:
        rank = 4
    return rank

def isTerm(s):
    """Checks whether a string is a valid mathematical term."""
    result = True
    if not isinstance(s,list):
        for char in s:
            if not char.isalnum() and char != '.':
                result = False
    return result

def getListDepth(lst):
    """Returns the depth at which the deepest level of lst is."""
    depths = []
    for item in lst:
        if isinstance(item,(list,tuple)):
            depth = 1
            depth += getListDepth(item)
            depths.append(depth)
    try:
        return max(depths)
    except ValueError:
        return 0

def countListItemsByType(lst):
    """Returns a tuple, with the first item the number of floats in a list, the second item the number of strings in a list, and the third item the number of lists in a list."""
    count = [0,0,0]
    for item in lst:
        if isinstance(item,float):
            count[0] += 1
        elif isinstance(item,str):
            count[1] += 1
        elif isinstance(item,list):
            count[2] += 1
        else:
            pass
    return tuple(count)

def listSearchAndReplace(lst,x,y):
    """Returns lst with every x in it replaced by y."""
    result = []
    for item in lst:
        if item == x:
            result.append(y)
        elif isinstance(item,list):
            result.append(listSearchAndReplace(item))
        else:
            result.append(item)
    return result

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
    charState = 0 # Tracks whether the last character was a separator (0), non-alphanumeric (1), number or period (2), or letter (3)
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
        elif not char.isalnum() and char != '.':
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
    """Parses list from parseStringToList to an evaluatable expression."""
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
        if not hadOp and (isTerm(item)):
            lcopy.append('*')
        lcopy.append(item)
        if isTerm(item):
            hadOp = False
        else:
            hadOp = True
    l = lcopy
    del hadOp,lcopy
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
        if len(l) == 0:
            return Error # Error: too many operators in a row
        if len(l) == 1:
            e = l[0]
            if isinstance(e,list):
                if e[0] == '[':
                    return Error # Error: list of arguments without preceding operator
                elif e[0] == '(':
                    if e[-1] == ')':
                        e = parseListToExpression(e[1:-1])
                    else:
                        return Error # Error: mismatched parentheses
                elif e[0] == '{':
                    if e[-1] == '}':
                        e = ['{']
                        hadComma = True # Keeps track of whether last item processed was a comma
                        for index,item in enumerate(l[0][1:-1]):
                            if item == ',':
                                hadComma = True
                            else:
                                if hadComma:
                                    if index != 0:
                                        e[-1] = parseListToExpression(e[-1])
                                    e.append([])
                                e[-1].append(item)
                                hadComma = False
                        e[-1] = parseListToExpression(e[-1])
                    else:
                        return Error # Error: mismatched parentheses
                else:
                    return Error # Error: argument clause without operator
            elif isinstance(e,str):
                charCount = 0 # Counts the number of non-numeral chars in e
                hadAlpha = False # Keeps track of whether there has been a letter yet
                for char in e:
                    if char == '.':
                        charCount += 1
                    elif char.isalpha():
                        hadAlpha = True
                        charCount += 2
                    else:
                        pass
                if charCount <= 1:
                    e = float(e)
                else:
                    if hadAlpha:
                        pass
                    else:
                        return Error # Error: cannot have term consisting entirely out of numbers and periods
            else:
                return Error # Error: unknown error
        elif len(l) == 2:
            if isinstance(l[0],str) and isinstance(l[1],list) and l[1][0] == '[' and l[1][-1] == ']':
                charCount = 0 # Same as above
                hadAlpha = False
                for char in l[0]:
                    if char == '.':
                        charCount += 1
                    elif char.isalpha():
                        hadAlpha = True
                        charCount += 2
                    else:
                        pass
                if charCount <= 1:
                    return Error # Error: cannot have numbers as function names
                else:
                    if not hadAlpha:
                        return Error # Error: cannot have function name consisting entirely out of numbers and periods
                    e.append(l[0])
                    hadComma = True # Tracks whether last item parsed in l[1] was a comma or not
                    for index,item in enumerate(l[1][1:-1]):
                        if item == ',':
                            hadComma = True
                        else:
                            if hadComma:
                                if index != 0:
                                    e[-1] = parseListToExpression(e[-1])
                                e.append([])
                            e[-1].append(item)
                            hadComma = False
                    e[-1] = parseListToExpression(e[-1])
    return e

def evaluateExpression(l):
    if not isinstance(l,(list,tuple)):
        return l
    else:
        op = l[0]
        args = l[1:]
        if op == '=':
            if len(args) != 2:
                return Error # Error: an equal sign has two sides
            elif getListDepth(args[0]) == 0 and countListItemsByType(args[0])[1:] >= 1 and countListItemsByType(args[0])[1:] == (0,0):
                for num,arg in enumerate(args[0][1:]):
                    args[1] = listSearchAndReplace(args[1],arg,str(num))
                fns[args[0][0]] = args[1]
            else:
                return evaluateExpression(args[0]) == evaluateExpression(args[1])
        elif op == '+':
            if len(args) == 2:
                return Plus(evaluateExpression(args[0]),evaluateExpression(args[1]))
            else:
                return Error # Error: + has too many arguments
        else:
            try:
                result = fns[op]
                for index,item in args[1:]:
                    result = listSearchAndReplace(str(index),item)
                return evaluateExpression(result)
            except IndexError:
                return Error # Error: no such function

print "MAT (Michael's Analysis Tool), version 0.0.0\nAll rights reserved"
while True:
    expression = raw_input("> ")
    if expression == 'quit':
        break
    else:
        print evaluateExpression(parseListToExpression(parseStringToList(expression)))

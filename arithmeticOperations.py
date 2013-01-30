import math

def getCommutativeArgList(op,lst):
    """Takes commutative operation op and expression lst and returns a list of all the arguments in the top of the expression that are being opped together. Alternatively, if lst is not a list, it just returns lst."""
    if isinstance(lst,(list,tuple)):
        result = []
        if lst[0] == op:
            for item in lst[1:]:
                if isinstance(item,(lst,tuple)) and item[0] ==  op:
                    result += getCommutativeArgList(item)
                else:
                    result.append(item)
        return result
    else:
        return lst

def Add(x,y):
    """Adds two things together."""
    if isinstance(y,list) and y[0] == '-' and y[2] == x:
        return y[1]
    elif isinstance(x,list) and x[0] == '-' and x[2] == y:
        return x[1]
    elif x in (0,0.0):
        return y
    elif y in (0,0.0):
        return x
    elif y in (['*',-1.0,x],['*',x,-1.0]) or x in (['*',-1.0,y],['*',y,-1.0]):
        return 0.0
    elif isinstance(x,float) and isinstance(y,float):
        return x+y
    elif isinstance(x,float) and isinstance(y,str):
        return ['+',x,y]
    elif isinstance(x,str) and isinstance(y,float):
        return Add(y,x)
    elif isinstance(x,str) and isinstance(y,str):
        if x == y:
            return ['*',2.0,x]
        else:
            return ['+',x,y]
    elif isinstance(x,float) and isinstance(y,list):
        if y[0] == '+':
            if isinstance(y[1],float):
                return Add(x+y[1],y[2])
            elif isinstance(y[2],float):
                return Add(x+y[2],y[1])
            else:
                return ['+',x,y]
        elif y[0] == '-':
            argslist = getCommutativeArgList('+',y[2])
            if isinstance(reduce(Add,argslist)[1],float):
                return ['-',Add(x/reduce(Add,argslist),y[1]),reduce(Add,argslist[1:])]
        elif y[0] == '{':
            return ['{']+[Add(x,i) for i in y[1:]]
        else:
            return ['+',x,y]
    elif isinstance(x,list) and isinstance(y,float):
        return Add(y,x)
    elif isinstance(x,str) and isinstance(y,list):
        if y[0] == '+':
            if y[1] == x:
                return Add(['*',2.0,x],y[2])
            elif y[2] == x:
                return Add(['*',2.0,x],y[1])
            else:
                return ['+',x,y]
        elif y[0] == '-':
            argslist = getCommutativeArgList('+',y[2])
            if x in argslist:
                argslist.remove(x)
                if len(argslist) > 0:
                    return ['-',y[1],reduce(Add,argslist)]
                else:
                    return y[1]
        elif y[0] == '*':
            if y[1] == x:
                return ['*',x,Add(y[1],1.0)]
            elif y[2] == x:
                return ['*',x,Add(y[2],1.0)]
            else:
                return ['+',x,y]
        elif y[0] == '{':
            return ['{']+[Add(x,i) for i in y[1:]]
        else:
            return ['+',x,y]
    elif isinstance(x,(list,tuple)) and isinstance(y,str):
        return Add(y,x)
    elif isinstance(x,(list,tuple)) and isinstance(y,(list,tuple)): # TO DO: minus expressions
        if x[0] == '+' and y[0] == '+':
            if isinstance(x[1],float):
                return Add(x[1],Add(y[1],Add(x[2],y[2])))
            elif isinstance(x[1],str):
                if isinstance(y[1],float):
                    return Add(y[1],Add(x[1],Add(x[2],y[2])))
                elif isinstance(y[2],float):
                    return Add(y[2],Add(x[1],Add(x[2],y[2])))
                else:
                    return Add(x[1],Add(y[1],Add(x[2],y[2])))
            else:
                if isinstance(x[2],(list,tuple)):
                    if (isinstance(y[1],(float,str)) or isinstance(y[1],(float,str))):
                        return Add(y,x)
                    else:
                        return Add(x[1],Add(x[2],Add(y[1],y[2])))
                else:
                    return Add(Add(x[2],x[1]),y)
        elif x[0] == '+' and y[0] == '*':
            argslistx == getCommutativeArgList('+',x)
            argslisty == getCommutativeArgList('*',y)
            ############### TO DO ##############
            return ['*',x,y]
        elif x[0] == '*' and y[0] == '+':
            return Add(y,x)
        elif x[0] == '*' and y[0] == '*':
            if x[1] == y[1]:
                return ['*',x[1],Add(x[2],y[2])]
            else:
                return ['+',x,y]
        elif x[0] == '{' and y[0] == '{':
            return ['+',x,y]
        else:
            return ['+',x,y]
    else:
        return ['+',x,y]
def AdditiveInverse(x):
    if isinstance(x,float):
        return -x
    elif x in (0,0.0):
        return 0.0
    elif isinstance(x,(list,tuple)):
        if x[0] == '-':
            if x[1] == x[2]:
                return 0.0
            else:
                return ['-',x[2],x[1]]
        else:
            return ['-',0,x]
    else:
        return ['-',0,x]
def Multiply(x,y):
    """Multiplies two things together."""
    if 0 in (x,y):
        return 0.0
    elif isinstance(y,list) and y[0] == '/' and y[2] == x:
        return y[1]
    elif isinstance(x,list) and x[0] == '/' and x[2] == y:
        return x[1]
    elif x in (1,1.0):
        return y
    elif y in (1,1.0):
        return x
    elif y in (['^',-1,x],['^',x,-1]) or x in (['^',-1,y],['^',y,-1]):
        return 1.0
    elif isinstance(x,float) and isinstance(y,float):
        return x*y
    elif isinstance(x,float) and isinstance(y,str):
        return ['*',x,y]
    elif isinstance(x,str) and isinstance(y,float):
        return Multiply(y,x)
    elif isinstance(x,str) and isinstance(y,str):
        if x == y:
            return ['^',x,2.0]
        else:
            return ['*',x,y]
    elif isinstance(x,float) and isinstance(y,list):
        if y[0] == '+':
            return Add(Multiply(x,y[1]),Multiply(x,y[2]))
        elif y[0] == '*':
            if isinstance(y[1],float):
                return Multiply(x*y[1],y[2])
            elif isinstance(y[2],float):
                return Multiply(x*y[2],y[1])
            else:
                return ['*',x,y]
        elif y[0] == '/':
            argslist = getCommutativeArgList('*',y[2])
            if isinstance(reduce(Multiply,argslist)[1],float):
                return ['/',Multiply(x/reduce(Multiply,argslist),y[1]),reduce(Multiply,argslist[1:])]
        elif y[0] == '{':
            return ['{']+[Multiply(x,i) for i in y[1:]]
        else:
            return ['*',x,y]
    elif isinstance(x,list) and isinstance(y,float):
        return Multiply(y,x)
    elif isinstance(x,str) and isinstance(y,list):
        if y[0] == '+':
            return Add(Multiply(x,y[1]),Multiply(x,y[2]))
        elif y[0] == '*':
            if y[1] == x:
                return Multiply(['^',x,2.0],y[2])
            elif y[2] == x:
                return Multiply(['^',x,2.0],y[1])
            else:
                return ['*',x,y]
        elif y[0] == '/':
            argslist = getCommutativeArgList(y[2])
            if x in argslist:
                argslist.remove(x)
                if len(argslist) > 0:
                    return ['/',y[1],reduce(Multiply,argslist)]
                else:
                    return y[1]
        elif y[0] == '^':
            if y[1] == x:
                return ['^',x,Add(y[1],1.0)]
            else:
                return ['*',x,y]
        elif y[0] == '{':
            return ['{']+[Multiply(x,i) for i in y[1:]]
        else:
            return ['*',x,y]
    elif isinstance(x,(list,tuple)) and isinstance(y,str):
        return Multiply(y,x)
    elif isinstance(x,(list,tuple)) and isinstance(y,(list,tuple)): ### TO DO: multiplying a multiplication expression with a fraction, multiplying a fraction with a fraction
        if x[0] == '+' and y[0] == '+':
            return Add(Multiply(Add(y[1],y[2]),x[1]),Multiply(Add(y[1],y[2]),x[2]))
        if x[0] == '+' and y[0] == '*':
            return Add(Multiply(x[1],y),Multiply(x[2],y))
        if x[0] == '*' and y[0] == '+':
            return Multiply(y,x)
        if x[0] == '*' and y[0] == '*':
            if isinstance(x[1],float):
                return Multiply(x[1],Multiply(y[1],Multiply(x[2],y[2])))
            elif isinstance(x[1],str):
                if isinstance(y[1],float):
                    return Multiply(y[1],Multiply(x[1],Multiply(x[2],y[2])))
                elif isinstance(y[2],float):
                    return Multiply(y[2],Multiply(x[1],Multiply(x[2],y[2])))
                else:
                    return Multiply(x[1],Multiply(y[1],Multiply(x[2],y[2])))
            else:
                if isinstance(x[2],(list,tuple)):
                    if (isinstance(y[1],(float,str)) or isinstance(y[1],(float,str))):
                        return Multiply(y,x)
                    else:
                        return Multiply(x[1],Multiply(x[2],Multiply(y[1],y[2])))
                else:
                    return Multiply(Multiply(x[2],x[1]),y)
        elif x[0] == '*' and y[0] == '^':
            argslist == getCommutativeArgList(x)
            def f(a):
                if isinstance(a,(list,tuple)):
                    return a[0:2]
                else:
                    return a
            if y[1] in argslist or ['^',y[1]] in map(f,arglist):
                addend = 0
                for item in filter(lambda a:a==y[1],argslist):
                    addend += 1
                    argslist.remove(item)
                for item in filter(lambda a: True if isinstance(a,(list,tuple)) and a[1]==y[1] else False,argslist):
                    addend = Add(addend,item[2])
                    argslist.remove(item)
                return Multiply(reduce(Multiply,argslist),['^',y[1],Add(addend,y[2])])
            else:
                return ['*',x,y]
        elif x[0] == '^' and y[0] == '*':
            return Multiply(y,x)
        elif x[0] == '^' and y[0] == '^':
            if x[1] == y[1]:
                return ['^',x[1],Add(x[2],y[2])]
            else:
                return ['*',x,y]
        elif x[0] == '{' and y[0] == '{':
            return ['*',x,y]
        else:
            return ['*',x,y]
    else:
        return ['*',x,y]
def Reciprocal(x):
    """Takes the reciprocal of something."""
    if x in (0,0.0):
    	return Error # Error: division by zero
    elif isinstance(x,float):
        return 1.0/x
    elif isinstance(x,str):
        return ['/',1.0,x]
    elif isinstance(x,list):
        if x[0] == '/':
            return ['/',x[2],x[1]]
        elif x[0] == '{':
            return ['{']+[Reciprocal(i) for i in x[1:]]
        elif x[0] == 'Sin':
            return ['Csc',x[1]]
        elif x[0] == 'Cos':
            return ['Sec',x[1]]
        elif x[0] == 'Tan':
            return ['Cot',x[1]]
        elif x[0] == 'Csc':
            return ['Sin',x[1]]
        elif x[0] == 'Sec':
            return ['Cos',x[1]]
        elif x[0] == 'Cot':
            return ['Tan',x[1]]
        else:
            return ['/',1.0,x]
    else:
        return ['/',1.0,x]

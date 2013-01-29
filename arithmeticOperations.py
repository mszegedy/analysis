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
    if x == 0:
        return y
    elif y == 0:
        return x
    elif y in (['*',-1,x],['*',x,-1]) or x in (['*',-1,y],['*',y,-1]):
        return 0
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
                return ['+',x+y[1],y[2]]
            elif isinstance(y[2],float):
                return ['+',x+y[2],y[1]]
            else:
                return ['+',x,y]
        elif y[0] == '{':
            return ['{']+[Add(x,i) for i in y[1:]]
        else:
            return ['+',x,y]
    elif isinstance(x,list) and isinstance(y,float):
        return Add(y,x)
    elif isinstance(x,str) and isinstance(y,list):
        if y[0] == '+':
            if y[1] == x:
                return ['+',['*',2.0,x],y[2]]
            elif y[2] == x:
                return ['+',['*',2.0,x],y[1]]
            else:
                return ['+',x,y]
        elif y[0] == '*':
            if y[2] == x:
                return ['*',Add(y[1],1.0),x]
            elif y[1] == x:
                return ['*',Add(y[2],1.0),x]
            else:
                return ['+',x,y]
        elif y[0] == '{':
            return ['{']+[Add(x,i) for i in y[1:]]
        else:
            return ['+',x,y]
    elif isinstance(x,list) and isinstance(y,str):
        return Add(y,x)
    elif isinstance(x,list) and isinstance(y,(list,tuple)):
        if x[0] == '+' and y[0] == '+':
            recursive1 = Add(Add(x[1],y[1]),Add(x[2],y[2]))
            if isinstance(recursive1,list):
                if isinstance(recursive1[1],list) and isinstance(recursive1[2],list):
                    if recursive1[1][0] == '+' and recursive1[2][0] == '+':
                        recursive2 = Add(Add(recursive1[1][1],recursive1[2][1]),Add(recursive1[1][2],recursive1[2][2]))
                        return recursive2
                    else:
                        return recursive1
                else:
                    return recursive1
            else:
                return recursive1
        elif x[0] == '*' and y[0] == '*':
            if x[1] == y[1]:
                return ['*',Add(x[2],y[2]),x[1]]
            elif x[2] == y[2]:
                return ['*',Add(x[1],y[1]),x[2]]
            elif x[1] == y[2]:
                return ['*',Add(x[2],y[1]),x[1]]
            elif x[2] == y[1]:
                return ['*',Add(x[1],y[2]),x[2]]
            else:
                return ['+',x,y]
        elif x[0] == '/' and y[0] == '/':
            if x[2] == y[2]:
                return ['/',Add(x[1],y[1]),x[2]]
            else:
                return ['+',x,y]
        elif x[0] == '{' and y[0] == '{':
            return ['{']+[Add(a,b) for a,b in zip(x[1:],y[1:])]
        else:
            return ['+',x,y]
    else:
        return ['+',x,y]
def Multiply(x,y):
    """Multiplies two things together."""
    if 0 in (x,y):
        return 0.0
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
                return ['*',x*y[1],y[2]]
            elif isinstance(y[2],float):
                return ['*',x*y[2],y[1]]
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
                return ['*',['^',x,2.0],y[2]]
            elif y[2] == x:
                return ['*',['^',x,2.0],y[1]]
            else:
                return ['*',x,y]
        elif y[0] == '^':
            if y[1] == x:
                return ['^',x,Add(y[1],1.0)]
            else:
                return ['*',x,y]
        elif y[0] == '{':
            return ['{']+[Multiply(x,i) for i in y[1:]]
        else:
            return ['*',x,y]
    elif isinstance(x,list) and isinstance(y,str):
        return Multiply(y,x)
    elif isinstance(x,(list,tuple)) and isinstance(y,(list,tuple)):
        if x[0] == '*' and y[0] == '*':
            recursive1 = Multiply(Multiply(x[1],y[1]),Multiply(x[2],y[2]))
            if isinstance(recursive1,list):
                if isinstance(recursive1[1],list) and isinstance(recursive1[2],list):
                    if recursive1[1][0] == '+' and recursive1[2][0] == '+':
                        recursive2 = Multiply(Multiply(recursive1[1][1],recursive1[2][1]),Multiply(recursive1[1][2],recursive1[2][2]))
                        return recursive2
                    else:
                        return recursive1
                else:
                    return recursive1
            else:
                return recursive1
        elif x[0] == '^' and y[0] == '^':
            if x[1] == y[1]:
                return ['^',x[1],Add(x[2],y[2])]
            else:
                return ['*',x,y]
        elif x[0] == '{' and y[0] == '{':
            return ['*',x,y]
        else:
            return ['+',x,y]
    else:
        return ['+',x,y]
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

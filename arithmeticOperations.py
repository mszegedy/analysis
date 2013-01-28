import math

def Plus(x,y):
    if isinstance(x,float) and isinstance(y,float):
        return x+y
    elif isinstance(x,float) and isinstance(y,str):
        return ['+',x,y]
    elif isinstance(x,str) and isinstance(y,float):
        return ['+',y,x]
    elif isinstance(x,float) and isinstance(y,list):
        if y[0] == '+':
            if isinstance(y[1],float):
                return ['+',x+y[1],y[2]]
            elif isinstance(y[2],float):
                return ['+',x+y[2],y[1]]
            else:
                return ['+',x,y]
        else:
            return ['+',x,y]
    elif isinstance(x,list) and isinstance(y,float):
        if x[0] == '+':
            if isinstance(x[1],float):
                return ['+',y+x[1],x[2]]
            elif isinstance(x[2],float):
                return ['+',y+x[2],x[1]]
            else:
                return ['+',y,x]
        else:
            return ['+',y,x]
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
                return ['*',Plus(y[1],1.0),x]
            elif y[1] == x:
                return ['*',Plus(y[2],1.0),x]
            else:
                return ['+',x,y]
        else:
            return ['+',x,y]
    elif isinstance(x,list) and isinstance(y,str):
        if x[0] == '+':
            if x[1] == y:
                return ['+',['*',2.0,y],x[2]]
            elif x[2] == y:
                return ['+',['*',2.0,y],x[1]]
            else:
                return ['+',y,x]
        elif x[0] == '*':
            if x[2] == y:
                return ['*',Plus(x[1],1.0),y]
            elif x[1] == y:
                return ['*',Plus(x[2],1.0),y]
            else:
                return ['+',y,x]
        else:
            return ['+',y,x]
    elif isinstance(x,list) and isinstance(y,list):
        pass
    else:
        return ['+',x,y]

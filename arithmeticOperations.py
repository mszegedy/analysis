import math

# The places where 'pass' is written are the places where code still needs to be written!

def Plus(x,y):
    """Adds two things together."""
    if isinstance(x,float) and isinstance(y,float):
        return x+y
    elif isinstance(x,float) and isinstance(y,str):
        return ['+',x,y]
    elif isinstance(x,str) and isinstance(y,float):
        return ['+',y,x]
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
        elif y[0] == '{': # }
            return ['{']+[Plus(x,i) for i in y[1:]] # }
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
        elif x[0] == '{': # }
            return ['{']+[Plus(y,i) for i in x[1:]] # }
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
        elif y[0] == '{': # }
            return ['{']+[Plus(x,i) for i in y[1:]] # }
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
        elif x[0] == '{': # }
            return ['{']+[Plus(y,i) for i in x[1:]] # }
        else:
            return ['+',y,x]
    elif isinstance(x,list) and isinstance(y,list):
        if x[0] == '{' and y[0] == '{': # }}
            return ['{']+[Plus(a,b) for a,b in zip(x[1:],y[1:])]
    else:
        return ['+',x,y]
def Times(x,y):
    """Multiplies two things together."""
    if isinstance(x,float) and isinstance(y,float):
        return x*y
    elif isinstance(x,float) and isinstance(y,str):
        return ['*',x,y]
    elif isinstance(x,str) and isinstance(y,float):
        return ['*',y,x]
    elif isinstance(x,float) and isinstance(y,list):
        pass
    elif isinstance(x,list) and isinstance(y,float):
        pass
    elif isinstance(x,str) and isinstance(y,list):
        pass
    elif isinstance(x,list) and isinstance(y,str):
        pass
    elif isinstance(x,list) and isinstance(y,list):
        pass
    else:
        return ['*',x,y]
def Reciprocal(x):
    """Takes the reciprocal of something."""
    if isinstance(x,float):
        return 1.0/x
    elif isinstance(x,str):
        return ['/',1.0,x]
    elif isinstance(x,list):
        if x[0] == '/':
            return ['/',x[2],x[1]]
        elif x[0] == '{': # }
            return ['{']+[Reciprocal(i) for i in x[1:]] # }
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
            return ['Cot',x[1]]
        else:
            return ['/',1.0,x]
    else:
        return ['/',1.0,x]

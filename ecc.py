#!/usr/bin/env python3

# KRY - 2. projekt
# Autor: Hana Slamova (xslamo00)


import sys

class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

Fp = 0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff
a = -0x3
b = 0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b
basePoint = Point(  x=0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296,
                    y=0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5)


# Tato funkce byla převzata z:https://www.johannes-bauer.com/compsci/ecc/
# Online [10.4.2019]
def eea(i, j):
    assert(isinstance(i, int))
    assert(isinstance(j, int))
    (s, t, u, v) = (1, 0, 0, 1)
    while j != 0:
        (q, r) = (i // j, i % j)
        (unew, vnew) = (s, t)
        s = u - (q * s)
        t = v - (q * t)
        (i, j) = (j, r)
        (u, v) = (unew, vnew)
    (d, m, n) = (i, u, v)
    return (d, m, n)

# Tato funkce byla převzata z:https://www.johannes-bauer.com/compsci/ecc/
# Online [10.4.2019]
def multiply(i, j):
    n = i
    r = 0
    for bit in range(j.bit_length()):
        if (j & (1 << bit)):
            r = (r + n) % Fp
        n = (n + n) % Fp
    return r

# Tato funkce byla převzata z:https://www.johannes-bauer.com/compsci/ecc/
# Online [10.4.2019]
def exponentiate(i, j):
    n = i
    r = 1
    for bit in range(j.bit_length()):
        if (j & (1 << bit)):
            r = multiply(r, n)
        n = multiply(n, n)
    return r

####################################################
# MODULAR ARITHMETIC                               #
####################################################
def Add(a,b):
    if a + b < Fp:
        return a + b
    else:
        return a + b - Fp

def Sub(a,b):
    if a - b >= 0:
        return a - b
    else:
        return a - b + Fp

def Mult(a,b):
    return multiply(a,b)

def Div(a,b):
    return (a*eea(Fp,b)[1])%Fp

def Exp(a,exponent):
    return exponentiate(a,exponent)
####################################################

# P+Q
def add(P:Point, Q:Point):
    alphaNumerator = Sub(Q.y,P.y)
    alphaDenominator = Sub(Q.x,P.x)
    alpha = Div(alphaNumerator,alphaDenominator)

    R = Point(0,0)
    R.x = Sub(Sub(Exp(alpha,2),P.x),Q.x)
    R.y = Sub(Mult(alpha,Sub(P.x,R.x)),P.y)
    return R

# P+P
def addSame(P:Point):
    alphaNumerator = Add(Mult(3,Exp(P.x,2)),a)
    alphaDenominator = Mult(2,P.y)
    alpha = Div(alphaNumerator,alphaDenominator)

    R = Point(0,0)
    R.x = Sub(Exp(alpha,2),Mult(2,P.x))
    R.y = Sub(Mult(alpha,Sub(P.x,R.x)),P.y)
    return R

if __name__ == "__main__":
    p = sys.argv[1][1:-1].split(',')
    P = Point(x=int(p[0],16),y=int(p[1],16))
    B = basePoint
    W = B
    k = 1
    while W.x != P.x or W.y != P.y:
        k=k+1
        if k == 2:
            W = addSame(B)
        else:
            W=add(W,B)

            
    print(str(k))
        
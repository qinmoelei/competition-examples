#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 28 12:15:22 2017

@author: http://blog.recursiveprocess.com/2013/03/14/calculate-pi-with-python/
"""

from decimal import *
from sys import argv
from os import path

#Sets decimal to 25 digits of precision
getcontext().prec = 25

def factorial(n):
    if n<1:
        return 1
    else:
        return n * factorial(n-1)

def plouffBig(n): #http://en.wikipedia.org/wiki/Bailey%E2%80%93Borwein%E2%80%93Plouffe_formula
    pi = Decimal(0)
    k = 0
    while k < n:
        pi += (Decimal(1)/(16**k))*((Decimal(4)/(8*k+1))-(Decimal(2)/(8*k+4))-(Decimal(1)/(8*k+5))-(Decimal(1)/(8*k+6)))
        k += 1
    return pi

def bellardBig(n): #http://en.wikipedia.org/wiki/Bellard%27s_formula
    pi = Decimal(0)
    k = 0
    while k < n:
        pi += (Decimal(-1)**k/(1024**k))*( Decimal(256)/(10*k+1) + Decimal(1)/(10*k+9) - Decimal(64)/(10*k+3) - Decimal(32)/(4*k+1) - Decimal(4)/(10*k+5) - Decimal(4)/(10*k+7) -Decimal(1)/(4*k+3))
        k += 1
    pi = pi * 1/(2**6)
    return pi

def chudnovskyBig(n): #http://en.wikipedia.org/wiki/Chudnovsky_algorithm
    pi = Decimal(0)
    k = 0
    while k < n:
        pi += (Decimal(-1)**k)*(Decimal(factorial(6*k))/((factorial(k)**3)*(factorial(3*k)))* (13591409+545140134*k)/(640320**(3*k)))
        k += 1
    pi = pi * Decimal(10005).sqrt()/4270934400
    pi = pi**(-1)
    return pi

if __name__=="__main__":
    if len(argv)==1:
        input_dir = '.'
        output_dir = '.'
    else:
        input_dir = path.abspath(argv[1])
        output_dir = path.abspath(argv[2])
        
    print("Using input_dir: " + input_dir)
    print("Using output_dir: " + output_dir)
    
    itnum=20
    pi = chudnovskyBig(itnum) # you can change that to plouffBig(itnum) or bellardBig(itnum)
    
    print "After", itnum, "iterations, pi =", pi
         
    with open(path.join(output_dir, 'answer.txt'), 'wb') as result_file:
        result_file.write(str(pi))


    

__author__ = 'Mike'
import time
from datetime import datetime


def ERROR(txt, errorcount=0):
    print 'ERROR:\t '+ txt

def ADD(txt):
    print '%s ADDING\t '%datetime.now() +txt

def CALC(txt):
    print '%s CALCULATING\t '%datetime.now() +txt

def NEW(txt):
    print '%s NEW\t '%datetime.now() +txt

def RUNTIME():
    print 'RUNTIME \t %ss' %time.clock()

def IMPORTING(txt=''):
    print '%s IMPORTING %sFILE\t '%(datetime.now(), txt)

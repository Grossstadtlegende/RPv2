__author__ = 'Mike'
import time
from datetime import datetime


def ERROR(txt, errorcount=0):
    print '%s ERROR:\t '%datetime.now()+ txt

def WARNING(txt, errorcount=0):
    print '%s WARNING:\t '%datetime.now()+ txt

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

def INFO(txt='', out=False):
    aux = '%s INFO %s\t '%(datetime.now(), txt)
    if not out:
        print aux
    else:
        return aux

def PLOTTING(txt=''):
    print '%s PLOTTING %s\t '%(datetime.now(), txt)

def line():
    print '---------------------------------------'
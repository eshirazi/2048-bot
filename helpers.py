# Use an iterator version of xrange whether it's Python 3 or 2
import random

try:
    irange = xrange
except:
    irange = range

def shuffle(thing):
    ret = list(thing)
    random.shuffle(ret)
    return ret
# Use an iterator version of xrange whether it's Python 3 or 2

try:
    irange = xrange
except:
    irange = range
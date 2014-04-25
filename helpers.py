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

# functions for working with (score, probability tuples)
tuple_max = lambda tuples: max(tuples, key=lambda x: x[0])[0]
tuple_min = lambda tuples: min(tuples, key=lambda x: x[0])[0]
tuple_weighted_average = \
    lambda tuples: sum(
        score * probability
        for score, probability in tuples
    ) / sum(probability for score, probability in tuples)

def tuple_not_implemented(tuples):
    raise Exception("Score aggregation function not chosen")
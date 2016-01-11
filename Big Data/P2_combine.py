"""
Anupa Murali
March 2, 2015
Programming Assignment 2: Problem 2

Use Monte Carlo Integration to approximate pi/4
"""

from mrjob.job import MRJob 
import math
from collections import defaultdict
import random

NUM_INTERVALS = 100001

def fraction(numerator):
    return float(numerator)/100001.0

# Compute sqrt(1-x^2) at x
def circle_equation(x):
    return math.sqrt(1-x**2)

def get_pairs(n):
    generator = random.seed(n)
    return [(random.random(), random.random()) for i in xrange(1000)]

def in_circle(pair):
    x, y = pair
    if y <= circle_equation(float(x)):
        return True
    else:
        return False

class MonteCarloIntegrate(MRJob):
   
    def mapper_init(self):
        self.numerator = defaultdict(int)
        self.denomenator = defaultdict(int)

    def mapper(self, _, line):
        pairs = get_pairs(int(line))
        for pair in pairs:
            if in_circle(pair):
                self.numerator[int(line)] += 1
            self.denomenator[int(line)] += 1
        
    def mapper_final(self):
        for line, value in self.numerator.iteritems():
            yield "numerator", value
        for line, value in self.denomenator.iteritems():
            yield "denomenator", value

    def reducer(self, key, values):
        yield key, sum(values)


if __name__ == '__main__':
    MonteCarloIntegrate.run()

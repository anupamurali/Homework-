"""
Anupa Murali
PA2: P4.py
May 13, 2015

Subclass of MRJob that counts number of times each letter occurs in inputted 
file.
"""

from mrjob.job import MRJob 
import math
from collections import defaultdict

from mrjob.job import MRJob 

newDict = {}
class LetterFrequencyCount(MRJob):
    """
    Functions must be called mapper and reducer
    """
    def mapper(self, key, line):
        for word in line.split():
            for letter in list(word):
                # Check if it is in the alphabet
                if letter.isalpha():
                    yield letter.lower(), 1
                    yield "total", 1




from collections import OrderedDict
from P4 import LetterFrequencyCount
import numpy as np
import sys 
import matplotlib.pyplot as plt 


if __name__ == '__main__':
    lfcounter = LetterFrequencyCount()
    result = lfcounter.run()
    newDict = lfcounter.getDict()

    sortDict = OrderedDict(sorted(newDict.items(), key=lambda t: t[0]))

    fig, ax = plt.subplots()

    fig.canvas.draw()

    plt.xticks(np.arange(1,27))

    x = [i for i in xrange(1,27)]
    y = [value for letter, value in sortDict.iteritems()]

    labels = [letter for letter in sortDict]
    ax.set_xticklabels(labels)

    plt.bar(x, y)
    plt.show()
"""
Anupa Murali 
PA2: P4Driver.py
May 13, 2015

Takes in some text file as an argument, counts number of occurrences of each 
letter in the alphabet, and plots result.
"""

from collections import OrderedDict
from P4 import LetterFrequencyCount
import numpy as np
import sys 
import matplotlib.pyplot as plt 


if __name__ == '__main__':
    files = ["TaleOfTwoCities.txt", "Frankenstein.txt", "PrideAndPrejudice.txt", "WutheringHeights.txt", "ParadiseLost.txt"]
    colors = ['r', 'b', 'g', 'y', 'c']
    count = 0

    fig, ax = plt.subplots()
    fig.canvas.draw()
    plt.xticks(np.arange(1,27))
    x = [i for i in xrange(1,27)]
    labels = map(chr, range(97, 123))
    ax.set_xticklabels(labels)

    for f in files:
        lfcounter = LetterFrequencyCount(args=["Novels - P4/" + f])
        print "*"*50
        currDict = {}
        with lfcounter.make_runner() as runner:
            print runner._input_paths
            runner.run()
            for line in runner.stream_output():
                key, value = lfcounter.parse_output_line(line)
                currDict[key] = value
                
        total_letters = currDict["total"]
        currDict.pop("total")


        for i in currDict.iteritems():
            currDict[i[0]] = float(i[1])/float(total_letters)


        sortDict = OrderedDict(sorted(currDict.items(), key=lambda t: t[0]))

        y = [value for letter, value in sortDict.iteritems()]

        plt.plot(x, y, color=colors[count], label=f)
        count += 1

    plt.legend()
    plt.show()
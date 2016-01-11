# job.py
from mrjob.job import MRJob
newDict = {}
class MyJob(MRJob):
    def mapper(self, key, line):
        for word in line.split():
            for letter in list(word):
                # Check if it is in the alphabet
                if letter.isalpha():
                    yield letter.lower(), 1
                    yield "total", 1

    def reducer(self, key, values):
        newDict[key] = sum(values)
        yield key, newDict[key]

    def getDict(self):
        return newDict

if __name__ == '__main__':
    MyJob.run()
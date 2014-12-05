from os import system
from sys import stdout
weights = ['.5 0 .5', '.4 .2 .4']

print "Running on differing PCA components..."
for weight in weights:
    command = ""
    for comp in xrange(20, 101, 20):
        command = 'python Validation.py -k 50 -c ' + str(comp) + ' -w ' + weight
        print "Running " + command + '...',
        stdout.flush()
        system(command + ">> results.csv")
        print "finished"

print "Running on differing knnKs..."
for weight in weights:
    command = ""
    for knnk in xrange(10, 101, 10):
        command = 'python Validation.py -k '+ str(knnk) + ' -c 100 -w ' + weight
        print "Running " + command + '...',
        stdout.flush()
        system(command + ">> results.csv")
        print "finished"

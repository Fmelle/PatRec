from os import system
from sys import stdout

weights = ['.5 0 .5', '.4 .2. 4']

print "Running on differing PCA components..."
for weight in weights:
    for comp in xrange(20, 101, 20):
        command = 'python Validation.py -k 50 -c ' + str(comp) + ' -w ' + weight
        print command + ' ...',
        stdout.flush()
        command = command + ' >> results.csv'
        system(command)
        print "completed"

print "Running on differing knnKs..."
for weight in weights:
    for knnk in xrange(10, 101, 10):
        command = 'python Validation.py -k ' + str(knnk) + ' -c 100 -w ' + weight
        print command + ' ...',
        stdout.flush()
        command = command + ' >> results.csv'
        system(command)
        print "completed"

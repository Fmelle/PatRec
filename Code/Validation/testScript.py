from os import system
from sys import stdout
weights = ['.5 0 .5', '.33 .33 .33']

print "Running on differing PCA components..."
for weight in weights:
    command = ""
    for comp in xrange(20, 201, 20):
        command = 'python Validation.py -k 100 -c ' + str(comp) + ' -w ' + weight
        print "Running " + command + '...',
        stdout.flush()
        system(command + ">> results.csv")
        print "finished"

# print "Running on differing knnKs..."
# for weight in weights:
#     command = ""
#     for knnk in xrange(10, 151, 10):
#         command = 'python Validation.py -k '+ str(knnk) + ' -c 100 -w ' + weight
#         print "Running " + command + '...',
#         stdout.flush()
#         system(command + ">> results.csv")
#         print "finished"

print "Results saved to results.csv"

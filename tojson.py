import json
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.mlab as mlab
from scipy.stats import norm

datafile = open('yellowTest1000.txt','r')

trips = []

trip = {}

for line in datafile:
    splitline = line.split()
    if splitline[0] == 'Dist,':
        trip['recorded_dist'] = int(float(splitline[1].split(':')[1][:-1]))
        trip['google_dist'] = int(splitline[2].split(':')[1])
    if splitline[0] == 'Time,':
        trip['recorded_time'] = int(float(splitline[1].split(':')[1][:-1]))
        trip['google_time'] = int(splitline[2].split(':')[1])
        trips += [trip]
        trip = {}
ratios = []

for trip in trips:
    ratio = float(trip['recorded_time'])/float(trip['google_time'])
    trip['ratio'] = ratio
    if ratio < 10:
        ratios += [ratio]
    #print json.dumps(trip, indent =1)
'''
#print ratios
print sum(ratios)/len(ratios)

#(mu, sigma) = norm.fit(ratios)

n, bins, patches = plt.hist(ratios, 50, facecolor='green', alpha=0.75)

#y = mlab.normpdf(bins, mu, sigma)
#l = plt.plot(bins, y, 'r--', linewidth=2)

plt.plot(bins)

plt.axis([0, 2.2, 0, 200])
plt.ylabel('Number of trips')
plt.xlabel('Actual Duration/Predicted Duraction Ratio')
plt.show()'''



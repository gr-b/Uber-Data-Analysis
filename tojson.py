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
        trip['tip'] = float(splitline[3])
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


x = []
y = []
sumbelow1 = 0
numbelow1 = 0

sumabove1 = 0
numabove1 = 0
for trip in trips:
    #points += [(trip['ratio'], trip['tip'])]
    if trip['ratio'] < 3:
        x += [trip['ratio']]
        y += [float(trip['tip'])/float(trip['recorded_time'])]
    
        if trip['ratio'] < 1:
            sumbelow1 += trip['tip']
            numbelow1 += 1
        elif trip['ratio'] >= 1:
            sumabove1 += trip['tip']
            numabove1 += 1
        
avgbelow = sumbelow1 / numbelow1
avgabove = sumabove1 / numabove1

print 'Average tip with trip ratio below 1: ' + str(avgbelow)
print 'Average tip with trip ratio above 1: ' + str(avgabove)
        
plt.scatter(x, y)
plt.ylabel('Tip Amount (Adjusted by Trip Duration)')
plt.xlabel('Ratio of Actual Trip Duration / Predicted Trip Duration')
plt.title('Do people tip more if the taxi goes faster than expected?')
plt.show()

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



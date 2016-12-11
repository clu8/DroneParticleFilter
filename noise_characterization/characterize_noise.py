import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from scipy.stats import norm

df = pd.read_csv('sensor_noise_log.txt')
accels = []
summ = 0
for index,row in df.iterrows():
    # print row[0]
    
    # print float(row[0])/2
    
    if float(row[0]) > 23:
        accels.append(float(row[0]))
# print summ
# print accels
mu = np.average(accels)
print mu
(mu,sigma) = norm.fit(accels)
print (mu, sigma)
weights = np.ones_like(accels)/float(len(accels))
n,bins,patches = plt.hist(accels, 50, weights = weights, facecolor='green', alpha=0.75)

y = mlab.normpdf( bins, mu, sigma)
l = plt.plot(bins, y, 'r--', linewidth=1)


plt.show()
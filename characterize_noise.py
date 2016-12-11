import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from scipy.stats import norm

df = pd.read_csv('sensor_noise_log.txt')
accels = []
for index,row in df.iterrows():
    accels.append(row[1] if row[1] < 2 else 0)
# print accels
(mu,sigma) = norm.fit(accels)
print (mu, sigma)
n,bins,patches = plt.hist(accels, 50, normed=1, facecolor='green', alpha=0.75)

# y = mlab.normpdf( bins, mu, sigma)
# l = plt.plot(bins, y, 'r--', linewidth=1)


plt.show()
import matplotlib
matplotlib.use('TkAgg')

import scipy.stats
import matplotlib.pyplot as plt

from scipy.stats import randint
import numpy as np


#normal
distribution = scipy.stats.norm(loc=100,scale=5)
print distribution.stats('mvsk')
# skewed
distribution = scipy.stats.gengamma(100, 90, loc=50, scale=10)
print distribution.stats('mvsk')

sample = distribution.rvs(size=10000)

sample = randint.rvs(0, 208, size = 1000)


pers = np.arange(1,101,1)

# Make each of the last 41 elements 5x more likely
prob = [1.0]*(len(pers)-41) + [5.0]*41

# Normalising to 1.0
prob /= np.sum(prob)

sample = np.random.choice(pers, 1000, p=prob)

plt.hist(sample)
plt.show()

print np.bincount(sample)[10]

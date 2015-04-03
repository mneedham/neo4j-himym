import math
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

values = range(1, 209)
probs = [1.0 / 208] * 208

for idx, prob in enumerate(probs):
    if idx > 3 and idx < 20:
        probs[idx] = probs[idx] * (1 + math.log(idx + 1))
    if idx > 20 and idx < 40:
        probs[idx] = probs[idx] * (1 + math.log((40 - idx) + 1))

probs = [p / sum(probs) for p in probs]
sample =  np.random.choice(values, 1000, p=probs)

print np.bincount(sample)[1]
print np.bincount(sample)[10]
print np.bincount(sample)[206]

binwidth = 2
plt.hist(sample, bins=np.arange(min(sample), max(sample) + binwidth, binwidth))
plt.xlim([0, max(sample)])
plt.show()

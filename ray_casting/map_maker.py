import numpy as np
from random import randint as rnd

N, M = 10, 10

level = np.zeros((N, M))
#level[1:N - 1, 1:M - 1] -= np.ones((N - 2, M - 2))


for _ in range(30):
    level[rnd(1,N - 2), rnd(1,M - 2)] = 1
    
print(level)
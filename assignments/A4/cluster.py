import numpy as np
from scipy.cluster.hierarchy import fclusterdata

#instances = np.ndarray

instances = np.array([(-4,-2), (-3,-2), (-2,-2), (-1,-2), (1, -1), (1,1), (2,3), (3,2), (3,4), (4,3)])

fclust1 = fclusterdata(instances, 0.0, method='single')
print(fclust1)
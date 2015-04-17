from clustering import Clustering
import math
import numpy as np
def objectiveFunction(ind):
	return ind**2
population = [1,2,0,3,4,9,6,-11,7,5,8,10]
print population + population
print population
for ind in population:
	population[population.index(ind)] = (ind,objectiveFunction(ind))

print population
population = sorted(population, key=lambda ind: ind[1])
clusterAssment = np.mat(np.zeros((10,2)))
clusterAssment[1,1] = 10
clusterAssment[1,0] = 5
clusterAssment[2,1] = 10
clusterAssment[3,0] = 5
clusterAssment[4,1] = 10
clusterAssment[5,0] = 5
print np.sum(clusterAssment[:,1)


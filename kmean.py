from numpy import *
import numpy as np
import time
def distEuclid(vecA,vecB):
	#Distance euclidienne entre 2 vecteurs
	if (np.isnan(sqrt(sum(power(vecA - vecB,2))))):
		print 'VEC A'
		print vecA
		print 'VEC B'
		print vecB
		time.sleep(60)

	# return sqrt(sum(power(vecA - vecB,2)))
	return np.linalg.norm(vecA-vecB)

def randCent(dataSet,k):
	#Generation aleatoire de K centroides
	n = shape(dataSet)[1]
	centroids = mat(zeros((k,n)))
	for j in range(n):
		minJ = min(dataSet[:,j])
		rangeJ = float(max(dataSet[:,j]) - minJ)
		centroids[:,j] = minJ + rangeJ * random.rand(k,1)
	return centroids

def kMeans(dataSet, k):
	#Algorithne des k-moyennes
	m = shape(dataSet)[0]
	clusterAssment = mat(zeros((m,2)))
	centroids = randCent(dataSet, k)
	clusterChanged = True
	while clusterChanged:
		clusterChanged = False
		for i in range(m):
			minDist = inf; minIndex = -1
			for j in range(k):
				distJI = distEuclid(centroids[j,:],dataSet[i,:])
				if distJI < minDist:
					minDist = distJI; minIndex = j
			#Si un des elements change de centroide on repart pour un tour pour optimiser encore la distance globale
			if clusterAssment[i,0] != minIndex: clusterChanged = True
			#On ajoute l'assignation de cluster et la distance par rapport a son centre
			clusterAssment[i,:] = minIndex,minDist**2
		# On redefinit les centroides a partir de la moyenne du cluster
		for cent in range(k):

			ptsInClust = dataSet[nonzero(clusterAssment[:,0].A==cent)[0]]
			if(ptsInClust.size != 0):
				# print ptsInClust
				
				centroids[cent,:] = mean(ptsInClust, axis=0)
		#On affiche la somme des distances des k centroids par rapport aux donnes pour la comparer a l'algo genetique
		# print np.sum(clusterAssment[:,1])
	
	return centroids, clusterAssment
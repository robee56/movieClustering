

import numpy as np
import pylab as plt


def printClusters(reduced_data):
	#Dessin des donnes avec matplotlib
	centroids, clusterAssment = kMeans(reduced_data,5)

	cluster1X = []
	cluster1Y = []
	cluster2X = []
	cluster2Y = []
	cluster3X = []
	cluster3Y = []
	cluster4X = []
	cluster4Y = []
	cluster5X = []
	cluster5Y = []

	for i in range(len(reduced_data)):

		if(clusterAssment[i][0,0]==0):
			cluster1X.append(reduced_data[i,0])
			cluster1Y.append(reduced_data[i,1])
		if(clusterAssment[i][0,0]==1):
			cluster2X.append(reduced_data[i,0])
			cluster2Y.append(reduced_data[i,1])
		if(clusterAssment[i][0,0]==2):
			cluster3X.append(reduced_data[i,0])
			cluster3Y.append(reduced_data[i,1])
		if(clusterAssment[i][0,0]==3):
			cluster4X.append(reduced_data[i,0])
			cluster4Y.append(reduced_data[i,1])
		if(clusterAssment[i][0,0]==4):
			cluster5X.append(reduced_data[i,0])
			cluster5Y.append(reduced_data[i,1])

	plot(cluster1X,cluster1Y,'sg')
	plot(cluster2X,cluster2Y,'ob')
	plot(cluster3X,cluster3Y,'or')
	plot(cluster4X,cluster4Y,'mo')
	plot(cluster5X,cluster5Y,'ys')

	show()
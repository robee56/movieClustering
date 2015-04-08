from dataset import Dataset
from movies import Movie
from notes import Notes
from users import User
from kmean import kMeans
import os
from numpy import *
import numpy
from pylab import plot,show
import operator
from numpy import multiply

currentPath = os.path.dirname(os.path.realpath(__file__))

FileUser = currentPath  + "/data/u.user"
FileMovies = currentPath  + "/data/u.item"
FileNotes = currentPath  + "/data/u.base"

dataset = Dataset(FileUser,FileMovies,FileNotes)
dataset.vecteurNotes()
for user in dataset.users:
	user.normaliserVecteur()


print "USER 1 "
print dataset.users[0].vecteurGenre
print dataset.users[0].vecteurGenreVote
print dataset.users[0].vecteurNormalise

print "USER 2 "
print dataset.users[1].vecteurNormalise

print "USER 3 "
print dataset.users[2].vecteurNormalise


reducedDataset = numpy.zeros((len(dataset.users),21))

for i in range(len(dataset.users)):
	for j in range(20):

		if(j==0):
			reducedDataset[i,j] = float(dataset.users[i].age)
		if(j==1):
			if(dataset.users[i].genre == "M"):
				genre = 0
			else:
				genre = 1
			reducedDataset[i,j] = genre 
		if(j>1):
			reducedDataset[i,j] = dataset.users[i].vecteurNormalise[j-1]

print "premier reduce dataset "
print reducedDataset[0]


centroids, clusterAssment = kMeans(reducedDataset,3)

cluster1X = []
cluster1Y = []
cluster2X = []
cluster2Y = []
cluster3X = []
cluster3Y = []

for i in range(len(reducedDataset)):

	if(clusterAssment[i][0,0]==0):
		cluster1X.append(reducedDataset[i,0])
		cluster1Y.append(reducedDataset[i,1])
	if(clusterAssment[i][0,0]==1):
		cluster2X.append(reducedDataset[i,0])
		cluster2Y.append(reducedDataset[i,1])
	elif(clusterAssment[i][0,0]==2):
		cluster3X.append(reducedDataset[i,0])
		cluster3Y.append(reducedDataset[i,1])


plot(cluster1X,cluster1Y,'sg')
plot(cluster2X,cluster2Y,'ob')
plot(cluster3X,cluster3Y,'or')

show()
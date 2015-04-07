from dataset import Dataset
from movies import Movie
from notes import Notes
from users import User
from kmean import kMeans
import os
from numpy import *
import numpy

currentPath = os.path.dirname(os.path.realpath(__file__))

FileUser = currentPath  + "/data/u.user"
FileMovies = currentPath  + "/data/u.item"
FileNotes = currentPath  + "/data/u.base"

dataset = Dataset(FileUser,FileMovies,FileNotes)
# reducedDataset = []
reducedDataset = numpy.zeros((len(dataset.users),2))

for i in range(len(dataset.users)):
	# if(dataset.users[i].genre == "M"):
	# 	genre = 0
	# else:
	# 	genre = 1
	# reducedDataset.append((dataset.users[i].age,genre))

	for j in range(2):

		if(j==0):
			reducedDataset[i,j] = dataset.users[i].age
		else:
			if(dataset.users[i].genre == "M"):
				genre = 0
			else:
				genre = 1
			reducedDataset[i,j] = genre 


print 'new dataset'
print reducedDataset[0]
m = shape(reducedDataset)[0]
print reducedDataset[0,1]

print m
kMeans(reducedDataset,3)
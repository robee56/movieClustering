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
import math
from clustering import Clustering


def listFilms(x,y):
	listcommune = []
	for i in dataset.notes:
		tab = []
		if(i.idUser > (x.id)):
			break
		if(x.id  == i.idUser):
			tab.append(i.idMovie)
			tab.append(i.note)
			tab.append(-1)
			listcommune.append(tab)
	j=0
	for i in dataset.notes:

		limite = len(listcommune)
		if(i.idUser > y.id or j > limite):
			break
		if(y.id == i.idUser):
			while(j<limite):
				if(i.idMovie == listcommune[j][0]):
					listcommune[j][2] = i.note
					j = j+1
					break
				elif(i.idMovie > listcommune[j][0]):
					listcommune.pop(j)
					limite = limite - 1
				else:
					break
	return listcommune



def pcs(x,y):

	Rx = x.avg
	Ry = y.avg
	listcommune= listFilms(x,y)
	s1 = 0.0
	s2 = 0.0
	s3 = 0.0

	for i in range(len(listcommune)):
		noteX = listcommune[i][1]
		noteY = listcommune[i][2]
		s1 = s1 + (noteX - Rx)**2
		s2 = s2 + (noteY - Ry)**2
		s3 = s3 + ((noteX - Rx) * (noteY - Ry))
	if(math.sqrt(s2 * s1) == 0):
		return float(0)
	return float(s3 / (math.sqrt(s2 * s1)))

def listeFilmsNonVu(j,listeKnn):
	listeFilmsNonVu = []
	listeNotesNonVu = []
	listeFilmsVu = []
	userId = j
	for i in range(len(dataset.notes)):
		notes = dataset.notes
		if(notes[i].idUser in listeKnn):
			if(notes[i].idMovie not in listeFilmsNonVu):
				listeFilmsNonVu.append(notes[i].idMovie)
				listeNotesNonVu.append([notes[i].note,1])
			else:
				idx = listeFilmsNonVu.index(notes[i].idMovie)
				listeNotesNonVu[idx][0] = listeNotesNonVu[idx][0] + notes[i].note
				listeNotesNonVu[idx][1] = listeNotesNonVu[idx][1] + 1
		if(notes[i].idUser > max(listeKnn)):
			break
	j = userId          
	for i in dataset.notes:
	    
	    if(i.idUser == dataset.users[j-1].id):
	        listeFilmsVu.append(i.idMovie)

	i = 0
	while(i<len(listeFilmsNonVu)):
	    if listeFilmsNonVu[i] in listeFilmsVu:
	        listeFilmsNonVu.pop(i)
	        listeNotesNonVu.pop(i)
	    else:
	        i = i + 1
	        
	print len(listeFilmsNonVu)
	listeNote = []
	for i in range(len(listeNotesNonVu)):
	    bonus = listeNotesNonVu[i][1]
	    listeNote.append((listeNotesNonVu[i][0] / (listeNotesNonVu[i][1] * 1.0)) )


	print max(listeNote)
	listeFilmVoir = []


	for i in range(5):
	    listeFilmVoir.append(listeFilmsNonVu[listeNote.index(max(listeNote))])
	    listeNote[listeNote.index(max(listeNote))] = -1

	print listeFilmVoir
	for i in listeFilmVoir:
	    print dataset.movies[i].nom
	    print dataset.movies[i].vecteur





def recommandation(k,j,clusterJ):

	listePcsvalue=[]
	listeKnn = []
	for i in range(len(reducedDataset)):

		pcsValue = -1
		if(i!=j-1):
			if(i>j-1):
				pcsValue = pcs(users[j-1],users[i])
			else:
				pcsValue = pcs(users[i],users[j-1])
			if(clusterAssment[i][0,0] == clusterAssment[j-1][0,0]):
				listePcsvalue.append(pcsValue)
			else:
				listePcsvalue.append(-1)
	
	for i in range(k):
		maxV = max(listePcsvalue)
		indexV = listePcsvalue.index(max(listePcsvalue)) 
		listePcsvalue[indexV] = -1
		listeKnn.append(indexV + 1)

	print listeKnn
	print clusterAssment[j-1][0,0]
	print "vecteur user cible : " + str(dataset.users[j].vecteurNormalise)
	for i in listeKnn:
		print clusterAssment[i][0,0]
		print "vecteur voisins : " + str(dataset.users[i].vecteurNormalise)
	listeFilmsNonVu(j,listeKnn)




		

currentPath = os.path.dirname(os.path.realpath(__file__))

FileUser = currentPath  + "/data/u.user"
FileMovies = currentPath  + "/data/u.item"
FileNotes = currentPath  + "/data/u.base"

dataset = Dataset(FileUser,FileMovies,FileNotes)
dataset.vecteurNotes()
for user in dataset.users:
	user.moyenne(dataset)
	user.normaliserVecteur()


# print "USER 1 "
# print dataset.users[0].vecteurGenre
# print dataset.users[0].vecteurGenreVote
# print dataset.users[0].vecteurNormalise

# print "USER 2 "
# print dataset.users[1].vecteurNormalise

# print "USER 3 "
# print dataset.users[2].vecteurNormalise


reducedDataset = numpy.zeros((len(dataset.users),21))
print "NB USERS : "
print len(dataset.users)
for i in range(len(dataset.users)):
	for j in range(20):

		if(j==0):
			reducedDataset[i,j] = float(dataset.users[i].age)/10
		if(j==1):
			if(dataset.users[i].genre == "M"):
				genre = 0
			else:
				genre = 1
			reducedDataset[i,j] = genre 
		if(j>1):
			reducedDataset[i,j] = dataset.users[i].vecteurNormalise[j-1]

# print "premier reduce dataset "
# print reducedDataset[0]

users =  dataset.users
clust = Clustering()

print clust.GA(10,reducedDataset,18)
centroids, clusterAssment = kMeans(reducedDataset,18)

print "similarite 1,6" + str(pcs(users[0],users[5]))
print "similarite 1,2" + str(pcs(users[0],users[1]))
print "similarite 2,6" + str(pcs(users[1],users[5]))



# listeKnn = []
# k = 10
# listePcsvalue = []
# j = 1
# print "Cluster J : " + str(clusterAssment[j-1])
# print clusterAssment[j-1][0,0] 
# recommandation(k,j,clusterAssment[j-1][0,0] )





# cluster1X = []
# cluster1Y = []
# cluster2X = []
# cluster2Y = []
# cluster3X = []
# cluster3Y = []
# cluster4X = []
# cluster4Y = []
# cluster5X = []
# cluster5Y = []

# for i in range(len(reducedDataset)):

# 	if(clusterAssment[i][0,0]==0):
# 		cluster1X.append(reducedDataset[i,0])
# 		cluster1Y.append(reducedDataset[i,1])
# 	if(clusterAssment[i][0,0]==1):
# 		cluster2X.append(reducedDataset[i,0])
# 		cluster2Y.append(reducedDataset[i,1])
# 	if(clusterAssment[i][0,0]==2):
# 		cluster3X.append(reducedDataset[i,0])
# 		cluster3Y.append(reducedDataset[i,1])
# 	if(clusterAssment[i][0,0]==3):
# 		cluster4X.append(reducedDataset[i,0])
# 		cluster4Y.append(reducedDataset[i,1])
# 	if(clusterAssment[i][0,0]==4):
# 		cluster5X.append(reducedDataset[i,0])
# 		cluster5Y.append(reducedDataset[i,1])




# plot(cluster1X,cluster1Y,'sg')
# plot(cluster2X,cluster2Y,'ob')
# plot(cluster3X,cluster3Y,'or')
# plot(cluster4X,cluster4Y,'mo')
# plot(cluster5X,cluster5Y,'ys')



# show()


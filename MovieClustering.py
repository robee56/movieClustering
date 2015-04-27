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
import pickle
from sklearn.metrics import mean_squared_error
import time 
def listFilms(x,y,dataset,clust=False,movieClust = -1):
	#Cette fonction etablit la liste commune de films entre x et y
	listcommune = []
	if(clust):
		for i in dataset.notes:
			tab = []
			if(i.idUser > (x.id)):
				break
			if(x.id  == i.idUser and movieClust == dataset.movies[i.idMovie-1].cluster):
				tab.append(i.idMovie)
				tab.append(i.note)
				tab.append(-1)
				listcommune.append(tab)
	else:
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



def pcs(x,y,dataset,clust=False,movieClust = 0):
	#La fonction pcs mesure la similarite entre deux personnes basee sur les films qu'ils ont en commun
	Rx = x.avg
	Ry = y.avg
	if(clust):
		listcommune= listFilms(x,y,dataset,clust,movieClust)
	else:
		listcommune= listFilms(x,y,dataset)
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

def listeFilmsNonVu(j,listeKnn,clusterSize,dataset,clusterFilm=-1):
	#Liste des films non vu pemet de prendre les films des k voisins qui n'ont pas ete vu par l'utilisateur j
	listeFilmsNonVu = []
	listeNotesNonVu = []
	listeFilmsVu = []
	userId = j
	for i in range(len(dataset.notes)):
		notes = dataset.notes
		if(notes[i].idUser in listeKnn):
			if(clusterFilm != -1):
				if((notes[i].idMovie not in listeFilmsNonVu )and (dataset.movies[notes[i].idMovie].cluster == clusterFilm  )):
					listeFilmsNonVu.append(notes[i].idMovie)
					listeNotesNonVu.append([notes[i].note,1])
				elif(dataset.movies[notes[i].idMovie].cluster == clusterFilm):
					idx = listeFilmsNonVu.index(notes[i].idMovie)
					listeNotesNonVu[idx][0] = listeNotesNonVu[idx][0] + notes[i].note
					listeNotesNonVu[idx][1] = listeNotesNonVu[idx][1] + 1
			else:
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
	    if(i.idUser > dataset.users[j-1].id):
	    	break

	i = 0
	while(i<len(listeFilmsNonVu)):
	    if listeFilmsNonVu[i] in listeFilmsVu:
	        listeFilmsNonVu.pop(i)
	        listeNotesNonVu.pop(i)
	    else:
	        i = i + 1
	        
	# print len(listeFilmsNonVu)
	listeNote = []
	for i in range(len(listeNotesNonVu)):
	    if(listeNotesNonVu[i][1]>(len(listeKnn)/6)):
	    	listeNote.append(((listeNotesNonVu[i][0]) / (listeNotesNonVu[i][1] * 1.0)))


	# print max(listeNote)
	listeFilmVoir = []


	for i in range(len(listeFilmsNonVu)):
		if(max(listeNote)) != -1:
			listeFilmVoir.append((listeFilmsNonVu[listeNote.index(max(listeNote))],max(listeNote)))
			listeNote[listeNote.index(max(listeNote))] = -1
		else:
			break
	    # listeFilmVoir.append(listeFilmsNonVu[listeNote.index(max(listeNote))])


	genreFilms = {	0:'unknown',
					1:'Action',
					2:'Adventure',
					3:'Animation',
					4:'Children',
					5:'Comedy',
					6:'Crime',
					7:'Documentary',
					8:'Drama',
					9:'Fantasy',
					10:'Film-Noir',
					11:'Horror',
					12:'Musical',
					13:'Mystery',
					14:'Romance',
					15:'Sci-Fi',
					16:'Thriller',
					17:'War',
					18:'Western'}    
	# print listeFilmVoir
	
	print "\n Les utilisateurs similaires a vous ont aime les films suivants  : \n"
	dataset.users[j-1].listfilms = listeFilmVoir[:]
	for i in listeFilmVoir:
		# print "cluster : " + str(dataset.movies[i[0]].cluster)
		
		genre = []
		for genr in range(len(dataset.movies[i[0]].vecteur)):
			if(dataset.movies[i[0]].vecteur[genr] == 1):
				genre.append((genreFilms[genr],float("{0:.2f}".format(dataset.movies[i[0]].vecteur[genr]))))
		print " Nom : %s, id : %d, note : %f " % (dataset.movies[i[0]].nom,i[0],i[1]),"genre : " + str(genre)



def recommandation(k,j,clusterJ,users,reducedDataset,dataset,clusterAssment,centroids,allC = False,ClusterFilm = -1,MovieId = -1):
	#La fonction recommandation effectue la mesure de similarite avec PCS, puis etablit les k voisins
	#Ces k voisins vont permettre de determiner une lsite de films que J n'a pas vu
	#Cluster J est le cluster de j dans lequel on recherche les k voisins
	listePcsvalue=[]
	listeKnn = []
	for i in range(len(reducedDataset)):

		pcsValue = -1

		if(i!=j-1):
			if(ClusterFilm != -1):
				if(clusterAssment[i][0,0] == clusterAssment[j-1][0,0]):
					if(i>j-1):
						pcsValue = pcs(users[j-1],users[i],dataset,True,ClusterFilm)
					else:
						pcsValue = pcs(users[i],users[j-1],dataset,True,ClusterFilm)
				
					listePcsvalue.append((i,pcsValue))
				elif(allC==True):
					if(i>j-1):
						pcsValue = pcs(users[j-1],users[i],dataset,True,ClusterFilm)
					else:
						pcsValue = pcs(users[i],users[j-1],dataset,True,ClusterFilm)
				
					listePcsvalue.append((i,pcsValue))
			else:

				if(clusterAssment[i][0,0] == clusterAssment[j-1][0,0]):
					if(i>j-1):
						pcsValue = pcs(users[j-1],users[i],dataset)
					else:
						pcsValue = pcs(users[i],users[j-1],dataset)
				
					listePcsvalue.append((i,pcsValue))
				elif(allC==True):
					if(i>j-1):
						pcsValue = pcs(users[j-1],users[i],dataset)
					else:
						pcsValue = pcs(users[i],users[j-1],dataset)
				
					listePcsvalue.append((i,pcsValue))


	listePcsvalue = sorted(listePcsvalue, key=lambda value: value[1],reverse = True)

	
	print "\n Nombre de personnes dans le cluster de l'utilisateur : \n" + str(len(listePcsvalue))
	
	for i in range(k):
		listeKnn.append(listePcsvalue[i][0])
	genreFilms = {	0:'unknown',
					1:'Action',
					2:'Adventure',
					3:'Animation',
					4:'Children',
					5:'Comedy',
					6:'Crime',
					7:'Documentary',
					8:'Drama',
					9:'Fantasy',
					10:'Film-Noir',
					11:'Horror',
					12:'Musical',
					13:'Mystery',
					14:'Romance',
					15:'Sci-Fi',
					16:'Thriller',
					17:'War',
					18:'Western'}

	genre = []
	for i in range(len(dataset.users[j].vecteurNormalise)):
		genre.append((genreFilms[i],float("{0:.2f}".format(dataset.users[j].vecteurNormalise[i]))))

	
	if(ClusterFilm != -1):
		listeFilmsNonVu(j,listeKnn,len(listePcsvalue),dataset,ClusterFilm)
	else:
		print "Le vecteur de Gout de l'utilisateur cible est : \n"
		
		print sorted(genre, key=lambda ind: ind[1],reverse = True)
		listeFilmsNonVu(j,listeKnn,len(listePcsvalue),dataset)



def saveData():

		
	#Determination du chemin de l'application pour y chercher les donnes du dataset

	currentPath = os.path.dirname(os.path.realpath(__file__))

	FileUser = currentPath  + "/data/u.user"
	FileMovies = currentPath  + "/data/u.item"
	FileNotes = currentPath  + "/data/u1.base"

	dataset = Dataset(FileUser,FileMovies,FileNotes)
	dataset.vecteurNotes()
	for user in dataset.users:
		user.moyenne(dataset)
		user.normaliserVecteur()
	for i in dataset.notes:
		dataset.movies[i.idMovie-1].totalNotes = dataset.movies[i.idMovie-1].totalNotes + i.note
		dataset.movies[i.idMovie-1].nbNotes = dataset.movies[i.idMovie-1].nbNotes + 1
	for i in range(len(dataset.movies)):
		if(dataset.movies[i].nbNotes!=0):
			dataset.movies[i].avg = dataset.movies[i].totalNotes / dataset.movies[i].nbNotes


#ReducedDataset est notre dataset utilise pour effectuer notre clustering il contient : Age,Sexe, ainsi que 19 types de films
	reducedDataset = numpy.zeros((len(dataset.users),21))
	print "NB USERS : "
	print len(dataset.users)
	for i in range(len(dataset.users)):
		for j in range(20):

			if(j==0):
				reducedDataset[i,j] = float(dataset.users[i].age)/100
			if(j==1):
				if(dataset.users[i].genre == "M"):
					genre = 0
				else:
					genre = 1
				reducedDataset[i,j] = genre 
			if(j>1):
				reducedDataset[i,j] = dataset.users[i].vecteurNormalise[j-1]
	centroids, clusterAssment = kMeans(reducedDataset,10)
	with open('dataset.pkl', 'wb') as output:
		pickle.dump(dataset,output)
	with open('reducedDataset.pkl', 'wb') as output:
		pickle.dump(reducedDataset,output)
	with open('centroids.pkl', 'wb') as output:
		pickle.dump(centroids,output)
	with open('clusterAssment.pkl', 'wb') as output:
		pickle.dump(clusterAssment,output)

# print "premier reduce dataset "
# print reducedDataset[0]
def loadData():
	centroids = []
	with open('dataset.pkl', 'rb') as picklF:
		dataset = pickle.load(picklF)
	with open('reducedDataset.pkl', 'rb') as picklF:
		reducedDataset = pickle.load(picklF)
	with open('clusterAssment.pkl', 'rb') as picklF:
		clusterAssment = pickle.load(picklF)
	with open('centroids.pkl', 'rb') as picklF:
		centroids = pickle.load(picklF)
	
	return dataset,reducedDataset,centroids,clusterAssment

def printClusters(reduced_data,algo="kmean"):
	#Dessin des donnes avec matplotlib
	clust = Clustering(reduced_data,5)
	if(algo == "ga"):
		clust.GA(10)
	else:
		clust.kMeans()


	centroids, clusterAssment = clust.centroids, clust.clusterAssment

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



def testErreur(idUser,dataset,notes):
	liste_films = []
	for i in notes:
		if(i.idUser == idUser):
			liste_films.append((i.idMovie,i.note))
	y_actual = []
	y_predicted = []

	for movie in dataset.users[idUser-1].listfilms:
		for film in liste_films:
			if film[0] == movie[0]:
				y_actual.append(film[1])
				y_predicted.append(movie[1])
				

	rms = sqrt(mean_squared_error(y_actual, y_predicted))
	return rms

def getOsPath():
	return os.path.dirname(os.path.realpath(__file__))

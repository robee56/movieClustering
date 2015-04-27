from MovieClustering import*
import operator
from sklearn.decomposition import PCA
from sklearn.preprocessing import scale
import time
#Fichier de test pour essayer le programme 
dataset,reducedDataset,centroids,clusterAssment = loadData()

datasetFilms = []
for i in dataset.movies:
    datasetFilms.append(i.vecteur)

dataset_Films =  PCA(n_components=2).fit_transform(datasetFilms)
printClusters(numpy.array(dataset_Films))
print numpy.array(dataset_Films)

reduced_data = reducedDataset[:,2:]
reduced_data =  PCA(n_components=2).fit_transform(reduced_data)
printClusters(reduced_data)
printClusters(reduced_data,"GA")


dataGout = reducedDataset[:,2:]
clustGout = Clustering(dataGout,10)
centroidsGout, clusterAssmentGout = clustGout.kMeans()
users =  dataset.users

k = 5
err1 = numpy.zeros(100)
err2 = numpy.zeros(100)
currentPath = os.path.dirname(os.path.realpath(__file__))
FileNotes = currentPath  + "/data/u1.test"

file_object = open(FileNotes, 'r')
corpus = file_object.readlines()
file_object.close()
notes = []
for j in range(len(corpus)):
	note = corpus[j].replace('\n','')
	m = note.split('\t')
	notes.append(Notes(m[0],m[1],m[2],m[3]))


for j in range(1,100):
	start_time = time.time()
	recommandation(k,j,clusterAssmentGout[j-1][0,0],users,dataGout,dataset,clusterAssmentGout,centroidsGout)
	print "Temps d'execution : %d secondes" % (time.time() - start_time),j
	err1[j-1] = testErreur(j,dataset,notes)

print "RMSE : " + str(numpy.mean(err1))
for j in range(1,100):
	start_time = time.time()
	recommandation(k,j,clusterAssmentGout[j-1][0,0],users,dataGout,dataset,clusterAssmentGout,centroidsGout,allC = True)
	print "Temps d'execution : %d secondes" % (time.time() - start_time),j
	err2[j-1] = testErreur(j,dataset,notes)


print "RMSE : " + str(numpy.mean(err2))




time.sleep(30)

clust = Clustering(numpy.array(datasetFilms),20)
clust.kMeans()
clusterAssment = clust.clusterAssment
centroids = clust.centroids
print clust.score

idFilm = 73
print "vous avez aime : " +  str(dataset.movies[idFilm].nom)
listeFilmsSimilaires = []
for i in range(len(clusterAssment)):
    dataset.movies[i].cluster = clusterAssment[i][0,0]
    if(clusterAssment[i][0,0] == clusterAssment[idFilm][0,0] and i!=idFilm):
        listeFilmsSimilaires.append(dataset.movies[i])

listeFilmsSimilaires = sorted(listeFilmsSimilaires, key=operator.attrgetter('avg'),reverse = True)
print "vous aimerez aussi : "

for i in range(0,5):
    if(i < len(listeFilmsSimilaires)):
        print listeFilmsSimilaires[i].nom

reduced_data = reducedDataset[:,0:1]

clusterUsers = Clustering(reduced_data,10)
clusterUsers.kMeans()
clusterAssmentUser = clusterUsers.clusterAssment
centroidsUser = clusterUsers.centroids


import time
users =  dataset.users
k = 20
j = 20
idFilm = 71
ClusterFilm = dataset.movies[idFilm-1].cluster
idFilm = idFilm - 1
print dataset.movies[idFilm].nom
print ClusterFilm
start_time = time.time()
recommandation(k,j,clusterAssmentUser[j-1][0,0],users,reduced_data,dataset,clusterAssmentUser,centroidsUser,ClusterFilm = ClusterFilm,MovieId = idFilm )
print "Temps d'execution : %d secondes" % (time.time() - start_time)

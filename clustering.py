from numpy import *
from notes import Notes
from random import randint
import random as rnd
import math
import numpy as np
import test

class Clustering:
	#Classe qui contient les algorithmes de clustering utilises dans le projet : K-means et Algorithme genetique
	#Nous avons suivi l'implementation du livre de Russel et Norvig pour l'algorithme Genetique
	#Nous avons egalement utilise le livre Machine learning in action pour la mise en place de K-mean
	def __init__(self,dataset,k):
		self.data = dataset
		self.k = k



	### ALGORITHME GENETIQUE
	def distEuclid(self,vecA,vecB):
		#La distance euclidiennne calcule une distance metrique permettant de comparer deux vecteurs
		# return sqrt(sum(power(vecA - vecB,2)))
		return np.linalg.norm(vecA-vecB)

	def randCent(self):
		k = self.k
		#RandCent genere aleatoirement des centroides dans l'espace des donnees
		centroids = mat(zeros((k,self.shape)))
		for j in range(self.shape):
			centroids[:,j] = self.minJ[j] + self.rangeJ[j] * random.rand(k,1)
		return centroids

	def mutate(self,x):
		k = self.k
		#Mutate genere la mutation de l'individu X avec un nouveau centroid genere avec RandCent
		centroid = self.randCent()
		x = np.array(x)
		index = randint(0,k-1)
		x[index] = centroid[index]
		return x

	def createChild(self,x,y,limite):
		#CreateChild est une fonction qui permet de realiser les fonction dite : Crossover
		#qui permettent de croiser les parents pour obtenir une nouvelle solution potentiellement meilleure
		child1 = [0]*len(x)
		child2 = [0]*len(x)
		for i in range(0,len(x)):
			if(i<limite):
				child1[i] = x[i]
				child2[i] = y[i]
			else:
				child1[i] = y[i]
				child2[i] = x[i]

		return child1,child2


	def reproduce(self,x,y):
		#Reproduce est la fonction globale permettant de faire le crossover qui va appeler createChild pour faire tous les
		#crossOver possibles
		children = []
		child1 = []
		child2 = []
		k = len(x)
		limite1 = math.floor(float(k)/3)
		limite2 = math.ceil(float(k)/2)
		child1,child2 = self.createChild(x,y,limite1)
		child3,child4 = self.createChild(x,y,limite2)
		children.append(child1)
		children.append(child2)
		children.append(child3)
		children.append(child4)
	 	return children

	def fitness(self,population):
		#on classe les population en fonction de la longueur de leur chemin, plus le chemin est court plus la note est meilleure
		#On normalise entre 0 et 1 avec l'ensemble des probabilitees = 1 pour effectuer le tirage 
		score_pop = population[:]
		WorstInd = score_pop[len(population)]
		BestInd = score_pop[0]
		inc = (WorstInd-BestInd)
		total = 0.0
		for i in range(len(population)):
			score_pop[i] =((1 - (1.0 * score_pop[i] / WorstInd)) * 5 )
			total = total + score_pop[i]
		for i in range(len(population)):
			score_pop[i] = score_pop[i] / total
		return score_pop


	def random_pick(self,population, probabilities):
		#On effectue le tirage sur la distribution de fitness
	    x = random.uniform(0, 1)
	    cumulative_probability = 0.0
	    for item, item_probability in zip(population, probabilities):
	        cumulative_probability += item_probability
	        if x < cumulative_probability: break
	    return item

	def objectiveFunction(self,individu):
		k = self.k
		#La fonction objective est une fonction qui a pour but de calculer la distance des centroides
		#des donnes, la somme de ces distances permet de savoir que le minimum est le meilleur ensemble de centroides
		clusterAssment = mat(zeros((self.m,2)))
		individu = np.array(individu)
		# print individu
		for i in range(self.m):
			minDist = inf; minIndex = -1
			for j in range(k):
				distJI = self.distEuclid(individu[j,:],self.data[i,:])
				if distJI < minDist:
					minDist = distJI; minIndex = j
			if clusterAssment[i,0] != minIndex: clusterChanged = True
			clusterAssment[i,:] = minIndex,minDist**2

		for cent in range(k):
			ptsInClust = self.data[nonzero(clusterAssment[:,0].A==cent)[0]]
			if(ptsInClust.size != 0):
				individu[cent,:] = mean(ptsInClust, axis=0)

		return individu,np.sum(clusterAssment[:,1]),clusterAssment

	def GA(self,limite):
		k = self.k
		#Algorithme repris de Russel et Norvig
		#Algorithme global genetique incluant le crossover, mutation et selection
		population = []
		newpop = []
		count = 0
		bestIndividuGlobal = 0
		self.shape = shape(self.data)[1]
		listmin = []
		listrange = []
		for j in range(self.shape):
			listmin.append(min(self.data[:,j]))
			listrange.append(float(max(self.data[:,j]) - listmin[j]))
		self.minJ = listmin
		self.rangeJ = listrange
		
		self.m = shape(self.data)[0]
		#Initialisation de la population
		for i in range(limite):
			population.append(self.randCent())

		while count < limite:
			newpop = []
			# print count

			for ind in range(len(population)):
				p = rnd.random()
 				if(p < 0.1):
					population[ind] = self.mutate(population[ind])
				individu, score,clusterAssment = self.objectiveFunction(population[ind])
				population[ind] = (individu,score)

			population = sorted(population, key=lambda ind: ind[1])

			bestIndividuLocal = population[0][1]
			# print bestIndividuGlobal
			# print bestIndividuLocal
			if(bestIndividuGlobal == 0 or bestIndividuLocal < bestIndividuGlobal ):
				individu, score,clusterAssment = self.objectiveFunction(population[0][0])
				bestIndividuGlobal = bestIndividuLocal
				self.score = score
				self.centroids = individu
				self.clusterAssment = clusterAssment
			
			#Generation des tuples des 2 parmi 10 parents	
			for i in range(0,10):
				for j in range(i+1,10):
					newpop = newpop + self.reproduce(population[i][0],population[j][0])
		 	population = newpop
		 	count = count + 1 

		print "Meilleur genetique : " + str(bestIndividuGlobal)
		return bestIndividuGlobal

	def kMeans(self):
		dataSet = self.data
		k = self.k
		self.shape = shape(self.data)[1]
		listmin = []
		listrange = []
		for j in range(self.shape):
			listmin.append(min(self.data[:,j]))
			listrange.append(float(max(self.data[:,j]) - listmin[j]))
		self.minJ = listmin
		self.rangeJ = listrange
		
		self.m = shape(self.data)[0]
		#Algorithne des k-moyennes
		m = shape(dataSet)[0]
		clusterAssment = mat(zeros((m,2)))
		centroids = self.randCent()
		clusterChanged = True
		while clusterChanged:
			clusterChanged = False
			for i in range(m):
				minDist = inf; minIndex = -1
				for j in range(k):
					distJI = self.distEuclid(centroids[j,:],dataSet[i,:])
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
		self.score = np.sum(clusterAssment[:,1])
		self.centroids = centroids
		self.clusterAssment = clusterAssment
		return centroids, clusterAssment
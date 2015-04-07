from numpy import *
class Clustering:
	def __init__(self,data):
		print 'kmeans : '
		self.kmeans(self,data)
		print 'GA : '
		self.geneticAlgorithm(self,data)

	def intersect(self,a, b):
		return list(set(a) & set(b))
	def pcs(self,x,y,notes):
		listallX=[]
		listallnotesX =[]
		listY=[]
		listX=[]
		i=0
		for note in notes:
			if(note.idUser == x.id):
				listallX.append(note.idMovie)
				listallnotesX.append(note)


		for note in notes:
			dansY = False
			dansX = False
			if(note.idMovie in listallX):
				dansX = True
			if(note.idUser == y.id):
				dansY = True
			if(dansX and dansY)
				list.append(note in listallnotesX if listallnotesX.)
				listY.append(note)
		listX = 


	def kmeans(self,data):
		print "not implemented"
	def geneticAlgorithm(self,data):
		print "not implemented"
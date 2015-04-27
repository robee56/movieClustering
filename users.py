from numpy import divide
class User:
	def __init__(self,id,age,genre,profession,codePostal):
		self.id = int(id)
		self.age = int(age)
		self.genre = genre
		self.profession = profession
		self.codePostal = codePostal
		self.vecteurGenreVote = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
		self.vecteurGenre = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
		self.vecteurNormalise = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
		self.avg = 0.0
		self.cluster = 0
		self.listfilms = []

	def normaliserVecteur(self):
		#On normalise le vecteur en fonction de la frequence d'apparition du type
		for valeur in range(len(self.vecteurGenre)):
			if self.vecteurGenre[valeur] == 0:
				self.vecteurGenre[valeur] = 1
		self.vecteurNormalise = divide(self.vecteurGenreVote,max(self.vecteurGenreVote))
		for valeur in range(len(self.vecteurNormalise)):
			self.vecteurNormalise[valeur] = float("{0:.2f}".format(self.vecteurNormalise[valeur]))
		
	def moyenne(self,dataset):
		#On calcule la note moyenne des films notes par l'utilisateur
		Total = 0.0
		iteration = 0.0
		for i in dataset.notes:
			if(i.idUser > self.id):
				break
			if((self.id == i.idUser)):
				Total = Total + i.note
				iteration = iteration + 1
		if(iteration == 0):
			self.avg = 0
		else:
			self.avg = Total/iteration


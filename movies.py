class Movie:
	def __init__(self,id,nom,dateSortie,video_release_date,lienImbd,unknownType,action,adventure,animation,children,
              comedy,crime,documentary,drama,fantasy,filmNoir,horror,musical,mystery,romance,sciFi,thriller,war,western,vecteur):
		self.id = id
		self.nom = nom
		self.dateSortie = dateSortie
		self.video_release_date = video_release_date
		self.lienImbd = lienImbd
		self.unknownType = int(unknownType)
		self.action = int(action)
		self.adventure = int(adventure)
		self.animation = int(animation)
		self.children = int(children)
		self.comedy = int(comedy)
		self.crime = int(crime)
		self.documentary = int(documentary)
		self.drama = int(drama)
		self.fantasy = int(fantasy)
		self.filmNoir = int(filmNoir)
		self.horror = int(horror)
		self.musical = int(musical)
		self.mystery = int(mystery)
		self.romance = int(romance)
		self.sciFi = int(sciFi)
		self.thriller = int(thriller)
		self.war = int(war)
		self.western = int(western)
		self.vecteur = vecteur
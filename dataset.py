from users import User
from movies import Movie
from notes import Notes
import re
import os
import operator
from numpy import multiply,add
import pandas as pd

class Dataset:
	def __init__(self,FileUser,FileMovie,FileNotes):
		self.users = self.loadUser(FileUser)
		self.movies = self.loadMovies(FileMovie)
		self.notes = self.loadNotes(FileNotes)

	def loadUser(self,FileUser):
		file_object = open(FileUser, 'r')
		corpus = file_object.readlines()
		file_object.close()
		users = []
		for j in range(len(corpus)):
			user = corpus[j].replace('\n','')
			m = user.split('|')
			users.append(User(m[0],m[1],m[2],m[3],m[4]))
		return users

	def loadMovies(self,FileMovie):
		file_object = open(FileMovie, 'r')
		corpus = file_object.readlines()
		file_object.close()
		movies = []
		for j in range(len(corpus)):
			movie = corpus[j].replace('\n','')
			m = movie.split('|',24)
			movies.append(Movie(m[0], m[1], m[2], m[3], m[4], m[5], m[6], m[7], m[8], m[9], m[10], \
                m[11], m[12], m[13], m[14], m[15], m[16], m[17], m[18], m[19], m[20], m[21], \
                m[22], m[23],[float(m[5]), float(m[6]), float(m[7]), float(m[8]), float(m[9]), float(m[10]), \
                float(m[11]), float(m[12]), float(m[13]), float(m[14]), float(m[15]), float(m[16]), float(m[17]), float(m[18]), float(m[19]), float(m[20]), float(m[21]), \
                float(m[22]), float(m[23])] ))
		return movies

	def loadNotes(self,FileNotes):
		file_object = open(FileNotes, 'r')
		corpus = file_object.readlines()
		file_object.close()
		notes = []
		for j in range(len(corpus)):
			note = corpus[j].replace('\n','')
			m = note.split('\t')
			notes.append(Notes(m[0],m[1],m[2],m[3]))
		return notes

	def vecteurNotes(self):
		#on affecte a l'utilisateur un vecteur en fonction de ses gouts (ses notes pour chaque film de chaque type ponderees)
		notes = self.notes
		films = self.movies
		users = self.users
		for note in notes:
			user = users[note.idUser-1]
			film = films[note.idMovie-1]
			user.vecteurGenre = add(user.vecteurGenre,film.vecteur)
			user.vecteurGenreVote = add(user.vecteurGenreVote,multiply(film.vecteur,note.note))

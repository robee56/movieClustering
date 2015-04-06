from users import User
from movies import Movie
from notes import Notes
import re
import os

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
                m[22], m[23]))
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



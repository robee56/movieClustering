from dataset import Dataset
from movies import Movie
from notes import Notes
from users import User
import os

currentPath = os.path.dirname(os.path.realpath(__file__))

FileUser = currentPath  + "/data/u.user"
FileMovies = currentPath  + "/data/u.item"
FileNotes = currentPath  + "/data/u.base"

dataset = Dataset(FileUser,FileMovies,FileNotes)
for i in dataset.users:
	print i.profession
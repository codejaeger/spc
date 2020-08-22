import sys
import os.path
from os import path
import pickle

text_file = os.path.expanduser('~/directory_path.pkl')
k = os.path.expanduser(sys.argv[1])

if path.exists(k):
	with open(text_file, 'wb') as fw:
		path1 = os.path.abspath(k)+"/"
		pickle.dump(path1,fw)
		fw.close()
	print("Directory path saved")
else :
	print("No such directory exists")
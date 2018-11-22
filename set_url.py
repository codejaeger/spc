import pickle
import os

k = input()
f = os.path.expanduser('~/server-url.pkl')
with open(f,'wb') as fw:
	pickle.dump(k,fw)
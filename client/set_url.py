import pickle
import os

k1 = input("Enter IP address of server: ")
k2 = input("Enter Port number: ")
f = os.path.expanduser('~/server-url.pkl')
with open(f,'wb') as fw:
	pickle.dump(k1+":"+k2,fw)
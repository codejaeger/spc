import pickle
import os

f = os.path.expanduser('~/server-url.pkl')
with open(f,'rb') as fw:
	k = str(pickle.load(fw))

a = k.split(':')

print('ip address: '+ a[0])
print('Port number: '+ a[1])
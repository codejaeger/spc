import sys
import os.path
from os import path
import pickle

myfile = os.path.expanduser('~/login_details.pkl')

if os.path.isfile(myfile) == False:
    print("You must login for performing this action")
    exit(0)

# url = 'http://192.168.2.1:8000/login/'
# d1url = "http://127.0.0.1:8000/files/download/?name=usrs.BookIndex/bytes/filename/mimetype/a.txt"
# durl = "http://127.0.0.1:8000/files/download/?name=usrs.BookIndex/bytes/filename/mimetype/Graph_and_Trees.pdf"

# client = requests.session()
# client.get(url)
# csrftoken1 = client.cookies['csrftoken']

# with open(myfile, 'r') as fr:
#     count = 1
#     for line in fr:
#         if count == 1:
#             u = line[:-1]
#         elif count == 2:
#             p = line[:-1]
#         count+=1

# print(u)
# print(p)

# login_data = dict(username=u, password=p, csrfmiddlewaretoken=csrftoken1)
# r1 = client.post(url, data=login_data)
# print(r1.url)


text_file = os.path.expanduser('~/encryption_scheme.pkl')

if sys.argv[1]=='list':
	print('1. AES')
	print('2. RSA')
else:
	if len(sys.argv)==2 and sys.argv[1]=='update':
		print('Do you want to update the data on the server?')
		ans = input('Y/N')
		if ans == 'Y':
			oldenc = os.path.expanduser('~/old_encryption_scheme.pkl')
			with open(oldenc,'wb') as fw:
				with open(text_file, 'rb') as fr:
					for l in fr:
						pickle.dump(l,fw)
		a = input("Schema used: ")
		if a == 'AES':
			k = input("Key: ")
			pas = input("Passphrase: ")
			with open(text_file,'wb') as fw:
				pickle.dump(['AES',pas],fw)
		elif a == 'RSA':
			with open(text_file,'wb') as fw:
				pickle.dump('RSA',fw)
		else:
			print("Wrong Schema")
			print("Use 'spc en-de list' to view available choices")
			exit(0)

	else:
		fn = os.path.expanduser(sys.argv[2])
		if sys.argv[1]=='update':
			print('Do you want to update the data on the server?')
			ans = input('Y/N')
			if ans == 'Y':
				oldenc = os.path.expanduser('~/old_encryption_scheme.pkl')
				with open(oldenc,'wb') as fw:
					with open(text_file, 'rb') as fr:
						for l in fr:
							pickle.dump(l,fw)
			with open(f,'wb') as fw:
				pickle.dump('1',fw)
			with open(text_file,'wb') as fw:
				with open(fn, 'rb') as fr:
					for l in fr:
						pickle.dump(l,fw)
		elif sys.argv[1]=='dump':
			with open(fn, 'wb') as fw:
				with open(text_file,'rb') as fr:
					for l in fr:
						pickle.dump(l,fw)
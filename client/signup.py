import os
import requests 
import pickle
import getpass

u = input("Username: ")
email = input("Email: ")
p = getpass.getpass("Password: ")
np = getpass.getpass("Password confirmation: ")

if p!=np:
	print("Passwords do not match")
	print("Try again")
else:
	f = os.path.expanduser('~/server-url.pkl')
	with open(f,'rb') as fr:
		ip = pickle.load(fr)
	url = 'http://'+ ip +'/signup/'
	client = requests.session()
	client.get(url)
	csrftoken = client.cookies['csrftoken']
	signup_data = {'username':u, 'password1':p,'email':email,'password2':p,'csrfmiddlewaretoken':csrftoken}
	r = client.post(url, data=signup_data)
	if r.status_code != 200 and r.url == url:
		print("Some Error Occurred")
	else:
		print("Successfully signed up")
	# print(r.content)

import os

myfile = os.path.expanduser('~/login_details.pkl')
if os.path.isfile(myfile):
	os.remove(myfile)
	print("logout successful")
else:
	print("You have not login") 

import os

myfile = 'login_details.txt'
if os.path.isfile(myfile):
	os.remove(myfile)
	print("logout successful")
else:
	print("You have not login") 
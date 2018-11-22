import os
import requests 
import pickle

print(1)
u = input("Enter username: ")
p = input("Enter password: ")

f = os.path.expanduser('~/server-url.pkl')
with open(f,'rb') as fr:
	ip = pickle.load(fr)

url = 'http://'+ ip +'/login/'
print(url)

client = requests.session()
client.auth = (u,p)
client.headers.update({'x-test': 'true'})

# Retrieve the CSRF token first

client.get(url, headers={'x-test2': 'true'})  # sets the cookie
csrftoken = client.cookies['csrftoken']

login_data = dict(username=u, password=p, csrfmiddlewaretoken=csrftoken)
r = client.post(url, data=login_data)

k = os.path.expanduser('~/somefile.pkl')
with open(k, 'wb') as f:
    pickle.dump(client.cookies, f)

print(r.url)

url = '%s%s%s'%(r.url[:-4],'fls',r.url[-1:])


print(url)
# client.get(r.url)
# csrftoken = client.cookies['csrftoken']
# files = {'index': open('abcd/b.txt','rb')}
# values = {'ownr': 3, 'name': 'abcd/b.txt', 'csrfmiddlewaretoken': csrftoken}
# r = client.post(r.url, files=files, data=values)

text_file = os.path.expanduser('~/login_details.pkl')
upload_file = os.path.expanduser('~/upload_file.pkl')

# values = {'username': u, 'password': p}
# resp = requests.get(url,data=values)
# print(r.status_code)
# print(r.content)
# print(r.headers)
# print(r.content[1])
# print(r.url)
# soup = BeautifulSoup(r.content,features="html.parser")
# title = soup.find('title')

#This outputs the content :)
# print(resp.cookies)
# print(resp.history)
# cookies = dict(sessionid=resp.cookies.get('sessionid'))
# csrftoken = resp.cookies['csrftoken'];
# # cookie = {'csrftoken': cookies}
# # print(cookies)
# # print(cookie)
# # body_data = resp.text
# # print(body_data)

# second_url = 'http://0.0.0.0:8000/model_files/add/'
# resp1 = requests.post(second_url,data=values,headers= {
#       'X-CSRFToken': csrftoken
#     })
# print(resp1.status_code)
# body_data1 = resp1.text
# print(body_data1)

# cookies = dict(sessionid=resp.cookies.get('sessionid'))
# b = False

if r.url == url and r.status_code == 200:
	print("Wrong username or password")
else:
	with open(text_file, 'wb') as fw:
		pickle.dump([u,p,url],fw)
	with open(upload_file, 'wb') as fw:
	    pickle.dump(r.url, fw)
	print("login successful")

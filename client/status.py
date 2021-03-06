import requests
import os
import pickle
import shutil
from bs4 import BeautifulSoup
import html 
import hashlib

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

lse = []
lin = []
lco = []

with open(myfile, 'rb') as fs:
    u,p,url = pickle.load(fs)

# print(url)

l = []

fname = os.path.expanduser('~/directory_path.pkl')
with open(fname, 'rb') as fs:
    directory = pickle.load(fs)

upload_file = os.path.expanduser('~/upload_file.pkl')

# print(directory)
with open(upload_file, 'rb') as fs:
    upload_url = pickle.load(fs)

inputd = {}
md5 = {}
def fillinputd():
    for (dirpath, dirnames, filenames) in os.walk(directory):
        # print(filenames)
        for filename in filenames:
            reldir = os.path.relpath(dirpath, directory)
            # print(reldir)
            if reldir != ".":
                relFile = os.path.join(reldir, filename)
            else:
                relFile = filename
            hash_md5 = hashlib.md5()
            full_name = directory + relFile
            with open(full_name, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            md5[relFile] = hash_md5.hexdigest()
            if filename[0]!='.':
                inputd[relFile]=0

    
def sync():
    client = requests.session()
    k = os.path.expanduser('~/somefile.pkl')
    with open(k, 'rb') as f:
        client.cookies.update(pickle.load(f))
    client.auth = (u,p)
    client.headers.update({'x-test': 'true'})
    # g = client.get(upload_url,cookies=client.cookies, headers={'x-test2': 'true'})
    # client.get(upload_url)
    # csrftoken = client.cookies['csrftoken']
    csrftoken = client.cookies['csrftoken']
    # files = {'index': open(filename,'rb')}
    # values = {'ownr': 1, 'name': filename,'md5s': 'vsdhabhja', 'username': 'sed4','csrfmiddlewaretoken': csrftoken,'password': 'Shubham123', 'deb': 1}
    r = client.get(url)
    soup = BeautifulSoup(r.content,features="html.parser")
    # print(1)
    tables = soup.findChildren('table')
    if len(tables)!=0:
        # print(2)
        # print(tables)
        my_table = tables[0]
        # print(3)
        # print(my_table)
        rows = my_table.findChildren('tr')
        # print(4)
        # print(rows)
        for row in rows:
         # print(row)
         cells = row.findChildren('td')
         k1 = cells[0].find('a').contents[0]
         k2 = cells[1].find('a')['href']
         k3 = cells[4].text
         k3 = k3[1:-1]
         # p = k2[0].find('a',href=True)
         # print(cells[1].find('a'))
         # print(k1)
         # # print(k2)
         # print(k3)
         # print("")
         temp = []
         temp.append(k1)
         temp.append(k2)
         temp.append(k3)
         l.append(temp)

def fun():
    for item in l:
        # print(item[0])
        full_name = directory + item[0]
        if os.path.isfile(full_name) == False:
            lse.append(item[0])
        else:
            # print(len(md5[item[0]]))
            if md5[item[0]] == item[2]:
                inputd[item[0]] = 1
            else:
                lse.append(item[0])
    for key,values in inputd.items():
        if values == 0:
            lin.append(key)
        else:
            lco.append(key)

def mprint():
    print('Files present only on server')
    for item in lse:
        print(item)
    print('Files present only on client')
    for item in lin:
        print(item)
    print('Files present on server as well as client')
    for item in lco:
        print(item)


fillinputd()
print(inputd)
sync()
fun()
mprint()

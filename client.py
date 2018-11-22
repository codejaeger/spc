import requests
import os
import pickle
import shutil
from bs4 import BeautifulSoup
import html , subprocess
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

with open(myfile, 'rb') as fs:
    u,p,url = pickle.load(fs)

print(url)
slashparts = url.split('/')
basename = '/'.join(slashparts[:3])

l = []
inputd={}

fname = os.path.expanduser('~/directory_path.pkl')
with open(fname, 'rb') as fs:
    directory = pickle.load(fs)

upload_file = os.path.expanduser('~/upload_file.pkl')

print(directory)
with open(upload_file, 'rb') as fs:
    upload_url = pickle.load(fs)

encr_file = os.path.expanduser('~/encryption_scheme.pkl')
with open(encr_file, 'rb') as fs:
    a = pickle.load(fs)

sch = a[0]
if sch == 'AES':
    passcode = a[1]

old_encr = os.path.expanduser('~/old_encryption_scheme.pkl')
try:
    os.path.isfile(old_encr)
    with open(old_encr, 'rb') as fs:
        a = pickle.load(fs)
    osch = a[0]
    if osch == 'AES':
        opasscode = a[1]
except:
    print('')
    



# file = 'encodedmd5.pickle'
# with open(file,'wb') as fw:
# inputd = pickle.load(fw)

md5 = {}
def fillinputd():
    for (dirpath, dirnames, filenames) in os.walk(directory):
        print(filenames)
        for filename in filenames:
            reldir = os.path.relpath(dirpath, directory)
            print(reldir)
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
         print(cells[1].find('a'))
         print(k1)
         # print(k2)
         print(k3)
         print("")
         temp = []
         temp.append(k1)
         temp.append(k2)
         temp.append(k3)
         l.append(temp)

def download():
    for item in l:
        full_name = directory + item[0]
        if os.path.isfile(full_name) == False:
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
            values = {'username': u,'csrfmiddlewaretoken': csrftoken,'password': p, 'check1': 1}    
            t = client.post(basename+item[1], data=values)
            print(item[0])
            if sch == 'AES':
                end = '.gpg'
            with open(full_name+end,'wb') as f:
                f.write(t.content)
            if sch == 'AES':
                print(full_name+end)
                subprocess.call(['gpg', '--yes', '--batch', '--passphrase="passcode"', full_name+end])
                # subprocess.call(['rm', full_name+end])
            hash_md5 = hashlib.md5()
            with open(full_name, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            temp = hash_md5.hexdigest()
            if temp != item[2]:
                print("File " + item[0] + " got corrupted while downloading")
                print("Please download it again") 
        else:
            print(type(md5[item[0]]))
            print(type(item[2]))
            print(md5[item[0]])
            print(len(item[2]))
            if md5[item[0]] == item[2] and os.path.isfile(old_encr)==False:
                inputd[item[0]] = 1
            else:
                if os.path.isfile(old_encr)==True:
                    k = 'S'
                else:
                    print('File with name '+ full_name + ' exist both on server and client' )
                    print('If you want to keep both files, then terminate the sync process and change file name')
                    print('Warning : If you continue then one of the file content is lost')
                    print('Type S(For overloading your file with server file)')
                    print('Type C(For overloading server file with your file)')
                    k = input()
                if k == 'S':
                    if os.path.isfile(old_encr)==False:
                        inputd[item[0]] = 1
                    client = requests.session()
                    os.remove(full_name)
                    k = os.path.expanduser('~/somefile.pkl')
                    with open(k, 'rb') as f:
                        client.cookies.update(pickle.load(f))
                    client.auth = (u,p)
                    client.headers.update({'x-test': 'true'})
                    # g = client.get(upload_url,cookies=client.cookies, headers={'x-test2': 'true'})
                    # client.get(upload_url)
                    # csrftoken = client.cookies['csrftoken']
                    csrftoken = client.cookies['csrftoken']
                    values = {'username': u,'csrfmiddlewaretoken': csrftoken,'password': p, 'check1': 1}    
                    t = client.post(basename+item[1], data=values)
                    print(item[0])
                    if os.path.isfile(old_encr)==False:
                        if sch == 'AES':
                            end = '.gpg'
                    else:
                        if osch == 'AES':
                            end = '.gpg'
                    with open(full_name+end,'wb') as f:
                        f.write(t.content)
                        f.close()
                    if os.path.isfile(old_encr)==False:
                        if sch == 'AES':
                            subprocess.call(['gpg', '--yes', '--batch', '--passphrase=passcode', full_name+end])
                            subprocess.call(['rm', full_name+'.gpg'])
                    else:
                        if osch == 'AES':
                            subprocess.call(['gpg', '--yes', '--batch', '--passphrase=opasscode', full_name+end])
                            subprocess.call(['rm', full_name+'.gpg'])
                    hash_md5 = hashlib.md5()
                    with open(full_name, "rb") as f:
                        for chunk in iter(lambda: f.read(4096), b""):
                            hash_md5.update(chunk)
                    temp = hash_md5.hexdigest()
                    if temp != item[2]:
                        print("File " + item[0] + " got corrupted while downloading")
                        print("Please download it again")
                elif k != 'C':
                    print('The option you entered is invalid')
                    exit(0)




def upload():
    for key,values in inputd.items():
        if values == 0:           
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
            key1 = directory + key
            print(key)
            if sch == 'AES':
                end = '.gpg'
                subprocess.call(['gpg', '--yes', '--batch', '--passphrase=passcode', '-c', key1])
            hash_md5 = hashlib.md5()
            with open(key1+end, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            temp = hash_md5.hexdigest()
            print(temp)
            print(len(temp))
            files = {'index': open(key1+end,'rb')}
            values = {'encpt_key': 'wvdehj','md5se':temp ,'en_schm':"dsf",'sharing': 'sdfs', 'name': key,'md5so': md5[key], 'username': u,'csrfmiddlewaretoken': csrftoken,'password': p, 'check1': 1}    
            r = client.post(upload_url, files=files, data=values)
            subprocess.call(['rm', key1+end])
# def md5_sum()
   
fillinputd()
print(inputd)
sync()
print(l)
download()
upload()

if os.path.isfile(old_encr)==True:
    os.remove(old_encr)

# if os.path.isfile(directory_path):
#     print("If you want to upload all files in your observing directory, enter 1")
#     print("(If some file is already uploaded then it will not get reuploaded even if some changes are made)")
#     print("If you want to upload a particular file, enter 2")
#     t = int(input(">> "))
#     if t == 1:
#         with open(directory_path, 'rb') as fs:
#             directory = fs.read().decode('ascii')
#         upload_directory()
#     else:
#         filename = input("Enter the path of file to be uploaded: ")
#         filename = os.path.abspath(filename)
#         upload_file(filename)
# else:
#     filename = input("Enter the path of file to be uploaded: ")
#     filename = os.path.abspath(filename)
#     upload_file(filename)



# text_file = 'login_details.txt'

# with open(text_file, 'rb') as fs:
#     count = 1
#     for line in fs:
#         if count == 3 :
#             csrftoken = line.decode('ascii')
#         else:
#             count+=1;

# print(csrftoken)



# def directory_server():
#     r = requests.get(url_for_sending_back_csv_containing_files_with_their_md5sum)

# directory_server()

# compare r with the directory structure of the client and then sync

# for root, dirs, files in os.walk(directory):
#     level = root.replace(os.getcwd(), '').count(os.sep)
#     indent = ' ' * 4 * (level)
#     str1 += '{}{}/'.format(indent, os.path.basename(root))
#     str1 += '\n'
#     subindent = ' ' * 4 * (level + 1)
#     for f in files:
#         str1 += '{}{}'.format(subindent, f)
#         str1 += '\n'
#     data = bytes(str1, 'utf-8')
#     csFT.sendall(data)

# upload_url = 'http://0.0.0.0:8000/model_files/add/'


# client = requests.session()
# client.get(upload_url)  # sets the cookie
# csrftoken = client.cookies['csrftoken']

# with open(text_file, 'wb') as fw:
#         fw.write(bytes(u, 'utf-8'))
#         fw.write(bytes("\n", 'utf-8'))
#         fw.write(bytes(p, 'utf-8'))
#         fw.close()

# files = {'Index': open(directory + 'login_details.txt','rb')}
# files = {'index': open('ssl-quiz3/RMO.pdf','rb')}
# values = {'ownr': 2, 'name': 'RMO', 'csrfmiddlewaretoken': csrftoken}
# r = client.post(upload_url, files=files, data=values)
# # print(r.status_code)
# # print(r.content)
# if r.status_code == 200:
#     print("Uploaded file successfully")
# else:
#     print("Some error ocurred while uploading file")

# download_url = 'http://192.168.2.1:8000/model_files/add/'





# str1 =""
# for root, dirs, files in os.walk(directory):
#     level = root.replace(os.getcwd(), '').count(os.sep)
#     indent = ' ' * 4 * (level)
#     str1 += '{}{}/'.format(indent, os.path.basename(root))
#     str1 += '\n'
#     subindent = ' ' * 4 * (level + 1)
#     for f in files:
#         str1 += '{}{}'.format(subindent, f)
#         str1 += '\n'
#     data = bytes(str1, 'utf-8')
#     csFT.sendall(data)

# #Send file
# with open(text_file, 'rb') as fs:
#     #Using with, no file close is necessary,
#     #with automatically handles file close
#     #csFT.send(b'BEGIN')
#     while True:
#         data = fs.read(1024)
#         print('Sending data', data.decode('utf-8'))
#         csFT.send(data)
#         print('Sent data', data.decode('utf-8'))
#         if not data:
#             print('Breaking from sending data')
#             break
#     csFT.sendall(b'exit')
#     fs.close()
 
# #Receive file
# print("Receiving..")
# with open(text_file, 'wb') as fw:
#     while True:
#         data = csFT.recv(1024)
#         if not data:
#             break
#         fw.write(data)
#     fw.close()
# print("Received..")
 
# csFT.close()



# files = {'upload_file': open('file.txt','rb')}
# values = {'DB': 'photcat', 'OUT': 'csv', 'SHORT': 'short'}

# r = requests.post(url, files=files, data=values)
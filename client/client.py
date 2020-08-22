import requests
import os
import base64
import pickle
import shutil
from bs4 import BeautifulSoup
import html , subprocess
import hashlib
import io
import pyAesCrypt
from Crypto import Random
import hashlib
from Crypto.Cipher import AES
import os
import os.path
from os import listdir
from os.path import isfile, join
import time
#from tqdm import tqdm
import math
from pyDes import *
import codecs
import blowfish
import progressbar

# def KSA(key):
#     ''' Key Scheduling Algorithm (from wikipedia):
#         for i from 0 to 255
#             S[i] := i
#         endfor
#         j := 0
#         for i from 0 to 255
#             j := (j + S[i] + key[i mod keylength]) mod 256
#             swap values of S[i] and S[j]
#         endfor
#     '''
#     key_length = len(key)
#     # create the array "S"
#     S = list(range(MOD))  # [0,1,2, ... , 255]
#     j = 0
#     for i in range(MOD):
#         j = (j + S[i] + key[i % key_length]) % MOD
#         S[i], S[j] = S[j], S[i]  # swap values

#     return S


# def PRGA(S):
#     ''' Psudo Random Generation Algorithm (from wikipedia):
#         i := 0
#         j := 0
#         while GeneratingOutput:
#             i := (i + 1) mod 256
#             j := (j + S[i]) mod 256
#             swap values of S[i] and S[j]
#             K := S[(S[i] + S[j]) mod 256]
#             output K
#         endwhile
#     '''
#     i = 0
#     j = 0
#     while True:
#         i = (i + 1) % MOD
#         j = (j + S[i]) % MOD

#         S[i], S[j] = S[j], S[i]  # swap values
#         K = S[(S[i] + S[j]) % MOD]
#         yield K


# def get_keystream(key):
#     ''' Takes the encryption key to get the keystream using PRGA
#         return object is a generator
#     '''
#     S = KSA(key)
#     return PRGA(S)


# def encrypt_logic(key, text):
#     ''' :key -> encryption key used for encrypting, as hex string
#         :text -> array of unicode values/ byte string to encrpyt/decrypt
#     '''
#     # For plaintext key, use this
#     key = [ord(c) for c in key]
#     # If key is in hex:
#     # key = codecs.decode(key, 'hex_codec')
#     # key = [c for c in key]
#     keystream = get_keystream(key)

#     res = []
#     for c in text:
#         val = ("%02X" % (c ^ next(keystream)))  # XOR and taking hex
#         res.append(val)
#     return ''.join(res)


# def encode3(key, plaintext):
#     ''' :key -> encryption key used for encrypting, as hex string
#         :plaintext -> plaintext string to encrpyt
#     '''
#     plaintext = [ord(c) for c in plaintext]
#     return encrypt_logic(key, plaintext)


# def decode3(key, ciphertext):
#     ''' :key -> encryption key used for encrypting, as hex string
#         :ciphertext -> hex encoded ciphered text using RC4
#     '''
#     ciphertext = codecs.decode(ciphertext, 'hex_codec')
#     res = encrypt_logic(key, ciphertext)
#     return codecs.decode(res, 'hex_codec').decode('utf-8')

# def encode3(key, clear):
#     enc = []
#     for i in range(len(clear)):
#         key_c = key[i % len(key)]
#         enc_c = chr((ord(clear[i]) + ord(key_c)) % 256)
#         enc.append(enc_c)
#     return base64.urlsafe_b64encode("".join(enc).encode()).decode()

# def decode3(key, enc):
#     dec = []
#     enc = base64.urlsafe_b64decode(enc).decode()
#     for i in range(len(enc)):
#         key_c = key[i % len(key)]
#         dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)
#         dec.append(dec_c)
#     return "".join(dec)

class Encryptor:
    def __init__(self, key):
        self.key = hashlib.sha256(key.encode()).digest()

    def pad(self, s):
        return s + b"\0" * (AES.block_size - len(s) % AES.block_size)

    def encrypt(self, message, key_size=256):
        message = self.pad(message)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return iv + cipher.encrypt(message)

    # def encrypt_file(self, file_name):
    #     with open(file_name, 'rb') as fo:
    #         plaintext = fo.read()
    #     enc = self.encrypt(plaintext)
    #     with open(file_name + ".txt", 'wb') as fo:
    #         fo.write(enc)
    #     os.remove(file_name)

    def decrypt(self, ciphertext):
        iv = ciphertext[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        plaintext = cipher.decrypt(ciphertext[AES.block_size:])
        return plaintext.rstrip(b"\0")

    # def decrypt_file(self, file_name):
    #     with open(file_name, 'rb') as fo:
    #         ciphertext = fo.read()
    #     dec = self.decrypt(ciphertext)
    #     with open(file_name[:-4], 'wb') as fo:
    #         fo.write(dec)
    #     os.remove(file_name)

    # def getAllFiles(self):
    #     dir_path = os.path.dirname(os.path.realpath(__file__))
    #     dirs = []
    #     for dirName, subdirList, fileList in os.walk(dir_path):
    #         for fname in fileList:
    #             if (fname != 'script.py' and fname != 'data.txt.enc'):
    #                 dirs.append(dirName + "\\" + fname)
    #     return dirs

    # def encrypt_all_files(self):
    #     dirs = self.getAllFiles()
    #     for file_name in dirs:
    #         self.encrypt_file(file_name)

    # def decrypt_all_files(self):
    #     dirs = self.getAllFiles()
    #     for file_name in dirs:
    #         self.decrypt_file(file_name)

global count1 
count1 = 0
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

# print(url)
slashparts = url.split('/')
basename = '/'.join(slashparts[:3])

l = []
inputd={}

fname = os.path.expanduser('~/directory_path.pkl')
with open(fname, 'rb') as fs:
    directory = pickle.load(fs)

upload_file = os.path.expanduser('~/upload_file.pkl')

# print(directory)
with open(upload_file, 'rb') as fs:
    upload_url = pickle.load(fs)

encr_file = os.path.expanduser('~/encryption_scheme.pkl')
with open(encr_file, 'rb') as fs:
    a = pickle.load(fs)

sch = a[0]
passcode = a[1]
if sch == 'blowfish':
    niv = a[2]
    # print('blowfish')
    # print(niv)

old_encr = os.path.expanduser('~/old_encryption_scheme.pkl')

if os.path.isfile(old_encr) == False:
    scheme = sch
    if sch == 'AES':
        enc = Encryptor(passcode)
    elif sch == 'DES':
        enc = des("DESCRYPT", CBC, passcode, pad=None, padmode=PAD_PKCS5)
    elif sch == 'blowfish':
        enc = blowfish.Cipher(passcode.encode())
        iv1 = niv
else:
    # print('2')
    with open(old_encr, 'rb') as fs:
        a = pickle.load(fs)
    osch = a[0]
    opasscode = a[1]
    scheme = osch
    if osch == 'AES':
        enc = Encryptor(opasscode)
    elif osch == 'DES':
        enc = des("DESCRYPT", CBC, opasscode, pad=None, padmode=PAD_PKCS5)
    elif osch == 'blowfish':
        enc = blowfish.Cipher(opasscode.encode())
        oiv = a[2]
        iv1 = oiv

# print(sch)
# print(osch)
# file = 'encodedmd5.pickle'
# with open(file,'wb') as fw:
# inputd = pickle.load(fw)

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
         temp = []
         temp.append(k1)
         temp.append(k2)
         temp.append(k3)
         l.append(temp)

def download():
    global count1
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
            k = item[1].split("=")
            values = {'name': k[1],'username': u,'csrfmiddlewaretoken': csrftoken,'password': p, 'check1': 1} 
            print('Downloading '+item[0]+" ...")   
            t = client.post(basename+item[1], data=values)
            end = '.txt'
            if scheme == 'blowfish':
                plaintxt = b"".join(enc.decrypt_cfb(t.content, iv1))
            else:
                plaintxt = enc.decrypt(t.content)
            # print(plaintxt)
            directory1 = os.path.dirname(full_name)
            try:
                    os.stat(directory1)
            except:
                    os.mkdir(directory1) 
            with open(full_name,'wb') as f:
                    # print("Preparing to download "+full_name)
                    f.write(plaintxt)
                # if total_size != 0 and wrote != total_size:
                #     print("ERROR, something went wrong") 
            #     fciph = io.BytesIO(t.content)
            #     fdec = io.BytesIO()
            #     ctlen = len(fciph.getvalue())
            #     fciph.seek(0)
            #     pyAesCrypt.decryptStream(fciph,fdec,"a",64*1024,ctlen)
            #     tofile = fdec.getvalue().decode("utf-8")
            #     # tofile = base64.b64decode(fdec.getvalue())
            #     print(type(tofile))
            # with open(full_name,'w') as f:
            #     f.write(tofile)
            # if sch == 'AES':
            #     print(full_name+end)
                # subprocess.call(['gpg', '--yes', '--batch', '--passphrase="passcode"', full_name+end])
            hash_md5 = hashlib.md5()
            with open(full_name, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            temp = hash_md5.hexdigest()
            count1 = count1 + 1
            bar.update(count1)
            print("")
            if temp != item[2]:
                print("File " + item[0] + " got corrupted while downloading")
                print("Please download it again") 
        else:
            # print(type(md5[item[0]]))
            # print(type(item[2]))
            # print(md5[item[0]])
            # print(len(item[2]))
            if md5[item[0]] == item[2] and os.path.isfile(old_encr)==False:
                inputd[item[0]] = 1
                count1 = count1 + 2
                bar.update(count1)
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
                    k = item[1].split("=")
                    csrftoken = client.cookies['csrftoken']
                    print('Downloading '+item[0]+" ...")
                    values = {'username': u,'name':k[1],'csrfmiddlewaretoken': csrftoken,'password': p, 'check1': 1}    
                    t = client.post(basename+item[1], data=values)
                    # print(item[0])
                    # print(scheme)
                    # print(scheme+'.-.-.-.-.-.-.-')
                    if scheme == 'AES':
                        plaintxt = enc.decrypt(t.content)
                    elif scheme == 'DES':
                        plaintxt = enc.decrypt(t.content, padmode=PAD_PKCS5)
                    elif scheme == 'blowfish':
                        plaintxt = b"".join(enc.decrypt_cfb(t.content, iv1))
                    # print(plaintxt)
                    with open(full_name,'wb') as f:
                        f.write(plaintxt)
                            # subprocess.call(['gpg', '--yes', '--batch', '--passphrase=opasscode', full_name+end])
                            # subprocess.call(['rm', full_name+'.gpg'])
                    hash_md5 = hashlib.md5()
                    # print(full_name)
                    with open(full_name, "rb") as f:
                        for chunk in iter(lambda: f.read(4096), b""):
                            hash_md5.update(chunk)
                    temp = hash_md5.hexdigest()
                    if os.path.isfile(old_encr)==True:
                        count1 = count1 + 1
                    else:
                        count1 = count1 + 2
                    bar.update(count1)
                    print("")
                    if temp != item[2]:
                        print("File " + item[0] + " got corrupted while downloading")
                        print("Please download it again")
                elif k == 'C':
                    count1 = count1 + 1
                    bar.update(count1)
                    print("")
                else:
                    print('The option you entered is invalid')
                    exit(0)




def upload():
    global count1
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
            # print(key1)
            end = '.txt'
            if scheme == 'AES':
                # print('3')
                # enc.encrypt_file(key1)
                # new
                with open(key1, "rb") as fIn:
                    with open(key1+end, "wb") as fOut:
                        data = fIn.read()
                        fOut.write(enc.encrypt(data))
            elif scheme == 'DES':
                # print('2')
                with open(key1, "rb") as fIn:
                    with open(key1+end, "wb") as fOut:
                        data = fIn.read()
                        fOut.write(enc.encrypt(data))
            elif scheme == 'blowfish':
                # print('1')
                with open(key1, "rb") as fIn:
                    with open(key1+end, "wb") as fOut:
                        # print('1')
                        data = fIn.read()
                        fOut.write(b"".join(enc.encrypt_cfb(data, iv1)))
            hash_md5 = hashlib.md5()
            with open(key1+end, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            temp = hash_md5.hexdigest()
            # print(temp)
            # print(len(temp))
            files = {'index': open(key1+end,'rb')}
            values = {'encpt_key': 'wvdehj','md5se':temp ,'en_schm':"dsf",'sharing': 'sdfs', 'name': key,'md5so': md5[key], 'username': u,'csrfmiddlewaretoken': csrftoken,'password': p, 'check1': 1}    
            print('Uploading '+key1+" ...")
            r = client.post(upload_url, files=files, data=values)
            # new
            # if scheme == 'AES':
            #     enc.decrypt_file(key1+end)
            # else:
            subprocess.call(['rm', key1+end])
            count1 = count1 + 1
            bar.update(count1)
            print("")
   
fillinputd()
# print(inputd)
sync()
# total_size = len(inputd)+len(l); 
# wrote = 0 
# print(l)

tempv = len(inputd)+len(l)
bar = progressbar.ProgressBar(maxval=tempv, widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
bar.start()

download()
if os.path.isfile(old_encr) == True:
        scheme = sch
        if sch == 'AES':
            enc = Encryptor(passcode)
        elif sch == 'DES':
            enc = des("DESCRYPT", CBC, passcode, pad=None, padmode=PAD_PKCS5)
        elif sch == 'blowfish':
            enc = blowfish.Cipher(passcode.encode())
            iv1 = niv
upload()

if os.path.isfile(old_encr)==True:
    os.remove(old_encr)
print("")


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

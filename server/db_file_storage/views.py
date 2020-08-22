# third party


from Crypto import Random
import hashlib
from Crypto.Cipher import AES
import os
import os.path
from os import listdir
from os.path import isfile, join
import time



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

    def encrypt_file(self, file_name):
        with open(file_name, 'rb') as fo:
            plaintext = fo.read()
        enc = self.encrypt(plaintext)
        with open(file_name + ".enc", 'wb') as fo:
            fo.write(enc)
        os.remove(file_name)

    def decrypt(self, ciphertext):
        iv = ciphertext[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        plaintext = cipher.decrypt(ciphertext[AES.block_size:])
        return plaintext.rstrip(b"\0")

    def decrypt_file(self, file_name):
        with open(file_name, 'rb') as fo:
            ciphertext = fo.read()
        dec = self.decrypt(ciphertext)
        with open(file_name[:-4], 'wb') as fo:
            fo.write(dec)
        os.remove(file_name)



import blowfish
from pyDes import *
from django.http import HttpResponse, HttpResponseBadRequest
from django.utils.translation import ugettext as _
from wsgiref.util import FileWrapper
# project
import base64
from django.core.exceptions import ValidationError
from db_file_storage.storage import DatabaseFileStorage
from django.contrib.auth.decorators import login_required
import io , sys
from django.shortcuts import render, redirect
import pyAesCrypt
from django.core.files.base import ContentFile 
storage = DatabaseFileStorage()

@login_required
def get_file(request, add_attachment_headers):

    name = request.GET.get('name')
    if 'check1' in request.POST:
    # bf = 64 * 1024
        name = request.POST.get('name')
        # raise ValidationError(request.POST)

        try:
    #     raise ValidationError('Hello')
    #     _file = storage.open(name)
    #     _fin = io.BytesIO(_file)
    #     _fdec = io.BytesIO()
    #     pyAesCrypt.decryptStream(_fin,_fdec,password,bf,len(_fin.getvalue()))
    #     _file=_fcip.getvalue()
        # raise ValidationError(request.POST)
            _file = storage._openlnx(name)
    # _fill = base64.b64decode(_fil)
    # _fin = io.BytesIO(_fill)
    # _fdec = io.BytesIO()
    # pyAesCrypt.decryptStream(_fin,_fdec,password,bf,len(_fin.getvalue()))
    # _file=storage._getme(_fdec.getvalue())
    # raise ValidationError(_file.mimetype)

        except Exception:
            return HttpResponseBadRequest(('Invalid request'))
        response = HttpResponse(
            FileWrapper(_file),
            content_type=_file.mimetype
            )
        response['Content-Length'] = _file.tell()
        if add_attachment_headers:
            response['Content-Disposition'] = \
                'attachment; filename=%(name)s' % {'name': _file.filename}

    else:
        # raise ValidationError(request.POST)

        try:
            password=request.session['key']
            schm = request.session['scm']
        except Exception:
            return redirect('model_files:book.scm')
        # storage.itii()
        # scm = request.session['scm']
    #     raise ValidationError('Hello')
    #     _file = storage.open(name)
    #     _fin = io.BytesIO(_file)
    #     _fdec = io.BytesIO()
    #     pyAesCrypt.decryptStream(_fin,_fdec,password,bf,len(_fin.getvalue()))
    #     _file=_fcip.getvalue()
        try:
        # _fil = storage.open(name,password)[1]
            if schm == "aes":
                _file = storage.open(name,password)
                # raise ValidationError(type(_fil))
                enc = Encryptor(password)
                # raise ValidationError(_gb.open('rb').read())
                plt = enc.decrypt(_file.open('rb').read())
                # raise ValidationError(plt)

                gb1 = ContentFile(plt)
                _file.close()
            elif schm == "des":
                _file = storage.open(name,password)
                # raise ValidationError(type(_fil))
                enc = des("DESCRYPT", CBC, password , pad=None , padmode =PAD_PKCS5)
                plt = enc.decrypt(_file.open('rb').read())
                gb1 = ContentFile(plt)
                _file.close()
            elif schm == 'bf':
                _file = storage.open(name,password)
                enc = blowfish.Cipher(password.encode())
            
            # iv1 = os.urandom(8)
            # raise ValidationError(iv1)
                iv1=b"\xf9\x11\xeb\x8a\x871\x98\x89"
                plt = b"".join(enc.decrypt_cfb(_file.open('rb').read(),iv1))
                # raise ValidationError(plt)

                gb1 = ContentFile(plt)
                _file.close()
            # _file.close()
            # raise ValidationError(plt)

        # _file.close()
        # with _file.open('wb') as f:
        #     f.write(plt)
        # _file.open('wb').write(plt)
        # _file.close()        
        # raise ValidationError(plt)
        # raise ValidationError(gb.open('rb').read())

            
    # _fill = base64.b64decode(_fil)
    # _fin = io.BytesIO(_fill)
    # _fdec = io.BytesIO()
    # pyAesCrypt.decryptStream(_fin,_fdec,password,bf,len(_fin.getvalue()))
    # _file=storage._getme(_fdec.getvalue())
    # raise ValidationError(_file.mimetype)

        except Exception:
            return HttpResponseBadRequest(('Invalid request'))

        response = HttpResponse(
            FileWrapper(gb1),
            content_type=_file.mimetype
        )
        # raise ValidationError(plt)

        response['Content-Length'] = gb1.tell()
        if add_attachment_headers:
            response['Content-Disposition'] = \
                'attachment; filename=%(name)s' % {'name': _file.filename}

    return response
# django
from django.db import models
# third party
from django.contrib.auth.models import User
from db_file_storage.model_utils import delete_file, delete_file_if_needed, exists
from db_file_storage.compat import reverse
import hashlib
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
#class

class BookIndex(models.Model):
    book_index_pk = models.AutoField(primary_key=True)
    bytes = models.TextField()
    filename = models.CharField(max_length=255)
    mimetype = models.CharField(max_length=50)

#class BookPages(models.Model):
#    book_pages_pk = models.AutoField(primary_key=True)
#    bytes = models.TextField()
#    filename = models.CharField(max_length=255)
#    mimetype = models.CharField(max_length=50)
##
##
#class BookCover(models.Model):
#    book_cover_pk = models.AutoField(primary_key=True)
#    bytes = models.BinaryField()
#    filename = models.CharField(max_length=255)
#    mimetype = models.CharField(max_length=50)


class Book(models.Model):
    book_pk = models.AutoField(primary_key=True)
    ownr = models.ForeignKey(User,related_name='files',on_delete=models.CASCADE)
#    ownw = models.ForeignKey(max_length=100)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    md5s = models.CharField(max_length=100,null=True)
    index = models.FileField(
        upload_to='usrs.BookIndex/bytes/filename/mimetype',
        blank=False, null=True
    )
    sharedwith = models.ManyToManyField(User)
    key=None
    scm=None
    class Meta:
        unique_together = ("name","ownr","md5s")
#    pages = models.FileField(
#        upload_to='model_filefields_example.BookPages/bytes/filename/mimetype',
#        blank=True, null=True
#    )
#    cover = models.ImageField(
#        upload_to='model_filefields_example.BookCover/bytes/filename/mimetype',
#        blank=True, null=True
#    )

    def get_absolute_url(self):
        return reverse('model_files:book.edit', kwargs={'pk': self.pk})

#     def save(self, *args, **kwargs):
#         # delete_file_if_needed(self, 'index')
# #        delete_file_if_needed(self, 'pages')
#         try:
#             super(Book, self).save(*args, **kwargs)
#         except IntegrityError:
#             if exists(self,'index'):
#                 return reverse('model_files:book.delete', kwargs={'pk': self.pk})
              
#     def save(self, *args, **kwargs):
#         if exists(self,'index'):
#             return reverse('model_files:book.delete', kwargs={'pk': self.pk})
#         # delete_file_if_needed(self, 'index')
# #        delete_file_if_needed(self, 'pages')
#         else:
#             super(Book, self).save(*args, **kwargs)
    def save(self, *args, **kwargs):
        # if exists(self,'index') and self.exists('index'):
            # return reverse('model_files:book.overwrite')

        delete_file_if_needed(self, 'index')
        if not self.pk:  # file is new
            md5 = hashlib.md5()
            for chunk in self.index.chunks():
                md5.update(chunk)
            self.md5s = md5.hexdigest()

#        delete_file_if_needed(self, 'pages')
        # else:
        # try:
        #     super(Book, self).save(*args, **kwargs)
        # except:
        if Book.objects.filter(name=self.name,ownr=self.ownr):
            sd=Book.objects.get(name=self.name,ownr=self.ownr)

                
            if sd.md5s!=self.md5s:
                return False
            else:
                return True
                    # raise ValidationError(self.md5s)
                    # return redirect('model_files:book.edit', kwargs={'pk': sd.pk})
        else:
            super(Book, self).save(*args, **kwargs)
            return True
            

    def it(self,k,s):
        self.key=k
        self.scm=s
    def delete(self, *args, **kwargs):
        super(Book, self).delete(*args, **kwargs)
        delete_file(self, 'index')
#        delete_file(self, 'pages')
    def __str__(self):
        return self.name
    def crtd(self):
        return self.created_at
#
#
#class SoundDeviceInstructionManual(models.Model):
#    bytes = models.TextField()
#    filename = models.CharField(max_length=255)
#    mimetype = models.CharField(max_length=50)
#
#
#class SoundDevice(models.Model):
#    name = models.CharField(max_length=100)
#    instruction_manual = models.FileField(
#        upload_to='model_filefields_example.SoundDeviceInstructionManual'
#                  '/bytes/filename/mimetype',
#        blank=True,
#        null=True
#    )


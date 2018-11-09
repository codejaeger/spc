# django
from django.db import models
# third party
from django.contrib.auth.models import User
from db_file_storage.model_utils import delete_file, delete_file_if_needed, exists
from db_file_storage.compat import reverse
import hashlib
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
    md5s = models.CharField(max_length=100)
    index = models.FileField(
        upload_to='usrs.BookIndex/bytes/filename/mimetype',
        blank=True, null=True
    )
    class Meta:
        unique_together = ("name","ownr")
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
#        delete_file_if_needed(self, 'pages')
        # else:
        super(Book, self).save(*args, **kwargs)

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


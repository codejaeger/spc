# Generated by Django 2.1.2 on 2018-11-21 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usrs', '0014_book_sharedwith'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='md5se',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='md5so',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
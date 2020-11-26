# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class News(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    token = models.CharField(unique=True, max_length=50)
    category = models.CharField(max_length=50)
    title = models.CharField(max_length=250)
    author = models.CharField(max_length=50, blank=True, null=True)
    date = models.CharField(max_length=50)
    image = models.CharField(max_length=500, blank=True, null=True)
    content = models.CharField(max_length=15000)
    dt_created = models.DateTimeField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'news'


class NewsList(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    token = models.CharField(unique=True, max_length=50)
    category = models.CharField(max_length=50)
    title = models.CharField(max_length=250)
    abstract = models.CharField(max_length=1500)
    date = models.CharField(max_length=50)
    image = models.CharField(max_length=500, blank=True, null=True)
    url = models.CharField(max_length=500)
    dt_created = models.DateTimeField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'news_list'

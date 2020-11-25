from django.db import models


class News(models.Model):
    token = models.CharField(unique=True, max_length=50)
    category = models.CharField(max_length=50)
    title = models.CharField(max_length=300)
    author = models.CharField(max_length=200, blank=True, null=True)
    date = models.CharField(max_length=50)
    image = models.CharField(max_length=500, blank=True, null=True)
    content = models.CharField(max_length=15000)
    dt_created = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'news'


class NewsList(models.Model):
    token = models.CharField(unique=True, max_length=50)
    category = models.CharField(max_length=50)
    title = models.CharField(max_length=300)
    abstract = models.CharField(max_length=1000)
    date = models.CharField(max_length=50)
    image = models.CharField(max_length=500, blank=True, null=True)
    url = models.CharField(max_length=500)
    dt_created = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'news_list'

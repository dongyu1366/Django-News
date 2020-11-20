from django.db import models


class News(models.Model):
    source_token = models.CharField(unique=True, max_length=50)
    category = models.CharField(max_length=50)
    title = models.CharField(max_length=300)
    author = models.CharField(max_length=200, blank=True, null=True)
    date_str = models.CharField(max_length=50)
    date = models.DateTimeField()
    image = models.CharField(max_length=500, blank=True, null=True)
    content = models.CharField(max_length=10000)
    dt_created = models.DateTimeField(blank=True, null=True)
    dt_modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'news'


class NewsList(models.Model):
    source_token = models.CharField(unique=True, max_length=50)
    category = models.CharField(max_length=50)
    category_tag = models.CharField(max_length=50)
    title = models.CharField(max_length=300)
    abstract = models.CharField(max_length=500)
    date_str = models.CharField(max_length=50)
    date = models.DateTimeField()
    image = models.CharField(max_length=500)
    url = models.CharField(max_length=500)
    dt_created = models.DateTimeField(blank=True, null=True)
    dt_modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'news_list'


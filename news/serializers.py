from rest_framework import serializers
from news.models import NewsList


class NewsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsList
        fields = ['category', 'token', 'title', 'abstract', 'date', 'image', 'url']

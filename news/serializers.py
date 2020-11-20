from rest_framework import serializers
from news.models import NewsList


class NewsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsList
        fields = ['category', 'source_token', 'title', 'abstract', 'date_str', 'image', 'url']

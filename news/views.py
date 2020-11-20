from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseNotFound
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from news.models import NewsList, News
from news.serializers import NewsListSerializer
from news.tool import CategoryTool


def index(request):
    news_list = NewsList.objects.all().order_by('-date')[0:10]
    context = {'category': 'Latest', 'news': news_list}
    return render(request, "news/index.html", context=context)


def display_news(request, category):
    """
    Display list of news in specific category
    """
    category_dict = CategoryTool.CATEGORY_DICT
    if category in category_dict:
        context = {'category': category_dict[category]}
        return render(request, "news/news.html", context=context)
    else:
        return HttpResponseNotFound('<h1>Page not found</h1>')


def display_news_detail(request, category, token):
    """
    Display the content of the news
    """
    try:
        news = News.objects.get(source_token=token)
        tag = CategoryTool.category_to_tag(category=news.category)
        context = {'news': news, 'tag': tag}
        return render(request, "news/news_detail.html", context=context)
    except ObjectDoesNotExist:
        return HttpResponseNotFound('<h1>Page not found</h1>')


@api_view(['GET', 'POST', ])
def get_news_list(request):
    """
    API endpoint that allows news to be viewed.
    """
    if request.method == 'GET':
        news_list = NewsList.objects.all().order_by('-date')
        serializer = NewsListSerializer(news_list, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = request.data
        news_list = NewsList.objects.filter(**data).order_by('-date')
        serializer = NewsListSerializer(news_list, many=True)
        return Response(serializer.data)

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseNotFound
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from news.models import NewsList, News
from news.serializers import NewsListSerializer
from news.utils import CategoryTool


def index(request):
    news_list = NewsList.objects.all().order_by('-token')[0:10]
    data = list()
    for a in news_list:
        a.tag = CategoryTool.category_to_tag(a.category)
        data.append(a)
    context = {'category': 'Latest', 'news': data}
    return render(request, "news/index.html", context=context)


def display_news(request, category):
    """
    Display list of news in specific category
    """
    category_dict = CategoryTool.CATEGORY_DICT
    if category in category_dict:
        category = category_dict[category]
        news_list = NewsList.objects.filter(category=category).order_by('-token')[0:10]
        data = list()
        for a in news_list:
            a.tag = CategoryTool.category_to_tag(a.category)
            data.append(a)
        context = {'category': category, 'news': data}
        return render(request, "news/news.html", context=context)
    else:
        return HttpResponseNotFound('<h1>Page not found</h1>')


def display_news_detail(request, category, token):
    """
    Display the content of the news
    """
    try:
        news = News.objects.get(token=token)
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
        news_list = NewsList.objects.all().order_by('-token')
        serializer = NewsListSerializer(news_list, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        category = request.data['category']
        page = request.data['page']
        news_list = NewsList.objects.filter(category=category).order_by('-token')
        news_list = news_list[0:(10*page)]
        serializer = NewsListSerializer(news_list, many=True)
        return Response(serializer.data)

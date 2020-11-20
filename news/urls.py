from django.urls import path
from news import views


urlpatterns = [
    path('news/', views.index, name='index'),
    path('news/<str:category>/', views.display_news, name='category'),
    path('news/<str:category>/<str:token>', views.display_news_detail, name='news'),
    path('api/news-list/', views.get_news_list),
]
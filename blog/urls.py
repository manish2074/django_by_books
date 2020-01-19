from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('',views.post_list, name='post_list'),
    path('<int:pk>/<str:slug>/',views.post_detail,name='post_detail'),
    path('<int:pk>/<str:slug>/share/',views.post_share,name='post_share'),
    path('tag/<str:tag_slug>/',views.post_list,name='post_list_by_tag')
]   
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path(r'old/', views.post_list_old, name='post_list_old'),
    #path(r'fav/', views.fav, name='fav'),
    path(r'favorite/', views.favorite, name='favorite'),
    path(r'want/', views.want, name='want'),
    path(r'read/', views.read, name='read'),
    path(r'famous/', views.famous, name='famous'),
    path(r'cash_clear/', views.cash_clear, name='cash_clear'),
    
]

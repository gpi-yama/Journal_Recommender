from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path(r'old/', views.post_list_old, name='post_list_old'),
    #    path('/created_date/', views.post_list_created_date, name="post_list"),
    #    path(r'sample/', views.BoardListView.as_view(), name='home'),
    #    path('post/<int:pk>', views.post_detail, name="post_detail"),
    #    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    #    path(r'^post/(?P<pk>?[0-9]+)/edit/$', views.post_edit, name='post_edit'),
]

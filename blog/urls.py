from django.urls import path
from . import views

urlpatterns = [
  
  # path('', views.create_comment, name='index'),
  path('', views.index, name='index'),
  path('fullpost/<int:id>', views.fullpost, name='fullpost'),
  path('create_post',views.create_post,name='create_post'),
  path('update_post/<int:id>',views.update_post,name='update_post'),
  path('dashboard',views.dashboard,name='dashboard'),
  path('delete_post/<int:pk>',views.delete_post,name='delete_post'),
  path('like_post/<int:id>',views.like_post,name='like_post'),
]
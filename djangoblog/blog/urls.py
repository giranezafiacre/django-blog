from django.urls import path
from . import views

urlpatterns = [
  path('', views.index, name='index'),
  path('create_post',views.create_post,name='create_post'),
  path('update_post/<int:id>',views.update_post,name='update_post')
]
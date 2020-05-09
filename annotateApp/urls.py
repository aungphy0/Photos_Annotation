from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('saveimage/', views.saveimage, name='saveimage'),
    path('location/', views.location, name='location'),
    path('time/', views.time, name='time'),
    path('annotate/', views.annotate, name='annotate'),
]

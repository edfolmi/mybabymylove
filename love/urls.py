from django.urls import path

from . import views

urlpatterns = [
    path('', views.page, name='page'),
    path('page1/', views.page1, name='page1'),
    path('page2/', views.page2, name='page2'),
    path('page3/', views.page3, name='page3'),
    path('page4/', views.page4, name='page4'),
    path('favourite/', views.intro, name='intro'),
    path('send-gift/', views.send_gift, name='send_gift'),
]

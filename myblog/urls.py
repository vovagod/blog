from django.urls import path
from myblog import views

urlpatterns = [
    path('register/', views.UserCreation.as_view()),
    path('login/', views.UserLogin.as_view()),
    path('postcreate/', views.PostCreation.as_view()),
    path('abcsorting/', views.AllAbcSorting.as_view()),
    path('numsorting/', views.AllNumSorting.as_view()),
    path('datesorting/', views.BloggerPostSorting.as_view()),
    path('subscribe/<int:pk>/', views.Subscribe.as_view()),
    path('unsubscribe/<int:pk>/', views.UnSubscribe.as_view()),
    path('sublist/', views.SubList.as_view()),
    path('readpostmark/<int:pk>/', views.ReadPostMark.as_view()),
    path('unreadpostoutput/', views.UnReadPostOutput.as_view()),
]

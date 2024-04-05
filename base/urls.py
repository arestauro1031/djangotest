from django.urls import path    
from . import views

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),
    
    path('', views.home, name='home'),
    path('room/<str:pk>/', views.room, name='room'),  #pk is a variable that will be passed to the view
    path('profile/<str:pk>/', views.userProfile, name='user-profile'),
    
    path('create-room/', views.createRoom, name="create-room"), #   name="create-room" is used in the html template
    path('update-room/<str:pk>/', views.updateRoom, name="update-room"), #  name="update-room" is used in the html template
    path('delete-room/<str:pk>/', views.deleteRoom, name="delete-room"), # name="delete-room" is used in the html template
    path('delete-messsage/<str:pk>/', views.deleteMessage, name="delete-message"),
    
    
    path('update-user/', views.updateUser, name="update-user"),
    path('topics/', views.topicsPage, name="topics"),
]

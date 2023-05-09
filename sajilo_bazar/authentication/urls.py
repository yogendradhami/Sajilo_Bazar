from django.urls import path
from authentication import views
urlpatterns = [
    path('register/', views.Register,name='register'),
    path('login/', views.Login,name='login'),
    path('logout/', views.Logout,name='logout'),
    path('login/', views.Login,name='login'),
    
]

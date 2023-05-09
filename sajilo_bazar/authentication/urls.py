from django.urls import path
from authentication import views
urlpatterns = [
    path('register/', views.Register,name='register'),
    path('login/', views.Login,name='login'),
    
]

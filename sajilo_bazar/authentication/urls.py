from django.urls import path
from authentication import views
urlpatterns = [
    path('register/', views.Register,name='regieter'),
    path('login/', views.Login,name='login'),
    
]

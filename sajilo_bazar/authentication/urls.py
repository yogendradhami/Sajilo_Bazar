from django.urls import path
from authentication import views
urlpatterns = [
    path('register/', views.Register,name='register'),
    path('login/', views.Login,name='login'),
    path('logout/', views.Logout,name='logout'),
    path('activate/<uidb64>/<token>', views.ActivateAccountView.as_view(),name='activate'),
    path('request-rest-email/', views.RequestResetEmailView.as_view(),name='request-reset-email'),
    path('set-new-password/<uidb64>/<token>', views.SetNewPasswordView.as_view(),name='set-new-password'),
    
]

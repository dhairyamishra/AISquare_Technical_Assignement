from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from django.contrib.auth import views as auth_views
from .views import home, register

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('summarizer.urls')),
    path('api/token-auth/', obtain_auth_token),
    path("quiz/", include("quizui.urls")),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/register/', register, name='register'),
    path('', home, name='home'),
]

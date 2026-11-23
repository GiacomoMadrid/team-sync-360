"""
URL configuration for teamsync project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.views import TokenVerifyView

from login import views as views_login


router = routers.DefaultRouter()

#Login
router.register(r'usuarios', views_login.UsuarioViewSet, basename='usuario')
router.register(r'groups', views_login.GroupViewSet, basename='grupo')

urlpatterns = [
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
    path('login-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # JWT Auth
    #path('api/register/', views_login.RegisterView.as_view(), name='register'),
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'), 

    # Activación de cuenta por URL
    path('api/activar/<str:uid>/<str:token>/', views_login.ActivateAccountView.as_view(), name='activate'),
    #path('api/activar/', views_login.ActivateAccountView.as_view(),name='activate'),
    path('api/logout/', views_login.LogoutView.as_view(), name='logout'),
    
    # Roles y Grupos
    path('api/usuarios/<int:user_id>/roles/', views_login.UserRolesView.as_view(), name='user-roles'),
    path('api/usuarios/<int:user_id>/roles/<int:role_id>/', views_login.UserRolesView.as_view(), name='user-role-detail'),
    
    # Consultar roles y permisos del usuario autenticado
    path('api/usuarios/me/roles/', views_login.MisRolesView.as_view(), name='my-roles'),
    path('api/usuarios/me/permisos/', views_login.MisPermissionsView.as_view(), name='my-permissions'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)    
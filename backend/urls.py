"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
"""

from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import routers
from rest_framework.schemas import get_schema_view
from rest_framework_swagger.renderers import SwaggerUIRenderer, OpenAPIRenderer

from .api.views import index_view, MessageViewSet
from .api.views import *
from django.views.generic import TemplateView

from .api import views

router = routers.DefaultRouter()
router.register('messages', MessageViewSet)
router.register('userprofiles', UserProfileViewSet)
router.register('users', UserViewSet)

schema_view = get_schema_view(title='API DOC', renderer_classes=[SwaggerUIRenderer, OpenAPIRenderer])  # add

urlpatterns = [
    path('', TemplateView.as_view(template_name='api/login.html')), # <--
    path('api/index', TemplateView.as_view(template_name='api/login.html')), # <--
    path('api/userlist/', views.UserList.as_view(), name='user_list'),

    # http://localhost:8000/
    #path('', index_view, name='index'),

    # http://localhost:8000/api/<router-viewsets>
    path('api/', include(router.urls)),

    # http://localhost:8000/api/admin/
    path('api/admin/', admin.site.urls),

    path('accounts/', include('allauth.urls')), # <--

    path('accounts/profile/', views.profile, name='profile'),

    path('accounts/profile/update/', views.profile_update, name='profile_update'),


    path('api/docs/', schema_view, name='docs'),  # add
]

#846932522788-f66q7fi5oqd8t869d0130cvtigi1f8nn.apps.googleusercontent.com
#6N5vn9DxbdpQfmuh64bXdlzL


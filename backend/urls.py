"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from .api.views import index_view, MessageViewSet
from django.views.generic import TemplateView

router = routers.DefaultRouter()
router.register('messages', MessageViewSet)

urlpatterns = [
    path('', TemplateView.as_view(template_name='api/login.html')), # <--

    # http://localhost:8000/
    #path('', index_view, name='index'),

    # http://localhost:8000/api/<router-viewsets>
    path('api/', include(router.urls)),

    # http://localhost:8000/api/admin/
    path('api/admin/', admin.site.urls),

    path('accounts/', include('allauth.urls')), # <--

]

#846932522788-f66q7fi5oqd8t869d0130cvtigi1f8nn.apps.googleusercontent.com
#6N5vn9DxbdpQfmuh64bXdlzL


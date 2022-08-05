"""viya URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from django.contrib import admin
from django.urls import path, include
from viya1.views import *
from viya1.api import *
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',indexview),
    path('contact/', ContactListCreateAPIView.as_view()),
    path('divisions/',  DivisionListAPIView.as_view()),
    path('districts/',  DistrictListAPIView.as_view()),
    path('subdistricts/', SubDistrictListAPIView.as_view()),
    path('admindrop/', include('admindrop.urls')),
    path('viya1/', include('viya1.urls')),
    path('contact/<int:id>/',ContactRetrieveUpdateDestroyAPIView.as_view()),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# add title, header title, and site tittle
admin.site.index_title = 'Viya Legal kjgjhgkh'
admin.site.site_header = 'Viya Legal Admin'
admin.site.site_title = 'Site Title Viya Legal'

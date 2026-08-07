from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

from django.views.generic.base import TemplateView

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions


from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('App.urls')),
    path('Add/', include('AddAppViewSets.urls')),
    path('Account/', include('accounts.urls')),
    path('SMS/', include('MyTemplatesApp.urls')),



]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)


admin.site.site_header= "SHULE FASTA DASHBOARD"
admin.site.site_title = "DASHBOARD AREA"
admin.site.index_title = "WELCOME TO ADMIN DASHBOARD"
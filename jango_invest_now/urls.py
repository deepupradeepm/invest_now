"""jango_invest_now URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.views.generic import TemplateView

from app1 import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',TemplateView.as_view(template_name='base.html')),
    path('ad/',views.log_in,name='admin1'),
    path('addc/',views.add_company,name='addc'),
    path('listco/',views.list_compay,name='listco'),
    path('update/<int:id>/',views.udpate_comay,name='update_co'),
    path('delete/<int:id>/',views.delete_comay,name='delete_co'),
    #path('user/',TemplateView.as_view(),name='user'),
    path('logout/',views.log_out,name='logout_admin'),
    path('user/',views.log_in_user,name='user'),
    path('reg/',views.register,name='regi'),
    path('create/',views.create_investmet,name='create'),
    path('list/',views.list_investmet,name='list'),
    path('update_invested/<int:id>/',views.udpate_investe,name='update_user'),
    path('delete_invested/<int:id>/',views.delete_investe,name="delete_user"),
    path('logout_user/',views.log_out_user,name='logout_user')
]

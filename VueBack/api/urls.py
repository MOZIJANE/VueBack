"""VueBack URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path
from . import views

app_name = "api"

urlpatterns = [
    path('getHistoryFromPRTG/', views.getHistoryFromPRTG),
    path('getMTLvpnUser/', views.getMTLvpnUser),
    path('getHistory_speed_FromPRTG/', views.getHistory_speed_FromPRTG),
    path('getSankeyFromUrl/', views.getSankeyFromUrl),
    path('Cisco_data/', views.Cisco_data),
    path('Info_Refer/', views.Info_Refer),
    path('regular_check/', views.regular_check),
    path('getSankeyFromUrl_GZ_HK/', views.getSankeyFromUrl_GZ_HK),
    path('getSankeyFromUrl_HK_GZ/', views.getSankeyFromUrl_HK_GZ),

]

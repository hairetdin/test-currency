"""testcurrency URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from currency import views as currency_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', currency_views.IndexView.as_view(), name='index'),
    url(r'^currencies/$', currency_views.CurrencyListView.as_view(), name='currencies'),
    url(r'^currency/(?P<pk>\d+)$', currency_views.CurrencyDetailView.as_view(), name='currency-detail'),
    url(r'^ajax-example/$', currency_views.AjaxExample.as_view(), name='ajax-example'),
    url(r'^converter/$', currency_views.Converter.as_view(), name='converter'),
]

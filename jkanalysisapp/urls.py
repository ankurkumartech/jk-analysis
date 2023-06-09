from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('get_data/', views.get_data),
    
    # path('yoy/<str:start_year>/<str:end_year>/', views.yoy),
    
    # path('qoq/<str:start_year>/<str:end_year>/<str:quarter>', views.qoq),
    # path('mom/<str:start_year>/<str:end_year>/<str:first_month>/<str:second_month>', views.mom),
    
    # path('percent_filter/<str:percent_filter>/<str:start_year>/<str:end_year>/<str:first_month>/<str:second_month>', views.percent_filter),
    
    # path('percent_filter/<str:percent_filter>/<str:start_year>/<str:end_year>/<str:quarter>/<str:end_quarter>', views.percent_filter),
    
    # path('percent_filter/<str:percent_filter>/<str:start_year>/<str:end_year>', views.percent_filter),
    
    # path('download_data/<str:percent_filter>/<str:start_year>/<str:end_year>', views.download_excel),
    
    path('download_data/<str:percent_filter>/<str:type>/<str:start_year>/<str:end_year>/<str:first_month>/<str:second_month>', views.download_excel),
    
    path('get_regions/', views.get_regions),
    path('get_zones', views.get_zones),
    path('yoy_new', views.yoy_new),
    path('qoq_new', views.qoq_new),
    path('mom_new', views.mom_new),
    
    
    
]

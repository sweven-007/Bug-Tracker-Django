from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('login/', views.login),
    path('home_admin/', views.home_admin),
    path('home_developer/', views.home_developer),
    path('home_user/', views.home_user),
    path('logout/', views.logout),
    path('report_bug/', views.report_bug),
    path('delete_report/<int:id_>/', views.delete_report),
    path('reopen_report/<int:id_>/', views.reopen_report),
    path('assign_report/', views.assign_report),
    path('reject_report/<int:id_>/', views.reject_report),    
    path('resolve_report/<int:id_>/', views.resolve_report),
]
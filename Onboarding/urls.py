"""Onboarding URL Configuration

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
from Onb_app import views
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='login/')),
    path('admin/', admin.site.urls),
    path('test/', views.test),
    path('welcome/', views.welcome),
    path('login/', views.auth_login),
    path('authenticate/', views.logincheck),
    path('home/', views.home),
    path('register/', views.register),
    path('logout/', views.auth_logout),
    path('error/', views.error),
    path('profile/', views.profile_page),
    path('profile/update_profile/', views.updateprofile),
    path('manage_users/', views.viewsupportengineers),
    path('manage_users/onb_assign/', views.onb_assign),
    path('manage_users/del_onb/', views.del_onb),
    path('weeks/', views.weeks),
    path('weeks/add_week/', views.add_week),
    path('weeks/del_week/', views.del_week),
    path('weeks/<int:id>', views.week_content, name='content'),
    path('weeks/add_content/', views.add_content),
    path('weeks/del_content/', views.del_content),
    path('targets/', views.show_targets),
    path('targets/add_target/', views.add_target),
    path('targets/del_target/', views.del_target),

]
'''path('weeks/week_check/', views.week_check),'''

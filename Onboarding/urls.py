from django.contrib import admin
from django.urls import path
from Onb_app import views
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views


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
    path('audit/', views.audit),
    path('profile/update_profile/', views.updateprofile),
    path('profile/change_password/', views.change_password),
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
    path('targets/target_check/', views.target_check),
    path('weeks/content_check/', views.content_check),
    path('home/view_details/', views.view_details),
    path('home/check_form/', views.check_form),
    path('home/check_weeks/', views.check_weeks),
    path('home/check_targets/', views.check_targets),
    path('home/check_content/', views.check_content),
    path('access_req/', views.access_req),
    path('access_req/access_tab/', views.access_tab),
    path('access_req/del_tab/', views.del_tab),
    path('access_req/get_items/', views.get_items),
    path('access_req/add_item/', views.add_item),
    path('access_req/del_item/', views.del_item),
    path('access_req/access_req_update/', views.access_req_update),
    path('home/add_resource/', views.add_resource),
    path('home/del_resource/', views.del_resource),
    path('home/nh_onboarded/', views.nh_onboarded),
    path('home/nh_not_onboarded/', views.nh_not_onboarded),
    path('reset_password/', views.reset_password),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='reset_password_sent.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='reset_password_input.html'), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='reset_password_done.html'), name='password_reset_complete'),
]
'''
path('reset_password/', auth_views.PasswordResetView.as_view(template_name='reset_password.html'), name='password_reset'),

path('otp/', views.generate_otp),
path('send_otp/', views.send_otp),
path('reset_password/', views.reset_password),
'''

from django import views
from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.Dashboard, name='dashboard'),
    path('leaves/', views.Leaves, name='leaves'),
    path('apply-leave/', views.applyleave, name='applyleave'),
    path('admin-dashboard/',views.admin,name='admin'),
    path('approve-leave/<int:id>/', views.approve_leave, name='approve_leave'),
    path('reject-leave/<int:id>/', views.reject_leave, name='reject_leave'),
    # Admin Register
    path('adminregister/',views.adminregister,name='adminregister'),
    # Admin Login
    path('adminlogin/',views.adminlogin,name='adminlogin'),
    # Admin Panel
    path('admin/',views.admin,name='admin'),
    path('swipe-data/', views.swipedata, name='swipedata'),
    path('checkin/', views.checkin, name='checkin'), #chenck in
    path('checkout/', views.checkout, name='checkout'), #check out
    path('timesheet/', views.timesheet, name='timesheet'),
    path('addentry/', views.addentry, name='addentry'),
    path("verify-timesheet/<int:id>/",views.verify_timesheet,name="verify_timesheet"),
    path("notverify-timesheet/<int:id>/",views.notverify_timesheet,name="notverify_timesheet"),
    path('employee/', views.employee, name='employee'),
    path("profile/", views.profile, name="profile"),
    path("assets/", views.assets, name="assets"),
    path("assetdetails/<int:id>/",views.assetdetails,name="assetdetails"),
    path("employee_profiles/",views.employee_profiles,name="employee_profiles"),
    path("paydetails/<int:employee_id>/",views.paydetails,name="paydetails"),
    path("payslip/", views.payslip, name="payslip"),
    path("delete_employee/<int:id>/",views.delete_employee,name="delete_employee"),
]
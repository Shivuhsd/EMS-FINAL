from django.urls import path
from . import views
from django.contrib.auth import views as auth_veiws

urlpatterns = [
    path('', views.LoginPage, name='loginpage'),

    path('dashboard/', views.dashboard, name='dashboard'),

    path('studentupload/', views.StudentUpload, name='studentupload'),

    path('showupload/<str:pk>/', views.ShowUpload, name='showupload'),

    path('validate/', views.Validate, name='validate'),

    path('emailveri/<str:pk>/', views.EmailVeri, name='emailveri'),

    path('otpverify/<str:pk>/<str:e_mail>/', views.OtpVerify, name='otpverify'),

    path('password/<str:pk>/<str:e_mail>/', views.Password, name='password'),

    #Dash Examination Path/URL
    path('Dash_Examination/', views.Dash_Examination, name='dash_examination'),

    #Dash HallTicket Generation Path/URL
    path('AdminHallTicket/<str:dp>/<str:cor>/', views.AdminHallticket, name='admin_HallTicket'),

    #Dash Student HallTicket View
    path('HallTicket/', views.Dash_Admin_HallTicketGeneration, name='dash_admin_HallTicketGeneration'),


    path('addsubjects/<str:dp>/<str:cr>/', views.Add_Subject, name='addsubject'),
    

    path('addstaff/', views.Dash_Admin_Add_Staff, name='addstaff'),


    path('addroom/', views.Add_Room, name='addroom'),


    path('profile/', views.Profile, name='profile'),


    path('selectdept/', views.SelectDept, name='selectdept'),

    #To Select Course after Selecting Department
    path('selectcor/<str:dp>/', views.SelectCourse, name='selectcor'),


    path('adddept/', views.addDept, name='adddept'),


    path('addcourse/', views.addCourse, name='addcourse'),


    path('seldept/', views.seldept, name='seldept'),


    path('selcor/<str:dp>/', views.selcor, name='selcor'),



    #Routes to Allotment of Students

    path('allotment/', views.Allotment, name='allotment'),


    path('datedetail/<str:pk>/', views.DateAllot, name='dateallot'),


    path('allotedpdf/', views.AllotPDF, name='allotpdf'),


    path('staffregister/', views.StaffRegister, name='staffregister'),


    path('admitpdf/', views.AdmitPDF, name='admitpdf'),


    path('studenteli/', views.Studenteli, name='studenteli'),


    path('studentelidetail/<str:pk>/', views.StudentEliDetail, name='studentelidetail'),


    path('report/', views.Reports, name='report'),


    path('notifications/', views.Notification, name='notifications'),


    path('readreport/', views.ReadReport, name='readreport'),


    path('usrlogout/', views.usrlogout, name='usrlogout'),


]
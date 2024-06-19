from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.mylogin,name='login'),

    path('chief_dashboard/', views.chief_dashboard, name='chief_dashboard'),
    path('teacher_dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('staff_dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('logout/',auth_views.LogoutView.as_view(),name='logout'),


    path('exam_view/',views.exam,name='exam_view'),
    path('get-courses/', views.get_courses, name='get_courses'),

    path('edit_teacher',views.edit_teacher,name='edit_teacher'),

    
    path('announce_exam/', views.announce_exam, name='announceExam'),
    path('view_alloted_duty/',views.view_alloted_duty,name='view_alloted_duty'),
    path('view_summary/',views.view_summary,name='view_summary'),
    path('upload_preferences/', views.upload_preferences, name='upload_preferences'),

    path('allot_duty/', views.allot_duty, name='allot_duty'),
]


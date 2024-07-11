from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.mylogin,name='login'),

    path('chief_dashboard/', views.chief_dashboard, name='chief_dashboard'),
    path('teacher_dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('staff_dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('logout/',views.logout_view,name='logout'),


    path('edit_teacher',views.edit_teacher,name='edit_teacher'),

    
    path('announce_exam/', views.announce_exam, name='announceExam'),
    path('view_alloted_duty/',views.view_alloted_duty,name='view_alloted_duty'),
    path('view_summary/',views.view_summary,name='view_summary'),
    path('upload_preferences/', views.upload_preferences, name='upload_preferences'),

    path('allot_duty/', views.allot_duty, name='allot_duty'),

    # path('add_teacher/', views.add_teacher, name='add_teacher'),

    path('edit_teacher/', views.add_teacher, name='edit_teacher'),

    path('add_teacher/', views.add_teacher, name='add_teacher'),
    path('delete_teacher/<int:teacher_id>/', views.delete_teacher, name='delete_teacher'),
    #path('teacher_management/', views.add_teacher, name='teacher_management'),  # Reuse the add_teacher view for initial load

    path('print_label/', views.print_label, name='print_label'),
    path('no_preference_duty/', views.no_preference_duty, name='no_preference_duty'),
    path('total_summary/', views.total_summary, name='total_summary'),

    #path('get_courses/', views.get_courses, name='get_courses'),
    path('exam/', views.exam, name='exam'),
    path('exam_success/', views.exam_success, name='exam_success'),

]


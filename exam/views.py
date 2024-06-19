from django.http import HttpResponse, JsonResponse
from .models import *
from datetime import datetime
from django.views.generic.edit import CreateView
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login 
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import Group,User
from .models import Timetable  # Import your model
from .forms import ExamAnnounce
from .models import Course, Department, ExamTimeTable
from .models import Exam
from .models import ExamTimeTable, preferTable
from django.contrib.auth.decorators import login_required
from .forms import PreferTableForm
from django.shortcuts import render, redirect
from django.db.models import Count
from .models import  dutyAllotment, teacherTable, ExamTimeTable, room
# from .forms import dutyAllotmentForm



@csrf_exempt
def mylogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Check user's groups
            groups = user.groups.all()

            if groups.exists():
                group_names = [group.name for group in groups]

                # Debugging: print group names
                print(f"User {username} belongs to groups: {group_names}")

                # Redirect based on group membership
                if 'Chief' in group_names:
                    return redirect('chief_dashboard')
                elif 'Teacher' in group_names:
                    return redirect('teacher_dashboard')
                elif 'Office' in group_names:
                    return redirect('staff_dashboard')
                elif 'Admin' in group_names:
                    return redirect('/admin/')
                else:
                    messages.error(request, 'You do not belong to any group.')
            else:
                messages.error(request, 'You do not belong to any group.')
        else:
            messages.error(request, 'Invalid username or password.')
            print("Invalid login credentials")  # Debugging line

    return render(request, 'exam/login.html')


def chief_dashboard(request):
    return render(request, 'exam/chief.html')

def teacher_dashboard(request):
    return render(request, 'exam/teacher.html')

def staff_dashboard(request):
    return render(request, 'exam/office.html')

# def exam_view(request):
#      # Fetching course_code and course_title from Course model
#      courses = Course.objects.values_list('course_code', 'course_title')
    
#      # Fetching dept_name from Department model
#      departments = Department.objects.values_list('dept_name', flat=True)
    
#      context = {
#          'courses': courses,
#          'departments': departments,
#      }

#      print("context", context)
#      return render(request, 'exam/exam.html', context)

def get_courses(request):
    if request.method == 'GET':
        #departmentname = request.GET.get('department')
        sem = request.GET.get("semester")
        #department = Department.objects.get(dept_name=departmentname)
        courses = Course.objects.filter(semester=sem).values('course_id', 'course_title')
       # print("get_courses", department, departmentname, f"{courses=}", sem)
        courses_list = list(courses)
        return JsonResponse(courses_list, safe=False)

@csrf_exempt
def exam(request):
    if request.method == "POST":
            
        # If the form is submitted
        #form = ExamTimeTable(request.POST)  # Assuming you have a form for validation
        print(request.POST.get("exam"))
        semester = request.POST.get("sem")
        exam = Course.objects.get(course_title=request.POST.get("exam"))
        date = request.POST.get("date")
        time_from = request.POST.get("time_from")
        time_to = request.POST.get("time_to")
        department = Department.objects.get(dept_name=exam.dept)

        print("request body prints here!!!!!", semester, exam,date,time_from,time_to, exam, department)
        exam_time_table = ExamTimeTable(course_id=exam,dept=department,date=date,time_from=time_from,time_to=time_to, semester=semester)
        exam_time_table.save()
        # if form.is_valid():
        #     # If form data is valid, save it to the database
        #     form.save()
        #     return redirect('exam_view')  # Redirect to a success page or any other URL
        # else
        #     # If form data is invalid, render the form again with errors
        return render(request, "exam/exam.html")
    else:
        # If it's a GET request, just render the form]
        courses = Course.objects.values_list('course_code', 'course_title')
        departments = Department.objects.values_list('dept_name', flat=True)
            
        context = {
        'departments': departments,
        'courses': courses,
        }

        #form = ExamTimeTable()  # Assuming you have a form for validation
        return render(request, "exam/exam.html", context)





def edit_teacher(request):
    return render(request,'exam/edit_teacher.html')



def exam_table(request):
    timetable_entries = ExamTimeTable.objects.all()

    if request.method == "POST":
        # If the form is submitted
        form = preferTable(request.POST)  # Assuming you have a form for validation
        if form.is_valid():
            # If form data is valid, save it to the database
            form.save()
            return redirect('uploading_preference')  # Redirect to a success page or any other URL
        else:
            # If form data is invalid, render the form again with errors
            context = {
                'form': form,
                'timetable_entries': timetable_entries
            }
            return render(request, "exam/uploading_preference.html", context)
    else:
        # If it's a GET request, just render the form
        form = preferTable()  # Assuming you have a form for validation
        context = {
            'form': form,
            'timetable_entries': timetable_entries
        }
        return render(request, 'exam/uploading_preference.html', context)

@csrf_exempt
def announce_exam(request):
    if request.method == 'POST':
        form = ExamAnnounce(request.POST)
        if form.is_valid():
            form.save()
            return redirect('announceExam')  # Redirect to a success page or any other page
    else:
        form = ExamAnnounce()
    return render(request, 'exam/announceExam.html', {'form': form})

def teacher_dashboard(request):
    latest_exams = Exam.objects.order_by('-date')[:4]
    return render(request, 'exam/teacher.html', {'latest_exams': latest_exams})


def view_alloted_duty(request):
    return render(request, 'exam/view_alloted_duty.html')

def view_summary(request):
    return render(request, 'exam/view_summary.html')


@login_required
def upload_preferences(request):
    if request.method == 'POST':
        # Process form submission
        teacher_id = request.user.id  # Get the logged-in teacher's user ID
        selected_exams = request.POST.getlist('selected_exams')

        for exam_id in selected_exams:
            exam = ExamTimeTable.objects.get(id=exam_id)
            prefer_entry = preferTable(teacher_id_id=teacher_id, course_id_id=exam.id, date=exam.date)
            prefer_entry.save()

        return redirect('teacher_dashboard')  # Redirect to teacher dashboard or appropriate URL
    else:
        # Render the page with latest uploaded exams
        timetable_entries = ExamTimeTable.objects.all()  # Retrieve all entries or filter as needed
        return render(request, 'exam/uploading_preference.html', {'timetable_entries': timetable_entries})
    


def allot_duty(request):
    if request.method == 'POST':
        teacher_id = request.POST.get('teacher_id')
        course_id = request.POST.get('course_id')
        date = request.POST.get('date')
        room_id = request.POST.get('room_id')

        teacher = teacherTable.objects.get(id=teacher_id)
        course = ExamTimeTable.objects.get(id=course_id)
        

        duty = dutyAllotment(
            teacher_id=teacher,
            course_id=course,
            date=date,
            
        )
        duty.save()

        return redirect('chief_dashboard')

    preferences = preferTable.objects.select_related('teacher_id', 'course_id').all()
    
    # Group preferences by exam date
    exam_dates = {}
    for preference in preferences:
        exam_date = preference.course_id.date
        if exam_date not in exam_dates:
            exam_dates[exam_date] = []
        exam_dates[exam_date].append(preference)
    
    context = {
        'exam_dates': exam_dates,
    }
    return render(request, 'exam/allot_duty.html', context)
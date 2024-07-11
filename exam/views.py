from django.http import HttpResponse, JsonResponse
from .models import *
from datetime import datetime
from django.views.generic.edit import CreateView
from django.urls import reverse
from django.shortcuts import get_object_or_404, render, redirect
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
from .forms import DutyAllotmentForm
from django.contrib import messages
from .models import ExamTimeTable, preferTable, room, dutyAllotment
from .forms import DutyAllotmentForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse
from django.views.decorators.http import require_POST

from django.shortcuts import render
from django.http import HttpResponse
from .models import Exam, ExamTimeTable
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
from reportlab.lib import colors
from django.contrib.auth import logout


@csrf_exempt
def logout_view(request):
    logout(request)
    # Redirect to a specific URL after logout (optional)
    return redirect('http://127.0.0.1:8000/')  # Replace 'home' with your desired URL name

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

# @csrf_exempt
# def exam(request):
#     if request.method == "POST":
            
#         # If the form is submitted
#         #form = ExamTimeTable(request.POST)  # Assuming you have a form for validation
#         print(request.POST.get("exam"))
#         semester = request.POST.get("sem")
#         exam = Course.objects.get(course_title=request.POST.get("exam"))
#         date = request.POST.get("date")
#         time_from = request.POST.get("time_from")
#         time_to = request.POST.get("time_to")
#         department = Department.objects.get(dept_name=exam.dept)

#         print("request body prints here!!!!!", semester, exam,date,time_from,time_to, exam, department)
#         exam_time_table = ExamTimeTable(course_id=exam,dept=department,date=date,time_from=time_from,time_to=time_to, semester=semester)
#         exam_time_table.save()
#         # if form.is_valid():
#         #     # If form data is valid, save it to the database
#         #     form.save()
#         #     return redirect('exam_view')  # Redirect to a success page or any other URL
#         # else
#         #     # If form data is invalid, render the form again with errors
#         return render(request, "exam/exam.html")
#     else:
#         # If it's a GET request, just render the form]
#         courses = Course.objects.values_list('course_code', 'course_title')
#         departments = Department.objects.values_list('dept_name', flat=True)
            
#         context = {
#         'departments': departments,
#         'courses': courses,
#         }

#         #form = ExamTimeTable()  # Assuming you have a form for validation
#         return render(request, "exam/exam.html", context)

# @csrf_exempt
# def exam_view(request):
#     if request.method == "POST":
#         semester = request.POST.get("sem")
#         course_title = request.POST.get("exam")
#         date = request.POST.get("date")
#         time_from = request.POST.get("time_from")
#         time_to = request.POST.get("time_to")
        
#         courses = Course.objects.filter(course_title=course_title)
#         if not courses.exists():
#             # Handle the case where no courses are found
#             return render(request, "exam/exam.html", {'error': 'No courses found with the given title.'})

#         for course in courses:
#             department = Department.objects.get(dept_name=course.dept)
#             exam_time_table = ExamTimeTable(
#                 course_id=course,
#                 dept=department,
#                 date=date,
#                 time_from=time_from,
#                 time_to=time_to,
#                 semester=semester
#             )
#             exam_time_table.save()

#         return redirect('exam_view')
#     else:
#         courses = Course.objects.values_list('course_code', 'course_title')
#         departments = Department.objects.values_list('dept_name', flat=True)
#         context = {
#             'departments': departments,
#             'courses': courses,
#         }
#         return render(request, "exam/exam.html", context)




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
    


# def allot_duty(request):
#     exam_dates = {}
#     for preference in preferTable.objects.select_related('teacher_id', 'course_id').all():
#         if preference.date not in exam_dates:
#             exam_dates[preference.date] = []
#         exam_dates[preference.date].append(preference)

#     if request.method == 'POST':
#         form = DutyAllotmentForm(request.POST)
#         if form.is_valid():
#             print("Form is valid")
#             print("Cleaned data:", form.cleaned_data)

#             user = form.cleaned_data['user']
#             course_id = form.cleaned_data['course_id']
#             date = form.cleaned_data['date']
#             room_id = form.cleaned_data['room_id']

#             duty_allotment, created = dutyAllotment.objects.get_or_create(
#                 user=user,
#                 course_id=course_id,
#                 date=date,
#                 room_id=room_id
#             )

#             if created:
#                 messages.success(request, 'Duty has been successfully allocated.')
#             else:
#                 messages.warning(request, 'Duty for this user and date already exists.')

#             return redirect(reverse('allot_duty'))
#         else:
#             print("Form is not valid")
#             print("Errors:", form.errors)

#     else:
#         form = DutyAllotmentForm()

#     context = {
#         'exam_dates': exam_dates,
#         'form': form,
#         'rooms': room.objects.all(),
#     }
#     return render(request, 'exam/allot_duty.html', context)

@login_required
def view_alloted_duty(request):
    my_duties = dutyAllotment.objects.filter(user=request.user)
    context = {
        'my_duties': my_duties
    }
    return render(request, 'exam/view_alloted_duty.html', context)


def view_summary(request):
    my_duties = dutyAllotment.objects.filter(user=request.user)
    total_duties = my_duties.count()  # Total number of duties taken by the user

    context = {
        'my_duties': my_duties,
        'total_duties': total_duties
    }
    return render(request, 'exam/view_summary.html', context)


def allot_duty(request):
    exam_dates = {}
    for preference in preferTable.objects.select_related('teacher_id', 'course_id').all():
        if preference.date not in exam_dates:
            exam_dates[preference.date] = []
        exam_dates[preference.date].append(preference)

    if request.method == 'POST':
        form = DutyAllotmentForm(request.POST)
        if form.is_valid():
            print("Form is valid")
            print("Cleaned data:", form.cleaned_data)

            user = form.cleaned_data['user']
            course_id = form.cleaned_data['course_id']
            date = form.cleaned_data['date']
            room_id = form.cleaned_data['room_id']

            duty_allotment, created = dutyAllotment.objects.get_or_create(
                user=user,
                course_id=course_id,
                date=date,
                room_id=room_id
            )

            if created:
                messages.success(request, 'Duty has been successfully allocated.')
            else:
                messages.warning(request, 'Duty for this user and date already exists.')

            return redirect(reverse('allot_duty'))
        else:
            print("Form is not valid")
            print("Errors:", form.errors)

    else:
        form = DutyAllotmentForm()

    context = {
        'exam_dates': exam_dates,
        'form': form,
        'rooms': room.objects.all(),
    }
    return render(request, 'exam/allot_duty.html', context)



@csrf_exempt
def add_teacher(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        dept_id = request.POST.get('dept_id')
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            # Fetch department instance by its ID
            department = Department.objects.get(dept_id=dept_id)
            
            # Create a new user
            user = User.objects.create_user(username=username, password=password)
            
            # Add user to Teacher group
            group = Group.objects.get(name='Teacher')
            user.groups.add(group)
            
            # Generate a unique teacher_id
            # For simplicity, increment from the last used teacher_id.
            # Replace this logic with a more robust method if needed.
            last_teacher = teacherTable.objects.last()
            if last_teacher:
                teacher_id = last_teacher.teacher_id + 1
            else:
                teacher_id = 1
            
            # Create teacherTable instance
            teacher = teacherTable.objects.create(
                teacher_id=teacher_id,
                name=name,
                dept_id=department,
                user=user
            )

            messages.success(request, 'Teacher added successfully.')
        except Department.DoesNotExist:
            messages.error(request, 'Department does not exist.')
        except Group.DoesNotExist:
            messages.error(request, 'Teacher group does not exist. Please create it.')
        except Exception as e:
            messages.error(request, f'Error adding teacher: {str(e)}')

        return redirect('edit_teacher')

    departments = Department.objects.all()
    return render(request, 'exam/edit_teacher.html', {'departments': departments})


@csrf_exempt
def delete_teacher(request, user_id):
    if request.method == 'POST':
        try:
            teacher = teacherTable.objects.get(user__id=user_id)
            user = teacher.user
            teacher.delete()
            user.delete()
            messages.success(request, 'Teacher deleted successfully.')
        except teacherTable.DoesNotExist:
            messages.error(request, 'Teacher not found.')
        except Exception as e:
            messages.error(request, f'Error deleting teacher: {str(e)}')

        return redirect('edit_teacher')

    departments = Department.objects.all()
    teachers = teacherTable.objects.all()
    return render(request, 'exam/edit_teacher.html', {'departments': departments, 'teachers': teachers})


# def print(request):
#     if request.method == 'POST':
#         form = ExamSelectionForm(request.POST)
#         if form.is_valid():
#             # Extract form data
#             semester = int(form.cleaned_data['semester'])
#             month = form.cleaned_data['month']
#             grad_level = form.cleaned_data['grad_level']
#             date = form.cleaned_data['date']
#             course = form.cleaned_data['course']

#             # Format exam title
#             exam_title = f"{ordinal(semester)} Semester {grad_level} Examination, {month} {date.year}"

#             # Format course information
#             course_code_name = f"Course: {course.course_id.course_code} - {course.course_id.course_title}"

#             # Generate PDF content
#             buffer = BytesIO()
#             doc = SimpleDocTemplate(buffer, pagesize=letter)

#             # Define styles
#             styles = getSampleStyleSheet()
#             custom_title_style = ParagraphStyle(
#                 name='CustomTitle',
#                 alignment=1,
#                 fontSize=18,
#                 spaceAfter=20,
#                 textColor=colors.navy,
#             )
#             custom_header_style = ParagraphStyle(
#                 name='CustomHeader',
#                 alignment=1,
#                 fontSize=22,
#                 spaceAfter=30,
#                 textColor=colors.black,
#             )

#             # Build content
#             content = []
#             content.append(Paragraph(exam_title, styles['Title']))
#             content.append(Spacer(1, 20))
#             content.append(Paragraph(course_code_name, custom_title_style))

#             # Build PDF document
#             doc.build(content)
#             buffer.seek(0)

#             # Prepare HTTP response
#             response = HttpResponse(buffer, content_type='application/pdf')
#             response['Content-Disposition'] = 'inline; filename="exam_label.pdf"'
#             return response
#     else:
#         form = ExamSelectionForm()

#     return render(request, 'exam/print.html', {'form': form})

# def ordinal(n):
#     """Returns the ordinal representation of a number."""
#     return "%d%s" % (n, "tsnrhtdd"[(n//10%10 != 1)*(n % 10 < 4)*n % 10::4])

# views.py
from django.shortcuts import render
from django.http import HttpResponse
from .models import ExamTimeTable
from .forms import ExamSelectionForm
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, Frame, Image
import io

def print_label(request):
    if request.method == 'POST':
        form = ExamSelectionForm(request.POST)
        if form.is_valid():
            course = form.cleaned_data['course']
            
            # Fetching exam details for the selected course
            exam_detail = ExamTimeTable.objects.filter(course_id=course.course_id).first()
            if exam_detail:
                date = exam_detail.date
                buffer = io.BytesIO()
                p = canvas.Canvas(buffer, pagesize=letter)

                # Adding some styles
                styles = getSampleStyleSheet()
                title_style = styles['Heading1']
                title_style.alignment = 1  # Center alignment
                title_style.fontSize = 18  # Larger font size
                title_style.spaceAfter = 20  # Space after title

                normal_style = ParagraphStyle(
                    name='Normal',
                    fontName='Helvetica',
                    fontSize=14,  # Larger font size
                    leading=18,
                    alignment=1  # Center alignment
                )

                # Drawing a border
                p.setStrokeColor(colors.grey)
                p.setLineWidth(2)
                p.rect(40, 400, 530, 200, stroke=1, fill=0)

                # Adding title with year
                title = f"{exam_detail.course_id.semester}th Semester {exam_detail.course_id.grad_level} Examination, {date.year}"
                title_paragraph = Paragraph(title, title_style)
                
                frame = Frame(100, 500, 400, 40, showBoundary=0, topPadding=10)
                frame.add(title_paragraph, p)

                # Adding date
                date_paragraph = Paragraph(date.strftime('%d/%m/%Y'), normal_style)
                frame = Frame(100, 480, 400, 40, showBoundary=0, topPadding=10)
                frame.add(date_paragraph, p)

                # Adding course details
                course_details = f"{exam_detail.course_id.course_code}: {exam_detail.course_id.course_title}"
                course_paragraph = Paragraph(course_details, normal_style)
                frame = Frame(100, 460, 400, 40, showBoundary=0, topPadding=10)
                frame.add(course_paragraph, p)

                p.showPage()
                p.save()

                buffer.seek(0)
                response = HttpResponse(buffer, content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="exam_label.pdf"'
                return response
            else:
                return HttpResponse("No exam found for the selected course.", status=404)
    else:
        form = ExamSelectionForm()

    return render(request, 'exam/print_label.html', {'form': form})



from django.shortcuts import render, redirect
from django.db.models import Count
from django.contrib.auth.models import Group
from .models import teacherTable, preferTable, dutyAllotment, ExamTimeTable, room
from .forms import DutyAllotmentForm
from datetime import date

def no_preference_duty(request):
    today = date.today()
    exam_date = today  # For demonstration, we use today's date. Change as needed.

    # Get all teachers who haven't given their preference for today
    preferred_teachers = preferTable.objects.filter(date=exam_date).values_list('teacher_id', flat=True)
    teacher_group = Group.objects.get(name="Teacher")
    available_teachers = teacherTable.objects.exclude(user_id__in=preferred_teachers).filter(user__groups=teacher_group)

    # Count the total duties taken by each available teacher
    duties_count = dutyAllotment.objects.values('user').annotate(total_duties=Count('user'))

    # Get details of courses and count of teachers already allotted for each course on the given date
    allotted_teachers = dutyAllotment.objects.values('course_id').annotate(count=Count('user'))
    course_details = {a['course_id']: ExamTimeTable.objects.get(id=a['course_id']) for a in allotted_teachers}

    # Prepare context
    context = {
        'available_teachers': available_teachers,
        'duties_count': {d['user']: d['total_duties'] for d in duties_count},
        'allotted_teachers': {course_details[a['course_id']]: a['count'] for a in allotted_teachers},
        'form': DutyAllotmentForm(initial={'date': exam_date})
    }

    if request.method == 'POST':
        form = DutyAllotmentForm(request.POST)
        if form.is_valid():
            user_id = request.POST.get('user')
            if user_id:
                form.instance.user_id = user_id
                form.save()
            
            # Refresh the counts after saving the form
            duties_count = dutyAllotment.objects.values('user').annotate(total_duties=Count('user'))
            allotted_teachers = dutyAllotment.objects.values('course_id').annotate(count=Count('user'))
            course_details = {a['course_id']: ExamTimeTable.objects.get(id=a['course_id']) for a in allotted_teachers}
            context['duties_count'] = {d['user']: d['total_duties'] for d in duties_count}
            context['allotted_teachers'] = {course_details[a['course_id']]: a['count'] for a in allotted_teachers}

            return redirect('no_preference_duty')

    return render(request, 'exam/no_preference_duty.html', context)




# views.py
from django.shortcuts import render
from django.db.models import Count, F

def total_summary(request):
    departments = Department.objects.all()
    duties = dutyAllotment.objects.select_related('user', 'course_id', 'course_id__course_id', 'course_id__dept', 'room_id')
    
    # Create a summary of duties taken by each teacher, including duty dates
    duty_summary = (
        duties
        .values(
            teacher_name=F('user__teachertable__name'), 
            department_name=F('user__teachertable__dept_id__dept_name'),
            duty_date=F('date')
        )
        .annotate(total_duties=Count('id'))
        .order_by('teacher_name')
    )

    context = {
        'departments': departments,
        'duties': duty_summary,
    }
    return render(request, 'exam/total_summary.html', context)


from django.shortcuts import render, redirect
from .forms import ExamSelectionForm

def exam(request):
    if request.method == 'POST':
        form = ExamSelectionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('exam_success')
    else:
        form = ExamSelectionForm()
    return render(request, 'exam/exam.html', {'form': form})

def exam_success(request):
    return render(request, 'exam/exam_success.html')
from django import forms
from .models import preferTable, Course
from .models import Exam,ExamTimeTable
from .models import dutyAllotment,teacherTable
from django.contrib.auth.models import User

# class ExamTimeTable(forms.ModelForm):
#      class Meta:
#          model = ExamTimeTable
#          fields = [ 'dept', 'date', 'time_from', 'time_to','semester', 'course_id']


class PreferTableForm(forms.ModelForm):
     exam_date = forms.DateField(widget=forms.Select())

     class Meta:
         model = preferTable
         fields = ['exam_date']

class CourseAdminForm(forms.ModelForm):
     csv_file = forms.FileField()

     class Meta:
         model = Course
         fields = '__all__'


class ExamAnnounce(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['sem', 'year', 'month', 'grad_level', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'grad_level': forms.Select(choices=[
                ('UG', 'Undergraduate (UG)'),
                ('PG', 'Postgraduate (PG)'),
                ('Int MSc', 'Integrated MSc')
            ])
        }

# class dutyAllotmentForm(forms.Form):
#     course = forms.ModelChoiceField(queryset=ExamTimeTable.objects.all())
#     date = forms.DateField()
#     max_teachers = forms.IntegerField(min_value=1, label="Max Teachers per Day")
    



# class DutyAllotmentForm(forms.ModelForm):
#     user = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput())

#     class Meta:
#         model = dutyAllotment
#         fields = ['user', 'course_id', 'date', 'room_id']
#         widgets = {
#             'course_id': forms.HiddenInput(),
#             'date': forms.HiddenInput(),
#         }

class DutyAllotmentForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput())

    class Meta:
        model = dutyAllotment
        fields = ['user', 'course_id', 'date', 'room_id']
        widgets = {
            'course_id': forms.HiddenInput(),
            'date': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
        }

# class ExamSelectionForm(forms.Form):
#     semester = forms.ChoiceField(choices=[(i, i) for i in range(1, 9)])
#     month = forms.ChoiceField(choices=[(exam.month, exam.month) for exam in Exam.objects.all()])
#     grad_level = forms.ChoiceField(choices=[(exam.grad_level, exam.grad_level) for exam in Exam.objects.all()])
#     date = forms.DateField(widget=forms.SelectDateWidget)
#     course = forms.ModelChoiceField(queryset=ExamTimeTable.objects.all())


# class ExamSelectionForm(forms.Form):
#     course = forms.ModelChoiceField(queryset=ExamTimeTable.objects.all().order_by('course_id__course_title'))



# forms.py
from django import forms
from django.contrib.auth.models import User, Group
from .models import dutyAllotment

class DutyAllotmentForm(forms.ModelForm):
    class Meta:
        model = dutyAllotment
        fields = ['user', 'course_id', 'date', 'room_id']

    def __init__(self, *args, **kwargs):
        super(DutyAllotmentForm, self).__init__(*args, **kwargs)
        teacher_group = Group.objects.get(name="Teacher")
        self.fields['user'].queryset = User.objects.filter(groups=teacher_group)


from django import forms
from .models import Course, ExamTimeTable, Department

class ExamSelectionForm(forms.ModelForm):
    class Meta:
        model = ExamTimeTable
        fields = ['course_id', 'dept', 'date', 'time_from', 'time_to', 'semester']

    course_id = forms.ModelChoiceField(queryset=Course.objects.all().order_by('course_title'))
    dept = forms.ModelChoiceField(queryset=Department.objects.all().order_by('dept_name'))
    date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))
    time_from = forms.TimeField(widget=forms.TextInput(attrs={'type': 'time'}))
    time_to = forms.TimeField(widget=forms.TextInput(attrs={'type': 'time'}))
    semester = forms.IntegerField()
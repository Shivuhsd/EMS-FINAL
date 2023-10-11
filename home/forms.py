from . models import StudentCSV, OTP, Student_data, Dept, Course, StudentData, Time_Table
from django import forms

class CSV_S(forms.ModelForm):
    class Meta:
        model = StudentCSV
        fields = ['file_name','csv_file']


class OTP_OTP(forms.ModelForm):
    class Meta:
        model = OTP
        fields = '__all__'

class Student(forms.ModelForm):
    class Meta:
        model = Student_data
        fields = ['photo']


class MyDept(forms.ModelForm):
    class Meta:
        model = Dept
        fields = '__all__'


class MyCourse(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'

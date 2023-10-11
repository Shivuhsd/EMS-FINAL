from django.contrib import admin
from .models import StudentCSV, Time_Table, StudentData, Student_data, OTP, Room, Add_Staff, Subjects, Link, Dept, Course, Eligibility, Student_seat, Staff, Noti

# Register your models here.

admin.site.register(StudentCSV)
admin.site.register(StudentData)
admin.site.register(OTP)
admin.site.register(Subjects)
admin.site.register(Link)
admin.site.register(Add_Staff)
admin.site.register(Room)
admin.site.register(Dept)
admin.site.register(Student_data)
admin.site.register(Time_Table)
admin.site.register(Course)
admin.site.register(Eligibility)
admin.site.register(Student_seat)
admin.site.register(Staff)
admin.site.register(Noti)
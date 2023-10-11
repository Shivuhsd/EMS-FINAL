from django.db import models
from django.contrib.auth.models import User


# Create your models here.


#Department
class Dept(models.Model):
    name = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

#Course
class Course(models.Model):
    dept = models.ForeignKey(Dept, on_delete=models.CASCADE)
    course_id = models.CharField(max_length=20, blank=True)
    name = models.CharField(max_length=100, blank=True)
    sems = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.course_id

class StudentData(models.Model):
    usn = models.CharField(max_length=20, null=False)
    name = models.CharField(max_length=100, null=False)
    father_name = models.CharField(max_length=100, null=False)
    mother_name = models.CharField(max_length=100, null=False)
    dept_name = models.CharField(max_length=100, blank=True)
    course = models.CharField(max_length=100, null=False)
    dob = models.DateField()
    mobile = models.CharField(max_length=12, null=False)
    sem = models.IntegerField(blank=True)

    def __str__(self):
        return self.usn + " --- " +self.name


class StudentCSV(models.Model):
    file_name = models.CharField(max_length=100, null=True)
    csv_file = models.FileField(upload_to='student_csv/')



#model for OTP
class OTP(models.Model):
    otp = models.CharField(max_length=10)
    otp_usn = models.CharField(max_length=100, null=False)


#model for Room
class Room(models.Model):
    room_number = models.CharField(max_length=4, blank=True)
    capacity = models.IntegerField(blank=True)
    status = models.BooleanField(blank=True, default=True)


    def __str__(self):
        return self.room_number
    

class Staff(models.Model):
    uid = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, default=None)
    dept = models.ForeignKey(Dept, on_delete=models.CASCADE)
    status = models.BooleanField(blank=True, default=True)

#model for Adding Staff
class Add_Staff(models.Model):
    name = models.CharField(max_length=100, blank=True)
    dept = models.ForeignKey(Dept, on_delete=models.CASCADE)
    mail = models.EmailField(blank=True)


    def __str__(self):
        return self.name
    


#Alternate Model To Link Student Staff and Room
class Student_seat(models.Model):
    seat = models.CharField(max_length=4, blank=True)
    student = models.ForeignKey(StudentData, on_delete=models.CASCADE)
    cour = models.CharField(max_length=10, blank=True)


#model to Link Students, Staff, Room
class Link(models.Model):
    st = models.ForeignKey(Student_seat, on_delete=models.DO_NOTHING)
    staff = models.ForeignKey(Staff, on_delete=models.DO_NOTHING)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)



#Model for Subjects
class Subjects(models.Model):
    cor = models.ForeignKey(Course, on_delete=models.CASCADE)
    sub_code = models.CharField(max_length=32, blank=True)
    sub_name = models.CharField(max_length=199, blank=True)
    sem = models.IntegerField(blank=False, null=True)

    def __str__(self):
        return self.sub_code + "----" + self.sub_name



##
class Student_data(models.Model):
    u_id = models.ForeignKey(StudentData, on_delete=models.CASCADE, blank=False)
    photo = models.ImageField(blank=False, upload_to='p_photo/')



### Time Table

class Time_Table(models.Model):
    date = models.DateField(blank=False)
    sub_code = models.ForeignKey(Subjects, on_delete=models.CASCADE)
    from_time = models.TimeField(blank=False)
    to_time = models.TimeField(blank=False)
    detp = models.ForeignKey(Dept, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    sem = models.IntegerField(blank=True)
    

###To Store Eligibility of a Student

class Eligibility(models.Model):
    eligibility = models.BooleanField(blank=True)
    student = models.ForeignKey(StudentData, on_delete=models.CASCADE)
    cor = models.CharField(max_length=100, blank=True)



###Report Table

class Report(models.Model):
    usr = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(blank=True)


###Notifications Table

class Noti(models.Model):
    message = models.TextField(blank=True)
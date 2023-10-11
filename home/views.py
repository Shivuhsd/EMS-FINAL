from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from . models import StudentData, StudentCSV, Student_data, Add_Staff, OTP, Subjects, Dept, Room, Course, Time_Table, Eligibility, Link, Student_seat, Staff, Report, Noti
import csv
from . forms import CSV_S, OTP_OTP, Student, MyDept, MyCourse
import os
from .sendingmail import Sending_Mail
from .custom import GenerateOTP, Schedule
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from io import BytesIO
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.http import HttpResponse

# Create your views here.

def LoginPage(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Check Your Credentials")
            
        # Return an 'invalid login' error message.
        ...
    return render(request, 'login.html')


def dashboard(request):
    data = StudentData.objects.filter(sem = 1, course = 'MCA')
    print(len(data))
    return render(request, 'dashboard.html')


def StudentUpload(request):
    form = CSV_S()
    if request.method == 'POST':
        file_csv = CSV_S(request.POST, request.FILES)
        if file_csv.is_valid():
            obj = file_csv.save()
            name_file = obj.id

            
            file_name = StudentCSV.objects.get(id = name_file)
           
            
            path_csv = os.path.join('media', file_name.csv_file.name)

            with open(path_csv, 'r') as file:
                csv_file = csv.DictReader(file)
                for row in csv_file:
                    usn = row['USN']
                    name = row['Name']
                    father_name = row['Father Name']
                    mother_name = row['Mother Name']
                    phone = row['Phone']
                    dob = row['DOB']
                    dept = row['Department']
                    course = row['Course']
                    sem = row['Sem']

                    data = StudentData(usn=usn, name = name, father_name = father_name, mother_name = mother_name, dept_name = dept, mobile = phone, dob = dob, course = course, sem=sem)
                    data.save()
        else:
            messages.error(request, "SomeThing Went Wrong")

    
        
    return render(request, 'supload.html', {'form':form})



def ShowUpload(request):
    return render(request, 'showupload.html')


def Validate(request):
    if request.method == 'POST':
        usn = request.POST['usn']
        phone = request.POST['phone']

        try:
            form = StudentData.objects.get(usn = usn, mobile = phone)
            pk = form.id
            return redirect('emailveri', pk=pk)
        except:
            messages.error(request, "Check Your Credentials")

    return render(request, 'validate.html')


def EmailVeri(request, pk):
    if request.method =='POST':
        e_mail = request.POST['mail']

        form = StudentData.objects.get(id = pk)

        #Storing the Generated OTP To Database
        otp = GenerateOTP()

        OTP(otp=otp, otp_usn=form.usn).save()

        subject = "OTP Verification"
        message = "Hi " + form.name + '\n' + form.usn + "\n\n" + "Your OTP is  " + otp
        try:
            Sending_Mail(subject, message, e_mail)
            return redirect("otpverify", pk=form.usn, e_mail=e_mail)
        except:
            messages.error(request, "Something Went Wrong")

    return render(request, 'emailveri.html')

def OtpVerify(request, pk, e_mail):
    if request.method == 'POST':
        otp = request.POST['otp']

        data = OTP.objects.get(otp=otp, otp_usn = pk)

        if data:
            messages.success(request, "Verification Success")
            da = data
            data.delete()
            return redirect('password', pk=da.otp_usn, e_mail=e_mail)
        else:
            messages.error(request, "OTP Verification Failed")
    return render(request, 'otp.html')


def Password(request, pk, e_mail):
    data = StudentData.objects.get(usn=pk)
    if request.method == 'POST':
        pass_word1 = request.POST['password1']
        pass_word2 = request.POST['password2']

        if pass_word1 != pass_word2:
            messages.error(request, 'Passwords Dont Match')
        else:
            user = User.objects.create_user(data.usn, e_mail, pass_word1)
            user.first_name = data.name
            user.save()
            login(request, user)
            return redirect('dashboard')
    return render(request, 'password.html', {'data':data, 'email':e_mail})

#DashBoard Examination View
def Dash_Examination(request):
    return render(request, 'admins/dash_Examination.html')



#Dashboard Admin add staff view
def Dash_Admin_Add_Staff(request):
    dept = Dept.objects.all()
    if request.method == 'POST':
        dept = request.POST['dept']
        name = request.POST['name']
        mail = request.POST['mail']

        depts = Dept.objects.get(name=dept)

        subject = "Register Yourself At Portal"

        message = "Hi Welcome...\n\nRegister Your self at http://127.0.0.1:8000/staffregister/" 

        Sending_Mail(subject, message, mail)

        data = Add_Staff(name = name, dept = depts, mail = mail)

        data.save()

        messages.success(request, 'Staff Added Succesfully')
    return render(request, 'admins/dash_admin_addstaff.html', {'dept': dept})


#Dashboard Admin add Subjects View



#Dashboard Admin HallTicket Generation
def AdminHallticket(request, dp, cor):
    dept = Dept.objects.get(id=dp)
    cor = Course.objects.get(id=cor)    
    sem = list(range(cor.sems+1))[1:]
    sub = None
    sheduled = None
    su = None
    subs = None
    sems1 = 0
    sems = sems1

    #Code To Get Already Scheduled
    
    
    

    if request.method == 'POST':
        sems1 = 0
        try:
            sems = request.POST['sem']
            print(sems)
        except:
            pass
        try:

            subs = request.POST['sub']
         
        except:
            pass
   
        date = request.POST['date']
        start_time = request.POST['start_time']
        end_time = request.POST['end_time']


        try:
            sheduled = Time_Table.objects.filter(detp = dept, course = cor, sem = sems)
        except:
            pass

        if subs:
            su = Subjects.objects.get(sub_name = subs)
            messages.success(request, 'Sheduled')
       

        if su:
            data = Time_Table(course = cor, sub_code = su, date = date, from_time = start_time, to_time = end_time, detp = dept, sem = su.sem)
            data.save()

        try:
            sub = Subjects.objects.filter(sem = sems, cor = cor.id)
        except:
            pass

    context = {'dept':dept, 'cor':cor, 'sem':sem, 'sub':sub, 'sheduled':sheduled, 'selsem':sems}
    return render(request, 'admins/hallticket.html', context)


#Dashboard Student Hall Ticket View
def Dash_Admin_HallTicketGeneration(request):
    sd = StudentData.objects.get(usn = request.user.username)
    cr = Course.objects.get(name = sd.course)
    data = Time_Table.objects.filter(sem = sd.sem, course = cr)
    pho = Student_data.objects.get(u_id = sd.id)

    try:
       Eligibility.objects.get(student = sd)
    except:
        return HttpResponse("You Are Not Eligible Contact Your Department")

    return render(request, 'student/dash_admin_hallticket.html', {'data':data, 'sd':sd, 'pho':pho})


#selecting Dept before adding subject
def SelectDept(request):
    dept = Dept.objects.all()
    return render(request, 'admins/dash_select_dept.html', {'dept':dept})



#selecting Course after dept
def SelectCourse(request, dp):
    cor = Course.objects.filter(dept = dp)
    dp = Dept.objects.get(id=dp)
    return render(request, 'admins/dash_select_cor.html', {'course':cor, 'dp':dp})


#Dashborad for Adding Subjects
def Add_Subject(request, dp, cr):
    cour = Course.objects.get(id=cr)
    dp = Dept.objects.get(id=dp)
    sem = list(range(cour.sems+1))[1:]
    if request.method == 'POST':
        sub_code = request.POST['sub_code']
        sub_name = request.POST['sub_name']
        sem = request.POST['sem']
        print(sem)

        data = Subjects(sub_code = sub_code, sub_name=sub_name, cor = cour, sem=sem)
        data.save()
        messages.success(request, "Subject Added Succesfully")
      
    return render(request, 'admins/dash_admin_subjects.html', {'course':cour, 'sem':sem, 'dept':dp})


###
def Add_Room(request):
    if request.method == 'POST':
        num = request.POST['num']
        cap = request.POST['capacity']

        data = Room(room_number = num, capacity = cap)
        data.save()

        messages.success(request, 'Room Added Successfully')
        
    return render(request, 'admins/dash_admin_room.html')


###Profile

def Profile(request):
    data = StudentData.objects.get(usn = request.user.username)
    photo = None
    try:
        photo = Student_data.objects.get(u_id=data)
    except:
        pass
    if request.method == 'POST':
        photo = request.FILES['photo']
        i___id = request.user.username
        dat = StudentData.objects.get(usn = i___id)
        data = Student_data(u_id=dat, photo=photo)
        data.save()
        
        messages.success(request, 'Updated Successfully')
        return redirect('profile')
    #else:
     #   messages.error(request, 'Something Went Wrong')
    return render(request, 'student/profile.html', {'data':data, 'photo':photo})


#
def addDept(request):
    form = MyDept()
    if request.method == 'POST':
        data = MyDept(request.POST)
        data.save()
        messages.success(request, "Department Added Succesfully")
    else:
        messages.error(request, "Something Went Wrong")
    return render(request, 'admins/admin_add_dept.html', {'form':form})


#
def addCourse(request):
    form = MyCourse()
    if request.method == 'POST':
        data = MyCourse(request.POST)
        if data.is_valid():
            data.save()
            messages.success(request, "Course Added Succesfully")
        else:
            messages.error(request, "Something Went Wrong")
    return render(request, 'admins/dash_add_course.html', {'form':form})


#Selecting Department Before Selecting Course for HallTicket Generation
def seldept(request):
    dept = Dept.objects.all()
    return render(request, 'admins/select_dept.html', {'dept':dept})


#Selcecting Cors Before Generating Hallticket for Scheduling 
def selcor(request, dp):
    cor = Course.objects.filter(dept = dp)
    dept = Dept.objects.get(id = dp)
    return render(request, 'admins/select_coure.html', {'cor':cor, 'dept':dept})


def Allotment(request):
    data = Schedule()
    return render(request, 'admins/dash_admin_allot.html', data)







### Major Fucntion to Allocate Student to Rooms
def DateAllot(request, pk):
    dct = {}
    s_lst = []
    sum, cap, sr = 0, 0, None
    sub = Time_Table.objects.filter(date=pk)

   


    rom = Room.objects.filter(status = True)
    staff = Staff.objects.filter(status = True)

     #Getting Only Department of Exam Writing Students

    for s in staff:
        for i in sub:
            if s.dept != i.detp:
                s_lst.append(s)

    s_lst = list(dict.fromkeys(s_lst))

    #Finding Number of Staff
    s_num = len(s_lst)




    #Calculating the Capacity of Available Rooms
    for i in rom:
        cap = cap + i.capacity

    
    sss = []

    s_stu = []

    #Calculating Number of Rooms Available 

    no_r = len(rom)

    dct_1 = {}

    t = 0

    for i in sub:
        
        s_stu = []
        sss.append(i.sub_code.sem)
        s = i.sub_code.sem
        stu = Eligibility.objects.filter(cor = i.sub_code.cor.name, eligibility=True)

        for j in stu:
            if j.student.sem == s:
                s_stu.append(j.student)
        



        dct[i.sub_code.sub_name] = len(s_stu)
        dct_1[i.sub_code.sub_name] = s_stu
            


    for i in dct.values():
        sum = sum+i

    #Calculating Capacity with Number of Students
    if sum <= cap:
        pass
    else:
        sr = "Low Capacity Add More Rooms..."




    
    #for i in range(50):
     #   print(Alpha[count] + str(Num) + "\n")
      #  Num += 1
       # print(Num)


        #if Num == 20:
         #   count = count + 1
          #  Num = 1

    Alpha = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
    Num = 1

    s = 1
    count = -1
    cour = None

    c1 = cour
    if request.method == 'POST':
        for i in dct_1.values():
            for j in i:
                cour = j.course #MCA
                if c1 == j.course: #MCA == MCA
                    
                    pass
                else:
                    count += 1
                    Num = 1
                    c1 = j.course
                data = Student_seat(seat = (Alpha[count] + str(Num)), student = j, cour = j.course)
                data.save()
                Num += 1
                s += 1
        
        count = 0
        s_count = -1
        print(sub)
        for i in sub:
            count = 0
            s_count = -1
            print("Start")
            n = dct[i.sub_code.sub_name] #Total Number of Students

            page_counter = 1
            for j in rom: #Iterating Through Rooms Available
                s_count += 1
                c = j.capacity/2 #Dividing One Room into Two Halfes

                quer = Student_seat.objects.filter(cour = i.course.name)
                
                page = Paginator(quer, c)

                page_obj = page.get_page(page_counter)

                print('New Page')
                for k in page_obj:
                    print("Broo......")
                    data = Link(st = k, staff = s_lst[s_count], room = j)
                    data.save()
                    count += 1
                page_counter += 1

                if count == n:
                    break

        return redirect('allotpdf')
    
                


    context = {'sub':sub, 'dct':dct, 'sum':sum, 'cap':cap, 'no_r':no_r, 'sr': sr, 's_num': s_num}
    return render(request, 'admins/admin_allot_stage.html', context)



def AllotPDF(request):
    data = Link.objects.all()

    templat = get_template('admins/allot.html')
    html = templat.render({'data':data})
    results = BytesIO()

    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), results)

    Link.objects.all().delete()
    Student_seat.objects.all().delete()
    

    if not pdf.err:
        Res =  HttpResponse(results.getvalue(), content_type='application/pdf')
        Res['Content-Disposition'] = 'attachment; filename="Examination Seat Allotment PDF.pdf"'
        return Res
    else:
        return None
    


def AdmitPDF(request):
    sd = StudentData.objects.get(usn = request.user.username)
    cr = Course.objects.get(name = sd.course)
    data = Time_Table.objects.filter(sem = sd.sem, course = cr)
    pho = Student_data.objects.get(u_id = sd.id)

    print(pho.photo.url)


    templat = get_template('student/downadmit.html')
    html = templat.render({'data':data, 'sd':sd, 'pho':pho})
    results = BytesIO()

    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), results)

    if not pdf.err:
        Res =  HttpResponse(results.getvalue(), content_type='application/pdf')
        Res['Content-Disposition'] = 'attachment; filename="AdminCard.pdf"'
        return Res
    else:
        return None
    


###Adding Eligibility for Students
def AddEli(request):
    return render(request, 'staff/stueli.html')


def StaffRegister(request):
    mails = None
    if request.method == 'POST':
        username = request.POST['username']
        mail = request.POST['mail']
        name = request.POST['name']
        p1 = request.POST['password1']

        try:
            mails = Add_Staff.objects.get(mail = mail)

            try:
                m = User.objects.get(email = mails.mail)
            except:
                pass

            user = User.objects.create_user(username, email=mails.mail, password=p1, is_staff = True, first_name = name)
            user.save()

            obj = User.objects.get(email = mail)
            data = Staff(uid = obj, dept = mails.dept)
            data.save()

        except:
            pass
    else:
        messages.error(request, 'Something Went Wrong')
   
    return render(request, 'staff/staffregister.html')



def Studenteli(request):
    data = None
    staff = None
    if request.user.is_staff:
        user = request.user
        staff = Staff.objects.get(uid = user)
        data = Course.objects.filter(dept = staff.dept)
    else:
        return HttpResponse("You Are Not Allowed To See This Page")
    
    if request.method == 'POST':
        cor = request.POST['cor']
        sem = request.POST['sem']
        print(cor, sem)
        data = StudentData.objects.filter(course = cor, sem = sem)
        return render(request, 'staff/stueli.html', {'data':data})
    return render(request, 'staff/corasem.html', {'data':data, 'dpt': staff.dept})



def StudentEliDetail(request, pk):
    data = StudentData.objects.get(id = pk)
    if request.method == 'POST':
        eli = request.POST['eli']

        if eli == 'on':
            che = True
        else:
            che = False

        info = Eligibility(eligibility = che, student = data, cor = data.course)
        info.save()

        return redirect('studenteli')
    return render(request, 'staff/studentdetail.html', {'data': data})



def Reports(request):
    if request.method == 'POST':
        mes = request.POST['mes']
        data = Report(usr = request.user, message = mes)
        data.save()
    return render(request, 'report.html')


def Notification(request):
    data = Noti.objects.all()
    if request.method == 'POST':
        mes = request.POST['mes']
        print(mes)
        dat = Noti(message=mes)
        dat.save()
    return render(request, 'notification.html', {'data':data})


def ReadReport(request):
    data = Report.objects.all()
    if request.method == 'POST':
        mes = request.POST['mes']

        subject = "Reply To Your Report"

        mail = request.user.email
        Sending_Mail(subject, mes, mail)
    else:
        messages.error(request, "Something Went Wrong")
    return render(request, 'admins/readreport.html', {'data':data})


def usrlogout(request):
    logout(request)
    return redirect('loginpage')
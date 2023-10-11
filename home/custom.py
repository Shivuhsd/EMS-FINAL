###Custom Functions
from .models import Time_Table, Student_data, Subjects, Room

#Function to Generate OTP
import random
import string
def GenerateOTP():
    n = 6
    otp = "".join(random.choices(string.ascii_uppercase + string.digits, k=n))
    return otp




#Funtion to create a dictionary of dates, subjects, number of students based on time table scheduling

context = None
def Schedule():
    lst = []
    dates = Time_Table.objects.all()
    for i in dates:
        lst.append(i.date)


    lst = list(dict.fromkeys(lst))


        

        
    context = {'dates': lst}
    return context




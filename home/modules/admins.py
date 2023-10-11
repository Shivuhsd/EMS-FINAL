from ..models import Subjects, Room, Add_Staff 
from django.shortcuts import render

#admin fucntion definition 

def Admin_view(request):
    if request.method == 'POST':
        pass
    return render(request, 'admins/hallticket.html')
from django.shortcuts import render,redirect
from.models import *
from django.contrib import messages
from adminapp.models import Book
import requests


# Create your views here.
def index(request):
    context = {
        'userid': request.session.get('userid'),
        'books': Book.objects.all(),
        'new_arrivals':Book.objects.all()[:10]
    }
    return render(request,'index.html',context)

def about(request):
    context = {
        'userid': request.session.get('userid'),
        
    }
    return render(request,'about.html',context)

def contact(request):
    if request.method =='POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        contactno = request.POST.get('contactno')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        enq = Enquiry(name=name,email=email,contactno=contactno,subject=subject,message=message)
        enq.save()
        url = "http://sms.bulkssms.com/submitsms.jsp"
        params = {
            "user": "BRIJESH",
            "key": "066c862acdXX",
            "mobile": "0945318798",
            "message": "Thanks for enquiry we will contact you soon.\n\n-Bulk SMS",
            "senderid": "UPDSMS",
            "accusage": "1",
            "entityid": "1201159543060917386",
            "tempid": "1207169476099469445"
        }

        response = requests.get(url, params=params)
        print("Response:", response.text)
        messages.success(request,"Your enquary has been submitted successfully.")
        return redirect('contact')
    return render(request,'contact.html')


def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        contactno = request.POST.get('contactno')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')
        if password != cpassword:
            messages(request,'Password and Confirm Password should be same')
            return redirect('register')
        ch = LoginInfo.objects.filter(username=email)
        if ch:
            messages.error(request,"Email alredy exists")
            return redirect('register')
        log = LoginInfo(usertype="user",username=email,password=password)
        user = UserInfo(name=name,email=email,contactno=contactno,login=log)
        log.save()
        user.save()
        messages.success(request,"Register is done successfully")
    return render(request,'register.html')
def category(request):
    return render(request,'category.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = LoginInfo.objects.get(usertype='user',username=username, password=password)
            if user is not None:
                request.session['userid'] = username
                messages.success(request, "Login successful")
                return redirect('index')
        except LoginInfo.DoesNotExist:
            messages.error(request, "Invalid Username or Password")
            return redirect('login')
    return render(request,'login.html')

def adminlogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            ad = LoginInfo.objects.get(username=username,password=password)
            if ad is not None:
                request.session['adminid']=username
                messages.success(request,"Welcome Admin")
                return redirect('admindash')
        except LoginInfo.DoesNotExist:
            messages.error(request,"Invalid Username or Password")
            return redirect('adminlogin')    
        
    return render(request,'adminlogin.html')

def book_details(request, id):
    book = Book.objects.get(id=id)
    return render(request,'book_details.html',{'book':book})
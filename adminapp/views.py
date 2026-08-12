from django.shortcuts import render,redirect
from django.contrib import messages
from mainapp.models import *
from .models import *
from useradmin.models import*

from decimal import Decimal
from django.views.decorators.cache import cache_control


# Create your views here.
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admindash(request):
    if not 'adminid' in request.session:
        messages.error(request,"You are not logged in")
        return redirect('adminlogin')
    adminid = request.session.get('adminid')
    context = {
        'adminid':adminid,
        'user_count':UserInfo.objects.all().count(),
        'book_count':Book.objects.all().count(),
        'order_count':Order.objects.all().count(),
        'enquiry_count':Enquiry.objects.all().count(),
    }
    return render(request,'admindash.html',{'adminid':adminid})
@cache_control(no_cache=True, must_revalidate=True, no_store=True)  
def adminlogout(request):
    if 'adminid' in request.session:
        del request.session['adminid']
        messages.success(request,'You are looged out')
        return redirect('adminlogin')
    else:
        return redirect('index')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)   
def viewenq(request):
    if not 'adminid' in request.session:
        messages.error(request,"You are not logged in")
        return redirect('adminlogin')
    enqs = Enquiry.objects.all()
    return render(request,'viewenq.html',{'enqs':enqs})

def delenq(request,id):
    if not 'adminid' in request.session:
        messages.error(request,"You are not logged in")
        return redirect('adminlogin')
    enq = Enquiry.objects.get(id=id)
    enq.delete()
    messages.success(request,'Enquiry Deleted Successfully')
    return redirect('viewenq')
def changepassword(request):
    adminid = request.session.get('adminid')
    if request.method=="POST":
        oldpwd = request.POST.get('oldpwd')
        newpwd = request.POST.get('newpwd')
        confirmpwd = request.POST.get('confirmpwd')
        try:
            admin = LoginInfo.objects.get(username = adminid)
            if admin.password != oldpwd:
                messages.error(request,"Old password is incorrect")
                return redirect('changepassword')
            elif newpwd != confirmpwd:
                messages.error(request,"New password and confirm password are not same")
                return redirect('changepassword')
            elif admin.password == newpwd:
                messages.error(request,"New password and old password are same")
                return redirect('changepassword')
            else:
                admin.password = newpwd
                admin.save()
                messages.success(request,"Your password has been change")
                return redirect('admindash')
        except LoginInfo.DoesNotExist:
            messages.error(request,"Something went wrong")
            return redirect('adminlogin')
        
    return render(request,'changepassword.html',{'adminid':adminid})
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def addcat(request):
    if not 'adminid' in request.session:
        messages.error(request,'You are not logged in')
        return redirect('adminlogin')
    if request.method == "POST":
        name = request.POST.get('name')
        description = request.POST.get('description')
        cat = Category(name=name,description=description)
        cat.save()
        messages.success(request,'Category Added Successfuly')
        return redirect('addcat')
    return render(request,'addcat.html')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def viewcat(request):
    if not 'adminid' in request.session:
        messages.error(request,'You are not logged in')
        return redirect('adminlogin')
    cats = Category.objects.all()
    return render(request,'viewcat.html',{'cats':cats})
def delcat(request,id):
    if not 'adminid' in request.session:
        messages.error(request,"You are not logged in")
        return redirect('adminlogin')
    cat = Category.objects.get(id=id)
    cat.delete()
    messages.success(request,'Enquiry Deleted Successfully')
    return redirect('viewcat')
def addbook(request):
    if not 'adminid' in request.session:
        messages.error(request,'You are not logged in')
        return redirect('adminlogin')
    cats = Category.objects.all()
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        catid = request.POST.get('category')
        cat = Category.objects.get(id=catid)
        description = request.POST.get('description')
        original_price = Decimal(request.POST.get('original_price'))
        price =Decimal(request.POST.get('price'))
        published_date = request.POST.get('published_date')
        language = request.POST.get('language')
        cover_image = request.FILES.get('cover_image')
        stock = request.POST.get('stock')
        book = Book(title=title,author=author,category=cat,description=description,original_price=original_price,price=price,published_date=published_date,language=language,cover_image=cover_image,stock=stock)
        book.save()
        messages.success(request,'New Book is Added Successfully')
        return redirect('addbook')
    return render(request,'addbook.html',{'cats':cats})
   
def viewbook(request):
    if not 'adminid' in request.session:
        messages.error(request,'You are not logged in')
        return redirect('adminlogin')
    books = Book.objects.all()
    return render(request,'viewbook.html',{'books':books})

def adminorders(request):
    if not 'adminid' in request.session:
        messages.error(request,"You are not logged in")
        return redirect('adminlogin')
    adminid = request.session.get('adminid')
    context = {
        'adminid':adminid,
        'orders':Order.objects.all().order_by('ordered_at'),
    }
    return render(request,'adminorders.html',{'adminid':adminid})
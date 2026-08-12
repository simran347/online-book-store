from django.urls import path
from . import views

urlpatterns = [
    path('admindash/',views.admindash,name='admindash'),
    path('adminlogout/',views.adminlogout,name='adminlogout'),
    path('viewenq/',views.viewenq,name='viewenq'),
    path('delenq/<id>',views.delenq,name='delenq'),
    path('changepassword/',views.changepassword,name='changepassword'),
    path('addcat/',views.addcat,name='addcat'),
    path('viewcat/',views.viewcat,name='viewcat'),
    path('addbook/',views.addbook,name='addbook'),
    path('viewbook/',views.viewbook,name='viewbook'),
    path('addcat/<id>',views.delcat,name='delcat'),
    path('adminorders/',views.adminorders,name='adminorders'),
    
]
from django.db import models

# Create your models here.
class Enquiry(models.Model):
        id = models.AutoField(primary_key=True)
        name = models.CharField(max_length=100)
        email = models.EmailField(max_length=100)
        contactno = models.CharField(max_length=15)
        subject =models.CharField(max_length=200)
        message = models.TextField()
        enqdate = models.DateTimeField(auto_now_add=True)



class  LoginInfo(models.Model):
    usertype = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=250)
    status = models.CharField(max_length=10, default='active')
    def __str__(self):
          return f"{self.usertype}-{self.username}"


class UserInfo(models.Model):
      name =models.CharField(max_length=100)
      email = models.EmailField(max_length=100)
      contactno = models.CharField(max_length=15)    
      address = models.TextField()
      profile = models.ImageField(upload_to='profile',null =True,blank=True)
      login = models.ForeignKey(LoginInfo, on_delete=models.CASCADE)    
      def __str__(self):
          return f"{self.name}-{self.email}"
from django.db import models
from django.db.models import UniqueConstraint

# Create your models here.
class PERSON(models.Model):
    pid=models.AutoField(primary_key=True)
    fname=models.CharField(max_length=50)
    lname=models.CharField(max_length=50,default=" ")
    gender=models.CharField(max_length=10)
    dob=models.CharField(max_length=15)
    phone=models.CharField(max_length=15)
    address=models.CharField(max_length=122)
    bgroup=models.CharField(max_length=10)
    MIssues= models.CharField(max_length=122,default="No")  
    def __str__(self):
        return str(self.pid)
    
            
class DONATION(models.Model):
    did=models.AutoField(primary_key=True)
    ddate=models.DateField()
    dqty= models.IntegerField()
    def __str__(self):
        return str(self.did)
    

class donates(models.Model):
    pid=models.ForeignKey(PERSON, on_delete=models.CASCADE)  
    did=models.ForeignKey(DONATION, on_delete=models.CASCADE)  
   
    def __str__(self):
        return  str(self.pid)+"-"+str(self.did)


class RECEIVE(models.Model):
    rid=models.AutoField(primary_key=True)
    rdate=models.DateTimeField()
    rqty= models.IntegerField()
    hospital_name=models.CharField(max_length=122)
    rbgroup=models.CharField(max_length=10)
    def __str__(self):
        return str(self.rid)
   


class receives(models.Model):
    pid=models.ForeignKey(PERSON, on_delete=models.CASCADE)  
    rid=models.ForeignKey(RECEIVE, on_delete=models.CASCADE) 
    def __str__(self):
        return  str(self.pid)+"-"+str(self.rid)
   

class STOCK(models.Model):
    sbgroup=models.CharField(max_length=10)
    qty=models.IntegerField()
    def __str__(self):
        return self.sbgroup



    
    

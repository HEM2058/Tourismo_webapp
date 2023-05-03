from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Tourist(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE,null=True)
    uname = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    contact = models.CharField(max_length=50)
    sex = models.CharField(max_length=50)
   
    def __str__(self):
        return self.uname
    

class Guide(models.Model):
    #  user = models.OneToOneField(User, on_delete=models.CASCADE,null=True)
     uname = models.CharField(max_length=50)
     email = models.EmailField(max_length=254)
     password = models.CharField(max_length=50)
     country = models.CharField(max_length=50)
     contact = models.CharField(max_length=50)
     sex = models.CharField(max_length=50)
     lat = models.FloatField()
     lng = models.FloatField()
     latitude = models.FloatField(null=True)
     longitude = models.FloatField(null=True)
     def __str__(self):
         return self.uname


class Plan(models.Model):
    tourist = models.ForeignKey(Tourist, on_delete=models.CASCADE)
    status = models.CharField(max_length=20)
    guides = models.ManyToManyField(Guide, related_name='plans')
    guide_requests = models.ManyToManyField(Guide, through='GuideRequest', related_name='plan_requests')
    pcoordinate = models.CharField(max_length=50,null=True)
    dcoordinate = models.CharField(max_length=50,null=True)
    datetime = models.DateTimeField()
    BUDGET_TYPE_CHOICES = (
        ('negotiation', 'Negotiation'),
        ('NRP', 'Nepalese Rupees'),
        ('USD', 'US Dollars')
    )
    budget_type = models.CharField(max_length=20, choices=BUDGET_TYPE_CHOICES, default='negotiation')
    budget_cash = models.PositiveIntegerField(blank=True, null=True, default='')
    
 



class GuideRequest(models.Model):
    guide = models.ForeignKey(Guide, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    date_requested = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)
    
   
# user_id=models.ForeignKey(UserMaster,on_delete=models.CASCADE)
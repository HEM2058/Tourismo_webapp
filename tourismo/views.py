from django.shortcuts import render, redirect
from .models import *
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

def Base(request):
    return render(request,"base.html")

# user pages
def Index1(request):
    return render(request,"index1.html")
def Index2(request):
    return render(request,"index2.html")
def Index3(request):
    return render(request,"index3.html")


# tourist user
def TSignUp(request):
  return render(request,"Tourist/signup.html")
def TSignInPage(request):
  return render(request,"Tourist/login.html")

def TRegistration(request):
    if (request.method=="POST"):

        uname = request.POST["uname"]
        email = request.POST["email"]
        contact = request.POST["contact"]
        country = request.POST["country"]
        sex = request.POST["sex"]
        password = request.POST.get("password")
        cpassword = request.POST.get("cpassword")

        Tuser = Tourist.objects.filter(email=email)  
        if(Tuser):
            msg = "Tourist with this email address is already exist!"
            return render(request,'Tourist/signup.html',{'msg':msg})      
        else:
            if(password==cpassword):
                 Tuser = Tourist.objects.create(uname=uname,email=email,contact=contact, country= country,sex=sex, password=password)
                 return render(request,'Tourist/login.html',{'email':email})

            else:
                msg = "Password and Confirm password does not match !"
                return render(request,'Tourist/signup.html',{'msg':msg})
            
def TSignIn(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            Tuser = Tourist.objects.get(email=email)
        except ObjectDoesNotExist:
            msg = "User with this email address does not exist"
            return render(request, 'Tourist/login.html', {'msg': msg})

        if Tuser.password == password:
            request.session['id'] = Tuser.id
            msg = f"Welcome {Tuser.uname}! You have successfully logged in as Tourist"
            return render(request, 'index2.html', {'msg': msg})
        else:
            msg = "Please enter a valid password"
            return render(request, 'Tourist/login.html', {'msg': msg})


# Guide user
def GSignUp(request):
  return render(request,"Guide/signup.html")
def GSignInPage(request):
  return render(request,"Guide/login.html")

def GRegistration(request):
    if (request.method=="POST"):

        uname = request.POST["uname"]
        email = request.POST["email"]
        contact = request.POST["contact"]
        country = request.POST["country"]
        sex = request.POST["sex"]
        lat = request.POST["lat"]
        lng = request.POST["lng"]
        password = request.POST.get("password")
        cpassword = request.POST.get("cpassword")

        Guser = Guide.objects.filter(email=email)  
        if(Guser):
            msg = "Guide with this email address is already exist!"
            return render(request,'Guide/signup.html',{'msg':msg})      
        else:
            if(password==cpassword):
                 
                 Guser = Guide.objects.create(uname=uname,email=email,contact=contact, country= country,lat=lat, lng=lng, sex=sex, password=password)
                 return render(request,'Guide/login.html',{'email':email})

            else:
                msg = "Password and Confirm password does not match !"
                return render(request,'Guide/signup.html',{'msg':msg})
            
            
def GSignIn(request):
    if (request.method=="POST"):
        email = request.POST.get("email")
        password = request.POST.get("password")
        try:
            Guser = Guide.objects.get(email=email)
        except ObjectDoesNotExist:
            msg = "User with this email address does not exist"
            return render(request, 'Guide/login.html', {'msg': msg})

        if (Guser.password == password):
            request.session['id'] = Guser.id
            request.session['uname'] = Guser.uname
            plan = Plan.objects.all()
            msg = f"Welcome {Guser.uname}! You have successfully logged in as Guide"
            return render(request, 'index3.html', {'msg': msg, 'plan':plan})
        else:
            msg = "Please enter valid password"
            return render(request, 'Guide/login.html', {'msg': msg})  
        

# Creating plan by tourists



def create_plan(request,pk):
    if request.method == 'POST':
        tourist = Tourist.objects.get(pk=pk)
        pcoordinate = request.POST['pcoordinate']
        dcoordinate = request.POST['dcoordinate']
        datetime = request.POST['datetime']
        budget_type = request.POST['budget_type']
        budget_cash = request.POST['budget_cash'] or None  # set to None if blank
        
        # create new Plan object
        plan = Plan.objects.create(
            tourist=tourist,
            pcoordinate=pcoordinate,
            dcoordinate=dcoordinate,
            datetime=datetime,
            budget_type=budget_type,
            budget_cash=budget_cash
        )
        
        msg = "Plan has been successfully posted !"
        return render(request, "index2.html",{'msg':msg})
  
    return render(request, "index2.html")


#Guide application request


def add_guide(request, plan_id, guide_id):
    plan = Plan.objects.get(id=plan_id)
    guide = Guide.objects.get(id=guide_id)
    guide_request, created = GuideRequest.objects.get_or_create(plan=plan, guide=guide)
    if created:
        msg = "You have applied for that plan! Please wait for tourist response"
        return render(request, 'index3.html',{'msg':msg})
    else:
        msg = "You have already applied for that plan!"
        return render(request, 'index3.html',{'msg':msg})
    

def YourPlans(request,pk):
    tourist = Tourist.objects.get(id=pk)
    plans = Plan.objects.filter(tourist=tourist).order_by('-datetime')
    return render(request,'Tourist/plans.html',{'plan':plans})


def accept_guide_request(request,guide_id,plan_id):
    guide = Guide.objects.get(id=guide_id)
    plan = Plan.objects.get(id=plan_id)
    guide_request = GuideRequest.objects.get(guide=guide,plan=plan)
    guide_request.accepted = True
    guide_request.save()
    session_id = request.session.get('id')
    # msg = f"You have accepted the request made by {guide.uname}! Please rate the {guide.uname} after your tour."
    return redirect('yourplans', pk=session_id)

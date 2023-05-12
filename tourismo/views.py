from django.shortcuts import render, redirect ,HttpResponse
from .models import *
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.http import JsonResponse
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import datetime
# Create your views here.

def Base(request):
    return render(request,"base.html")

# user pages
def Index1(request):
    return render(request,"index1.html")
def Index2(request):
    return render(request,"index2.html")
def Index3(request):
    plan = Plan.objects.all()
    return render(request,"index3.html",{'plan':plan})
def Help(request):
    return render(request,"help.html")

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
        
        # msg = "Plan has been successfully posted !"
        return redirect('yourplans',pk=pk)
  
    return render(request, "index2.html")


#Guide application request


# def add_guide(request, plan_id, guide_id):
#     plan = Plan.objects.get(id=plan_id)
#     guide = Guide.objects.get(id=guide_id)
  
#     guide_request, created = GuideRequest.objects.get_or_create(plan=plan, guide=guide)
#     session_id = request.session.get('id')
#     if created:
       
#           return redirect('appliedplans', pk=session_id)
#     else:
#           return redirect('appliedplans', pk=session_id)
    
def add_guide(request, plan_id, guide_id):
    plan = Plan.objects.get(id=plan_id)
    guide = Guide.objects.get(id=guide_id)
    tourist_id = plan.tourist.id
    guide_request, created = GuideRequest.objects.get_or_create(plan=plan, guide=guide)
    session_id = request.session.get('id')
    if created:
        expire_at = timezone.now() + datetime.timedelta(days=1)  # set TTL to 1 day
        message = f"The {guide.uname} guide has applied to your plan with ID {plan_id}. Guide ID: {guide_id}"
        TouristNotification.objects.create(tourist=tourist_id,message=message,expire_at=expire_at)
        # Get the channel layer for sending WebSocket messages
        channel_layer = get_channel_layer()
        
        # Get the WebSocket group name for the tourist
        group_name = f'tourist_{plan.tourist.id}'
        
        # Send a WebSocket message to the tourist group
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                'type': 'guide_request_created',
                'plan_id': plan.id,
                'guide_id': guide.id,
                'guide_uname' : guide.uname,
            }
        )
       
        return redirect('appliedplans', pk=session_id)
    else:
        return redirect('appliedplans', pk=session_id)









def YourPlans(request,pk):
    tourist = Tourist.objects.get(id=pk)
    if request.session.get('id') != pk:
        return HttpResponse('<h1>You are not authorized to view this page !</h1>')
    else:
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


def AppliedPlans(request,pk):
    guide = Guide.objects.get(id=pk)
    guiderequest = GuideRequest.objects.filter(guide=guide)
    if request.session.get('id')!=pk:
          return HttpResponse('<h1>You are not authorized to view this page !</h1>')
    else:
          return render(request,'Guide/plans.html',{ 'guiderequest':guiderequest})
    


def get_guide_info_ajax(request, guide_id):
    guide = Guide.objects.get(id=guide_id)
    guide_info = {
        'guide_id':guide_id,
        'uname': guide.uname,
        'contact': guide.contact,
        'email': guide.email,
         'sex'  :guide.sex,
    }
    return JsonResponse(guide_info)





#24 hours notification showing in tourist page 


def get_Tnotifications(request):
    if request.session.get('id') is not None:  # check if tourist is logged in
        tourist_id = request.session['id']
        notifications = TouristNotification.objects.filter(tourist=tourist_id).order_by('-created_at')
        data = []
        for notification in notifications:
            data.append({
                'message': notification.message,
                'created_at': timezone.localtime(notification.created_at).strftime('%Y-%m-%d %H:%M:%S'),
                'expire_at': timezone.localtime(notification.expire_at).strftime('%Y-%m-%d %H:%M:%S'),
            })
        return JsonResponse({'notifications': data})
    else:
        return JsonResponse({'error': 'Tourist not logged in'})
    


#Drive reauest to guide from tourist

def create_guide_request(request, guide_id):
    if request.method == 'POST':
        guide = Guide.objects.get(id=guide_id)
        tourist_id = request.session.get('id')
        tourist = Tourist.objects.get(id=tourist_id)
        tourist_request, created =  TouristRequest.objects.get_or_create(tourist=tourist,guide=guide)
        if created:
             expire_at = timezone.now() + datetime.timedelta(days=1)  # set TTL to 1 day
             message = f"The {tourist.uname} tourist has requested for ride.You can contact them at {tourist.contact}."
             GuideNotification.objects.create(guide=guide.id,message=message,expire_at=expire_at)
              # Get the channel layer for sending WebSocket messages
             channel_layer = get_channel_layer()
        
              # Get the WebSocket group name for the tourist
             group_name = f'guide_{guide.id}'
        
              # Send a WebSocket message to the tourist group
             async_to_sync(channel_layer.group_send)(
              group_name,
              {
                'type': 'tourist_request_created',
                'guide_id': guide.id,
                'tourist_uname' : tourist.uname,
                'tourist_contact':tourist.contact,
            }
        )
             return JsonResponse({'status': 'success'})
        else:
                # Get the channel layer for sending WebSocket messages
             channel_layer = get_channel_layer()
        
              # Get the WebSocket group name for the tourist
             group_name = f'guide_{guide.id}'
        
              # Send a WebSocket message to the tourist group
             async_to_sync(channel_layer.group_send)(
              group_name,
              {
                'type': 'tourist_request_created',
                'guide_id': guide.id,
                'tourist_uname' : tourist.uname,
                 'tourist_contact':tourist.contact,
            }
        )
             return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})
    


def get_Gnotifications(request):
    if request.session.get('id') is not None:  # check if tourist is logged in
        guide_id = request.session['id']
        notifications = GuideNotification.objects.filter(guide=guide_id).order_by('-created_at')
        data = []
        for notification in notifications:
            data.append({
                'message': notification.message,
                'created_at': timezone.localtime(notification.expire_at).strftime('%Y-%m-%d %H:%M:%S'),
                'expire_at': timezone.localtime(notification.expire_at).strftime('%Y-%m-%d %H:%M:%S'),
            })
        return JsonResponse({'notifications': data})
    else:
        return JsonResponse({'error': 'Tourist not logged in'})  
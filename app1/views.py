
from django.shortcuts import render, HttpResponse,redirect,get_object_or_404
from django.views import View
from app1.models import Profile,Message
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.core.exceptions import ObjectDoesNotExist

class registerview(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']

        if cpassword == password:
            # Create a new user instance
            user = User(first_name=first_name, last_name=last_name, username=username, email=email)
            
            # Set and hash the password using set_password
            user.set_password(password)
            
            # Save the user object
            user.save()

            return redirect('login')
        else:
            return render(request, 'register.html', {'alert': "Password does not match"})


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            return render(request, 'login.html', {"alert1": "**Wrong email or password**"})


class logoutview(View):
	def get(self,request):
	    request.session.clear()
	    return redirect('login')
        
#..................................user authentication End................................#
#.........................................................................................#


class Homeview(View):
    @method_decorator(login_required(login_url="login"))
    def get(self,request):
        message_data = Message.objects.filter(sender=request.user)
        # for i in message_data:
        #     print(i.content)
        #     print(i.receiver.username)
        context={
        "message_data":message_data
        }
        return render(request,'home.html',context)

class Editprofileview(View):
    @method_decorator(login_required(login_url='login'))
    def get(self, request):
        user = request.user
        try:
            profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            profile = Profile(user=user)
            profile.save()
        return render(request, 'editprofile.html', {'user_profile': profile})

    def post(self, request):
        user = request.user
        bio = request.POST['bio']
        profile_picture = request.FILES['profile_picture']
        location = request.POST['location']

        # Check if a profile already exists for the user
        try:
            profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            profile = Profile(user=user)

        # Update the profile with the new data
        profile.bio = bio
        profile.profile_picture = profile_picture
        profile.location = location
        profile.save()

        return redirect("profile")
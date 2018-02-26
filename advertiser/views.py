from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render, redirect
from django.views import generic
from django.views.generic import View
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.conf import settings

from api.models import Advertiser
from api.models import TargetedAge,AdvertisementCategory,Category
from .forms import *


class IndexView(View):
    template_name = 'advertiser/dashboard/index.html'

    def get(self, request):
        return render(request, 'advertiser/dashboard/index.html')

    def post(self, request):
        pass

    def logout(self, request):
        del request.session['username']
        return render(request, 'advertiser/login.html')


class DashboardView(View):
    template_name = 'advertiser/dashboard/index.html'

    def get(self, request):
        if 'username' in request.session:
            dash = Advertisement.objects.filter(name=request.session['username']).count
            context = {'dash':dash}
            return render(request, 'advertiser/dashboard/index.html', context)
        else:
            return redirect('/advertiser/login')



class ContactView(View):
    template_name = 'advertiser/website/contact.html'

    def get(self, request):
        return render(request, 'advertiser/website/contact.html')


def index(request):
    return render(request, 'advertiser/website/index.html', {'username': 'Moamen'})


class FormsView(View):
    template_name = 'advertiser/dashboard/forms.html'

    def get(self, request):
        return render(request, 'advertiser/dashboard/forms.html')

    def post(self, request):
        pass


class ChartsView(View):
    template_name = 'advertiser/dashboard/charts.html'

    def get(self, request):
        if 'username' in request.session:
         stuents = Advertisement.objects.filter().count()
         context = {'stuents': stuents}
         return render(request, 'advertiser/dashboard/charts.html', context)
        else:
            return redirect('/advertiser/login/')

    def post(self, request):
        pass


def logout(request):
     if 'username' in request.session:
         del request.session['username']
         return redirect('/advertiser/')


class HomeView(View):
    template_name = 'advertiser/website/index.html'

    def get(self, request):
        return render(request, 'advertiser/website/index.html')

    def post(self, request):
        pass


class LoginFormView(View):
    form_class = LoginForm
    template_name = 'advertiser/login.html'

    def get(self, request):
        if 'username' in request.session:
            if request.session['username'] is None:
                form = LoginForm(None)
                context = {'form': form}
                return render(request, 'advertiser/login.html', context)
            else:
                return redirect('/advertiser/dashboard')
        else:
            form = LoginForm(None)
            context = {'form': form}
            return render(request, 'advertiser/login.html', context)


    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            if Advertiser.objects.filter(name=form.cleaned_data['username']).exists():
                advertiser = Advertiser.objects.get(name=form.cleaned_data['username'])
                if check_password(form.cleaned_data['password'], advertiser.password):
                    username = request.session['username'] =form.cleaned_data['username']
                    context = {'username': username}
                    return redirect('/advertiser/dashboard/', context)
                else:
                    form = LoginForm(None)
                    context = {'form': form, 'msg': 'Incorrect password.'}
                    return render(request, 'advertiser/login.html', context)
            else:
                form = LoginForm(None)
                context = {'form': form, 'msg': 'Username does not exist.'}
                return render(request, 'advertiser/login.html', context)
        else:
            form = LoginForm(None)
            return render(request, 'advertiser/login.html', {'form': form, 'msg': 'Invalid form fml'})


class RegistrationFormView(View):
    form_class = RegistrationForm
    template_name = 'advertiser/registration.html'

    def get(self, request):
        if 'username' in request.session:
            return redirect('/advertiser/')
        form = RegistrationForm(None)
        context = {'form': form}
        return render(request, 'advertiser/registration.html', context)

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():

            if not Advertiser.objects.filter(name=form.cleaned_data['username']).exists():
                if form.cleaned_data['password'] == form.cleaned_data['confirmpassword']:
                    name = form.cleaned_data['username']
                    email = form.cleaned_data['email']
                    password = make_password(form.cleaned_data['password'])
                    phone = form.cleaned_data['phone']
                    Advertiser.objects.create(name=name, email=email, password=password, phone=phone, budget=50)
                    messages.success(request, "Your account has been registered successfully!")
                    return redirect('/advertiser/login')
                else:
                    form = RegistrationForm(None)
                    messages.error(request, 'Password does not match')
                    return render(request, 'advertiser/registration.html',
                                  {'form': form})

            else:
                form = RegistrationForm(None)
                messages.error(request, 'Account with the same username already exists')
                return render(request, 'advertiser/registration.html',
                              {'form': form})


class AdvertisersListView(generic.ListView):
    model = Advertiser
    template_name = 'advertiser/index.html'

    def get_queryset(self):

        return Advertiser.objects.all()


class AdvertisementDetailView(generic.DeleteView):
    model = Advertisement


class AdvertisementFormView(View):
    form_class = Userinput
    template_name = 'advertiser/dashboard/forms.html'

    def get(self, request):
      if 'username' in request.session:
        form = Userinput(None)
        context = {'form': form}
        return render(request, 'advertiser/dashboard/forms.html', context)
      else:
          return redirect('/advertiser/login/')

    def post(self, request):
        form = Userinput(request.POST)
        if form.is_valid():
            if 'username' in request.session:
                username = request.session['username']
                hoss = Advertiser.objects.get(name=username)
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            pub_date = form.cleaned_data['pub_date']
            max_age = form.cleaned_data['max_age']
            min_age = form.cleaned_data['min_age']
            category = form.cleaned_data['category']
            #category = request.POST.getlist('category')
            Advertisement.objects.create(name=name, description=description, pub_date=pub_date, advertiser=hoss)
            pop = Advertisement.objects.get(name=name)
            TargetedAge.objects.create(min_age=min_age, max_age=max_age,advertisement=pop)
            for i in category:
                cat=Category.objects.get(color=i)
                AdvertisementCategory.objects.create(advertisement=pop,category=cat)
        newform = Userinput(None)
        return render(request, 'advertiser/dashboard/forms.html', {'form': newform})


def Student(request):
    stuents = Advertisement.objects.all.count()
    context = {'stuents': stuents}
    return render(request, 'advertiser/dashboard/charts.html', context)


def Index(request):
    stuents = Advertisement.objects.filter(name="Hossam").count()
    context = {'stuents': stuents}
    return render(request, 'advertiser/dashboard/index.html', context)


class ResetFormView(View):
    form_class = EmailForm
    template_name = 'advertiser/email.html'

    def get(self, request):
        if 'username' in request.session:
          return redirect('/advertiser/dashboard/')
        form = RegistrationForm(None)
        context = {'form': form}
        return render(request, 'advertiser/email.html', context)

    def post(self, request):
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            useremail = EmailMessage("ChangePassword", 'Can you change password by this link  '
                                                       'http://127.0.0.1:8000/advertiser/Changepassword/', to=[email])
            useremail.send()

            form = EmailForm(None)
            return render(request, 'advertiser/email.html',
                          {'form': form})



def advertisement(request):
    if 'username' in request.session:
        username = request.session['username']
        hoss = Advertiser.objects.get(name=username)
        stuents = Advertisement.objects.all().filter(advertiser=hoss)
        context = {'stuents': stuents}
        return render(request, 'advertiser/dashboard/update.html', context)
    else:
        return redirect('/advertiser/login/')
	 
	


def delete(request, part_id):
    if 'username' in request.session:
        username = request.session['username']
        hoss = Advertiser.objects.get(name=username)
    stuents = Advertisement.objects.all().filter(advertiser=hoss)
    context = {'stuents': stuents}
    object = Advertisement.objects.filter(id=part_id)
    pp=TargetedAge.objects.filter(advertisement=part_id)
    cat=AdvertisementCategory.objects.filter(advertisement=part_id)
    pp.delete()
    cat.delete()
    object.delete()

    return render(request, 'advertiser/dashboard/update.html',context)


class UpdateFormView(View):
    form_class = update
    template_name = 'advertiser/dashboard/updateData.html'

    def get(self, request, part_id):
        if 'username' not in request.session:
            return redirect('/advertiser/login/')
        form = update(None)
        context = {'form': form}
        return render(request, 'advertiser/dashboard/updateData.html', context)

    def post(self, request, part_id):
        form = update(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            max_age = form.cleaned_data['max_age']
            min_age = form.cleaned_data['min_age']
            category = form.cleaned_data['category']
            Advertisement.objects.filter(id=part_id).update(name=name, description=description)
            TargetedAge.objects.filter(advertisement=part_id).update(max_age=max_age,min_age=min_age)
            for i in category:
                cat=Category.objects.get(color=i)
                AdvertisementCategory.objects.filter(advertisement=part_id).update(category=cat)

            newform = update(None)
            return render(request, 'advertiser/dashboard/updateData.html', {'form': newform})


class ChangepasswordFormView(View):
    form_class = changeForm
    template_name = 'advertiser/changeEmail.html'

    def get(self, request):
        form = changeForm(None)
        context = {'form': form}
        return render(request, 'advertiser/changeEmail.html', context)

    def post(self, request):
        form = changeForm(request.POST)
        if form.is_valid():
            if Advertiser.objects.filter(name=form.cleaned_data['username']).exists():
                if form.cleaned_data['password'] == form.cleaned_data['confirmpassword']:
                    name = form.cleaned_data['username']
                    password = make_password(form.cleaned_data['password'])
                    Advertiser.objects.filter(name=name).update(password=password)
                    return redirect('advertiser/login')

            else:
                messages.error(request, 'Username is not here')

            form = changeForm(None)
            return render(request, 'advertiser/changeEmail.html',
                          {'form': form})

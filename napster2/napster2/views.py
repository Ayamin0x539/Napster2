from napster2.forms import *
from napster2.models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import render

def index(request): # request parameter has host params (ip, etc)
    return render_to_response('index.html', {}, RequestContext(request))

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                email=form.cleaned_data['email']
                )

            person = Person(email = form.cleaned_data['email'])
            person.save()

            return HttpResponseRedirect('/register/success/')
        else:
            return render_to_response('registration/failure.html')
    else:
        form = RegistrationForm()
        variables = RequestContext(request, {'form': form})
        # can pull the variable "form" from the view.
        return render_to_response('registration/register.html', variables,)

def register_success(request):
    return render_to_response('registration/success.html',)

def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')

@login_required
def dashboard(request):
    return render_to_response('dashboard.html', { 'user': request.user })

@login_required
def update_payment_info(request):
    form = EditPaymentsForm(request.POST)
#    if form.is_valid():
    return render_to_response('updatepaymentsuccess.html')

@login_required
def view_cart(request):
    cart = request.session.get('cart', None)
    return render_to_response('view_cart.html', { 'user': request.user })

@login_required
def add_Track_to_cart(request, trackidnum):
    cart = request.session.get('cart', None)
    if cart:
        cart[trackidnum]= Track.objects.all().filter(trackid=trackidnum);
    else:
        request.session['cart'] = cart
        cart[trackidnum]= Track.objects.all().filter(trackid=trackidnum);
    return render_to_response('dashboard.html', { 'user': request.user })

@login_required
def remove_from_cart(request, trackid):
    cart = request.session.get('cart', None)
    if cart[trackid]:
        del cart[trackid];
    else:
        cart=cart
    return render_to_response('dashboard.html', { 'user': request.user })

@login_required
def checkout(request):
    return render_to_response('checkout.html', { 'user': request.user })
    
@login_required
def update_account_info(request):
    if request.method == 'POST':
        form = AccountManagementForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/update/success/')
        else:
            return render_to_response('update/failure.html')
    else:
        form = AccountManagementForm()
        variables = RequestContext(request, {'form': form})
        # can pull the variable "form" from the view.
        return render_to_response('update/update.html', variables,)    

def update_success(request):
    return render_to_response('update/success.html',)

@login_required
def enter_new_media(request):
    form = EmployeeEnterNewMediaForm(request.POST)

@login_required
def run_report(request):
    form = AdministratorRunReportForm(request.POST)

@login_required
def employee_productivity_Report(request):
    form = AdministratorEmployeeProductivityForm(request.POST)

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
    return render_to_response('checkout/view_cart.html', { 'user': request.user })

@login_required
def add_Track_to_cart(request, trackidnum):
    cart = request.session.get('cart', None)
    if cart:
        cart[trackidnum]= Track.objects.all().filter(trackid=trackidnum);
    else:
        request.session['cart'] = cart
        cart[trackidnum]= Track.objects.all().filter(trackid=trackidnum);
    return render_to_response('checkout/view_cart.html', { 'user': request.user })

@login_required
def remove_from_cart(request, trackid):
    cart = request.session.get('cart', None)
    if cart[trackid]:
        del cart[trackid];
    else:
        cart=cart
    return render_to_response('checkout/view_cart.html', { 'user': request.user })

@login_required
def checkout(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = Order()
            order.save()
            return HttpResponseRedirect('/checkout/success/')
        else:
            return render_to_response('checkout/failure.html')
    return render_to_response('checkout/checkout.html', { 'user': request.user })

@login_required
def update_account_info(request):
    if request.method == 'POST':
        form = AccountManagementForm(request.POST)
        for field in form.fields:
            form.fields[field].required = False

        if form.is_valid():
            print("Update is valid!")
            # update the database
            # first, do a select statement. select * from Person where username = <current session dude's username>
            person = Person.objects.get(username=request.user.get_username())
            firstname=form.cleaned_data['firstname']
            if firstname != "":
                person.firstname = firstname
            lastname=form.cleaned_data['lastname']
            if lastname != "":
                person.lastname = lastname
            phone=form.cleaned_data['phone']
            if phone != "":
                person.phone = phone
            email=form.cleaned_data['email']
            if email != "":
                person.email = email
            postalcode=form.cleaned_data['postalcode']
            if postalcode != "":
                person.postalcode = postalcode
            address=form.cleaned_data['address']
            if address != "":
                person.address = address
            city=form.cleaned_data['city']
            if city != "":
                person.city = city
            state=form.cleaned_data['state']
            if state != "":
                person.state = state
            country=form.cleaned_data['country']
            if country != "":
                person.country = country
            fax=form.cleaned_data['fax']
            if fax != "":
                person.fax = fax
            creditcardnumber=form.cleaned_data['creditcardnumber']
            if creditcardnumber != "":
                person.creditcardnumber = creditcardnumber
            paypalemail=form.cleaned_data['paypalemail']
            if paypalemail != "":
                person.paypalemail = paypalemail
            googlepayid=form.cleaned_data['googlepayid']
            if googlepayid != "":
                person.googlepayid = googlepayid
            applepayid=form.cleaned_data['applepayid']
            if applepayid != "":
                person.applepayid = applepayid
            person.save()
            return HttpResponseRedirect('/update/success/')
        else:
            print("update was not valid")
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

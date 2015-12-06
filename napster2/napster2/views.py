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
    person = None
    if request.user.is_authenticated():
        person = Person.objects.get(username=request.user.get_username())
    variables = RequestContext(request, {'person': person})
    return render_to_response('index.html', variables,)

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
            person.username = form.cleaned_data['username']
            person.affiliation = 'Customer'
            person.save()

            return HttpResponseRedirect('/register/success/')
        else:
            person = None
            if request.user.is_authenticated():
                person = Person.objects.get(username=request.user.get_username())
            variables = RequestContext(request, {'person': person})
            return render_to_response('registration/failure.html', variables,)
    else:
        person = None
        if request.user.is_authenticated():
            person = Person.objects.get(username=request.user.get_username())
        variables = RequestContext(request, {'person': person})
        form = RegistrationForm()
        variables = RequestContext(request, {'form': form})
        # can pull the variable "form" from the view.
        return render_to_response('registration/register.html', variables,)

def register_success(request):
    person = None
    if request.user.is_authenticated():
        person = Person.objects.get(username=request.user.get_username())
    variables = RequestContext(request, {'person': person})
    return render_to_response('registration/success.html',)

def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')

@login_required
def dashboard(request):
    person = None
    if request.user.is_authenticated():
        person = Person.objects.get(username=request.user.get_username())
    variables = RequestContext(request, {'person': person, 'user': request.user})
    return render_to_response('dashboard.html', variables,)

@login_required
def view_cart(request):
    track_cart = request.session.get('track_cart', None)
    upl_cart = request.session.get('upl_cart', None)
    epl_cart = request.session.get('epl_cart', None)
    person = None
    if request.user.is_authenticated():
        person = Person.objects.get(username=request.user.get_username())
    variables = RequestContext(request, {'person': person})
    return render_to_response('checkout/view_cart.html', { 'user': request.user })

@login_required
def search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            print("Search form is valid!")
            result = None
            trackname = form.cleaned_data['track']
            albumname = form.cleaned_data['album']
            artistname = form.cleaned_data['artist']
            composername = form.cleaned_data['composer']
            genrename = form.cleaned_data['genre']
            medianame = form.cleaned_data['media']
            
            query = "SELECT * from Track, Album, Artist, Genre, MediaType where Track.AlbumId = Album.AlbumId and Album.ArtistId = Artist.ArtistId and Track.GenreId = Genre.GenreId and Track.MediaTypeId = MediaType.MediaTypeId and Track.Name like \"%%" + trackname + "%%\" and Album.Title like \"%%" + albumname + "%%\" and Artist.Name like \"%%" + artistname + "%%\" and Track.Composer like \"%%" + composername + "%%\" and Genre.Name like \"%%" + genrename + "%%\" and MediaType.Name like \"%%" + medianame + "%%\""

            result = Track.objects.raw(query)

            person = None
            if request.user.is_authenticated():
                person = Person.objects.get(username=request.user.get_username())
            # make a new form for the next search
            form = SearchForm()
            variables = RequestContext(request, {'result': result, 'person': person, 'form': form})
            return render_to_response('search/search.html', variables,)
        else:
            print("Search form fields not valid.")
            person = None
            if request.user.is_authenticated():
                person = Person.objects.get(username=request.user.get_username())
            variables = RequestContext(request, {'person': person})
            return render_to_response('/search/failure.html', variables,)
    else:
        form = SearchForm()
        person = None
        if request.user.is_authenticated():
            person = Person.objects.get(username=request.user.get_username())
        variables = RequestContext(request, {'form': form, 'person': person})
        return render_to_response('search/search.html', variables)

@login_required
def add_track_to_cart(request, trackidnum):
    track_cart = request.session.get('track_cart', None)
    if track_cart:
        track_cart[trackidnum]= Track.objects.all().filter(trackid=trackidnum);
    else:
        request.session['cart'] = cart
        track_cart[trackidnum]= Track.objects.all().filter(trackid=trackidnum);
    return render_to_response('checkout/view_cart.html', { 'user': request.user })

@login_required
def remove_track_from_cart(request, trackid):
    track_cart = request.session.get('cart', None)
    if track_cart[trackid]:
        del track_cart[trackid];
    else:
        track_cart=track_cart
    person = None
    if request.user.is_authenticated():
        person = Person.objects.get(username=request.user.get_username())
    variables = RequestContext(request, {'person': person, 'user': request.user})
    return render_to_response('checkout/view_cart.html', variables,)

@login_required
def add_upl_to_cart(request, idnum):
    upl_cart = request.session.get('upl_cart', None)
    if upl_cart:
        upl_cart[trackidnum]= Track.objects.all().filter(MyPlaylistID=idnum);
    else:
        request.session['upl_cart'] = upl_cart
        upl_cart[trackidnum]= Track.objects.all().filter(MyPlaylistID=idnum);
    return render_to_response('checkout/view_cart.html', { 'user': request.user })

@login_required
def remove_upl_from_cart(request, idnum):
    upl_cart = request.session.get('upl_cart', None)
    if upl_cart[idnum]:
        del upl_cart[idnum];
    else:
        upl_cart=upl_cart
    return render_to_response('checkout/view_cart.html', { 'user': request.user })

@login_required
def add_epl_to_cart(request, idnum):
    epl_cart = request.session.get('epl_cart', None)
    if epl_cart:
        epl_cart[trackidnum]= Track.objects.all().filter(PlaylistID=idnum);
    else:
        request.session['epl_cart'] = epl_cart
        epl_cart[trackidnum]= Track.objects.all().filter(PlaylistID=idnum);
    return render_to_response('checkout/view_cart.html', { 'user': request.user })

@login_required
def remove_upl_from_cart(request, idnum):
    epl_cart = request.session.get('upl_cart', None)
    if epl_cart[idnum]:
        del epl_cart[idnum];
    else:
        epl_cart=epl_cart
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
            return render_to_response('checkout/failure.html', variables,)
    return render_to_response('checkout/checkout.html', variables,)

@login_required
def update_account_info(request):
    if request.method == 'POST':
        form = AccountManagementForm(request.POST)
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
            person = None
            if request.user.is_authenticated():
                person = Person.objects.get(username=request.user.get_username())
            variables = RequestContext(request, {'person': person})
            return render_to_response('update/failure.html', variables)
    else:
        form = AccountManagementForm()
        person = None
        if request.user.is_authenticated():
            person = Person.objects.get(username=request.user.get_username())
        variables = RequestContext(request, {'form': form, 'person': person})
        # can pull the variable "form" from the view.
        return render_to_response('update/update.html', variables,)

def update_success(request):
    person = None
    if request.user.is_authenticated():
        person = Person.objects.get(username=request.user.get_username())
    variables = RequestContext(request, {'person': person})
    return render_to_response('update/success.html', variables,)

@login_required
def run_report(request):
    form = AdministratorRunReportForm(request.POST)

@login_required
def employee_productivity_Report(request):
    form = AdministratorEmployeeProductivityForm(request.POST)


@login_required
def demographics(request):
    customer_numbers = Person.objects.all().count()
    customer_country_numbers = Person.objects.values('country').distinct().count()
    person = None
    if request.user.is_authenticated():
        person = Person.objects.get(username=request.user.get_username())
#    variables = RequestContext(request, {'person': person})
    user = request.user
    return render_to_response('demographics/demographics.html', locals())

@login_required
def manage_orders(request):
    person = None
    if request.user.is_authenticated():
        person = Person.objects.get(username=request.user.get_username())
    variables = RequestContext(request, {'person': person})
    return render_to_response('orders/employee_order_management.html', variables,)

@login_required
def add_tracks(request):
    if request.method == 'POST':
        form = AddTrack(request.POST)
        if form.is_valid():
            print("Update is valid!")
            track.trackname = form.cleaned_data['trackname']
            track.save()
            print("Update was successful.")
            return HttpResponseRedirect('/music_management/success.html')
        else:
            print("Update was not valid.")
            person = None
            if request.user.is_authenticated():
                person = Person.objects.get(username=request.user.get_username())
            variables = RequestContext(request, {'person': person})
            return render_to_response('/music_management/failure.html', variables,)
    else:
        form = AddTrack()
        person = None
        if request.user.is_authenticated():
            person = Person.objects.get(username=request.user.get_username())
        variables = RequestContext(request, {'form': form, 'person': person})
        return render_to_response('music_management/add_tracks.html', variables)

@login_required
def view_MyPlaylist(request):
    if request.user.is_authenticated():
        person = Person.objects.get(username=request.user.get_username())
        person_id = person.personid
    query = "SELECT * from Customer, MyPlaylist where Customer.CustPersonId = \"%%" + str(person_id) + "%%\"  and Customer.CustomerId = MyPlaylist.CustomerID"
    result = Myplaylist.objects.raw(query)
    if request.user.is_authenticated():
        variables = RequestContext(request, {'result': result, 'person': person})
    return render_to_response('MyPlaylist/view_MyPlaylist.html', variables,)
       




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
from django.db import connection
import time
import datetime

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
            print(form.cleaned_data['affiliation'])
            person = Person(email = form.cleaned_data['email'])
            person.username = form.cleaned_data['username']
            
            if form.cleaned_data['affiliation'] == 'Customer':
                person.affiliation = 'Customer'
                person.save()
                print(form.cleaned_data['affiliation'])
                customer = Customer(custpersonid=person)
                customer.save()
            elif form.cleaned_data['affiliation'] == 'Employee':
                person.affiliation = 'Employee'
                person.save()
                employee = Employee(personid=person)
                employee.save()
            elif form.cleaned_data['affiliation'] == 'Administrator':
                person.affiliation = 'Administrator'
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
    if request.method == 'POST' and 'view_order_details' in request.POST:
        # Customer/Employee has clicked on a button to view order details.
        orderid = request.POST['orderid']
        return view_order_details(request, orderid)
    if request.method == 'POST' and 'approve' in request.POST:
        # Employee has clicked on a button to approve this order.
        request_approve_orderid = request.POST['orderid']
        # Update Order table.
        order = Order.objects.get(orderid=request_approve_orderid)
        order.confirmed = 't'
        order.save()
        # Update Invoice table.
        customer_id = order.customerid.customerid
        customer = Customer.objects.get(customerid=customer_id)
        person_c = Person.objects.get(personid=customer.custpersonid.personid)
        # Get the current date and time.
        now = datetime.datetime.now()
        sql_date_obj = now.strftime('%Y-%m-%d %H:%M:%S')
        invoice = Invoice(customerid=customer, invoicedate=sql_date_obj, billingaddress=person_c.address, billingcity=person_c.city, billingstate=person_c.state, billingcountry=person_c.country, billingpostalcode=person_c.postalcode, total=order.price)
        invoice.save()
        print("Saved order confirm.")
        return HttpResponseRedirect('/dashboard/')
    person = None
    if request.user.is_authenticated():
        person = Person.objects.get(username=request.user.get_username())
    if person.affiliation == "Customer":
        # Customer dashboard.
        customer = Customer.objects.get(custpersonid=person.personid)
        filled_orders_query = "SELECT * FROM `Order` WHERE CustomerID = '" + str(customer.customerid) + "' AND Confirmed = 't'"
        filled_orders = Order.objects.raw(filled_orders_query)

        unfilled_orders_query = "SELECT * FROM `Order` WHERE CustomerID = '" + str(customer.customerid) + "' AND Confirmed = 'f'"
        unfilled_orders = Order.objects.raw(unfilled_orders_query)
        variables = RequestContext(request, {'person': person, 'user': request.user, 'filled_orders': filled_orders, 'unfilled_orders': unfilled_orders})
        return render_to_response('dashboard.html', variables,)
    if person.affiliation == "Employee" or person.affiliation == "Administrator":
        # Employee dashboard.
        unfilled_orders_query = "SELECT * FROM `Order` WHERE Confirmed = 'f'"
        unfilled_orders = Order.objects.raw(unfilled_orders_query)
        variables = RequestContext(request, {'person': person, 'user': request.user,  'unfilled_orders': unfilled_orders})
        return render_to_response('dashboard.html', variables,)

@login_required
def view_order_details(request, order_id):
    person = None
    if request.user.is_authenticated():
        person = Person.objects.get(username=request.user.get_username())
    order = Order.objects.get(orderid=order_id)
    if order.playlistmadby is None:
        # It's an order of tracks.
        order_tracks_query = "SELECT * FROM Track, `Order`, OrderTrack where `Order`.OrderID = OrderTrack.OrderId AND OrderTrack.OrderTrackId = Track.TrackId AND `Order`.OrderID = '" + order_id + "'"
        tracks = Track.objects.raw(order_tracks_query)
        variables = RequestContext(request, {'person': person, 'order': order, 'tracks': tracks})
        return render_to_response('orders/customer_view_order_details.html', variables,)        
    if order.playlistmadby == "Customer":
        # It's a customer-made playlist order.
        cust_playlist_query = "SELECT * FROM MyPlaylist, `Order`, OrderCustPlaylist where `Order`.OrderID = OrderCustPlaylist.OrderCustID AND OrderCustPlaylist.CustPlaylistID = MyPlaylist.MyPlaylistID AND `Order`.OrderID = '" + order_id + "'"
        playlists = MyPlaylist.objects.raw(cust_playlist_query)
        variables = RequestContext(request, {'person': person, 'order': order, 'playlists': playlists})
        return render_to_response('orders/customer_view_order_details.html', variables,)
    if order.playlistmadby == "Employee":
        # It's an employee-made playlist order.
        emp_playlist_query = "SELECT * FROM Playlist, `Order`, OrderEmpPlaylist where `Order`.OrderID = OrderEmpPlaylist.OrderEmpID AND OrderEmpPlaylist.EmpPlaylistID = Playlist.PlaylistId AND `Order`.OrderID = '" + order_id + "'"
        playlists = Playlist.objects.raw(emp_playlist_query)
        variables = RequestContext(request, {'person': person, 'order': order})
        return render_to_response('orders/customer_view_order_details.html', variables,)

@login_required
def view_cart(request):
    if request.method == 'POST':
        if 'remove_track' in request.POST:
            print("Clicked Remove Track")
            trackid = request.POST['trackid']
            return remove_track_from_cart(request, trackid)
        elif 'checkout' in request.POST:
            print("User clicked checkout.")
            return HttpResponseRedirect('/checkout/')
        elif 'remove_myplaylist' in request.POST: 
            print("Clicked Remove UPL")
            user_playlist_id = request.POST['myplaylistid']
            return remove_upl_from_cart(request, user_playlist_id)
        elif 'remove_playlist' in request.POST: 
            print("Clicked Remove EPL")
            employee_playlist_id = request.POST['playlistid']
            return remove_epl_from_cart(request, employee_playlist_id)
        return HttpResponseRedirect("/view_cart/")

    else:
        track_cart = request.session.get('track_cart', None)
        upl_cart = request.session.get('upl_cart', None)
        epl_cart = request.session.get('epl_cart', None)
        person = None
        if request.user.is_authenticated():
            person = Person.objects.get(username=request.user.get_username())
        variables = RequestContext(request, {'person': person, 'user': request.user, 'track_cart': track_cart, 'upl_cart': upl_cart, 'epl_cart': epl_cart})
        print("In view_cart, cart is: ")
        print(track_cart)
        return render_to_response('checkout/view_cart.html', variables,)

@login_required
def search(request):
    if request.method == 'POST' and 'track' in request.POST:
        # We have a received a search.
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
            
            query = "SELECT Track.TrackId, Track.Name, Artist.Name as artistname from Track, Album, Artist, Genre, MediaType where Track.AlbumId = Album.AlbumId and Album.ArtistId = Artist.ArtistId and Track.GenreId = Genre.GenreId and Track.MediaTypeId = MediaType.MediaTypeId and Track.Name like \"%%" + trackname + "%%\" and Album.Title like \"%%" + albumname + "%%\" and Artist.Name like \"%%" + artistname + "%%\" and Track.Composer like \"%%" + composername + "%%\" and Genre.Name like \"%%" + genrename + "%%\" and MediaType.Name like \"%%" + medianame + "%%\""

            result = Track.objects.raw(query)
            print("Found " + str(len(list(result))) + " results in search!")

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
    elif request.method == 'POST' and 'item' in request.POST:
        item_name = request.POST['item']
        print("You are trying to add the item " + item_name + " to the cart!")
        trackid = request.POST['trackid']
        return add_track_to_cart(request, trackid)
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
    track_obj = Track.objects.get(trackid=trackidnum)
    # Track data is a 3-tuple: (track ID, track Name, price)
    data = (trackidnum, track_obj.name, str(track_obj.unitprice))

    if track_cart:
        print("CART NOT EMPTY")
        track_cart.append(data)
    else:
        print("CART EMPTY")
        request.session['track_cart'] = list()
        track_cart = request.session.get('track_cart', None)
        track_cart.append(data)

    request.session.modified = True
    print("TRACK Cart contains:")
    print(track_cart)
    return HttpResponseRedirect("/view_cart/")


@login_required
def remove_track_from_cart(request, trackid):
    track_cart = request.session.get('track_cart', None)
    track_cart = [(tid, name, price) for tid, name, price in track_cart if tid != trackid] # hurrah for list comprehensions.
    request.session['track_cart'] = track_cart # set it back
    request.session.modified = True # save changes
    return HttpResponseRedirect("/view_cart/")

@login_required
def add_upl_to_cart(request, idnum):
    upl_cart = request.session.get('upl_cart', None)
    upl_obj = Myplaylist.objects.get(myplaylistid=idnum)
    tracks_query = "SELECT * FROM Track, MyPlaylist, MyPlaylistTracks WHERE MyPlaylistTracks.TrackID = Track.TrackId AND MyPlaylistTracks.MyPlaylistID = MyPlaylist.MyPlaylistID AND MyPlaylist.MyPlaylistId = '" + idnum + "'"
    tracks = Track.objects.raw(tracks_query)
    total_cost = 0
    for track in tracks:
        total_cost += track.unitprice
    total_cost = float('%.2f'%total_cost) # truncate to 2 decimal places
    data = (idnum, upl_obj.name, str(total_cost))
    if upl_cart:
        print("CART NOT EMPTY")
        upl_cart.append(data)
    else:
        print("CART EMPTY")
        request.session['upl_cart'] = list()
        upl_cart = request.session.get('upl_cart', None)
        upl_cart.append(data)
    request.session.modified = True
    print("UPL Cart contains:")
    print(upl_cart)
    return HttpResponseRedirect("/view_cart/")

@login_required
def remove_upl_from_cart(request, idnum):
    upl_cart = request.session.get('upl_cart', None)
    upl_cart = [(pid, name, price) for pid, name, price in upl_cart if pid != idnum]
    request.session['upl_cart'] = upl_cart
    request.session.modified = True
    return HttpResponseRedirect("/view_cart/")

@login_required
def remove_item_from_cart(request, idnum):
    if request.method=='POST' and 'remove_track' in request.POST:
        track_id = request.POST['trackid']
        return remove_track_from_cart(request, track_id)
    elif request.method=='POST' and 'remove_upl_from_cart' in request.POST: 
        user_playlist_id = request.POST['myplaylistid']
        return remove_upl_from_cart(request, user_playlist_id)
    elif request.method=='POST' and 'remove_epl_from_cart' in request.POST: 
        employee_playlist_id = request.POST['playlistid']
        return remove_epl_from_cart(request, employee_playlist_id)
    return HttpResponseRedirect("/view_cart/")

@login_required
def add_epl_to_cart(request, idnum):
    epl_cart = request.session.get('epl_cart', None)
    epl_obj = Playlist.objects.get(playlistid=idnum)
    tracks_query = "SELECT * FROM Track, Playlist, PlaylistTrack WHERE PlaylistTrack.TrackId = Track.TrackId AND PlaylistTrack.PlaylistId = Playlist.PlaylistId AND Playlist.PlaylistId = '" + idnum + "'"
    tracks = Track.objects.raw(tracks_query)
    total_cost = 0
    for track in tracks:
        total_cost += track.unitprice
    total_cost = float('%.2f'%total_cost) # truncate to 2 decimal places
    data = (idnum, epl_obj.name, str(total_cost))
    if epl_cart:
        print("CART NOT EMPTY")
        epl_cart.append(data)
    else:
        print("CART EMPTY")
        request.session['epl_cart'] = list()
        epl_cart = request.session.get('epl_cart', None)
        epl_cart.append(data)
    request.session.modified = True
    print("EPL Cart contains:")
    print(epl_cart)
    return HttpResponseRedirect("/view_cart/")

@login_required
def remove_epl_from_cart(request, idnum):
    epl_cart = request.session.get('epl_cart', None)
    epl_cart = [(pid, name, price) for pid, name, price in epl_cart if pid != idnum]
    request.session['epl_cart'] = epl_cart
    request.session.modified = True
    return HttpResponseRedirect("/view_cart/")    

@login_required
def search_playlists(request):
    if request.method == 'POST' and 'track' in request.POST:
        # We have a received a search.
        form = PlaylistSearchForm(request.POST)
        if form.is_valid():
            print("Search form is valid!")
            result = None
            playlistname = form.cleaned_data['name']
            trackname = form.cleaned_data['track']
            artistname = form.cleaned_data['artist']
            genrename = form.cleaned_data['genre']
            
            query = "SELECT Playlist.PlaylistId, Playlist.Name from Track, Album, Playlist, Artist, PlaylistTrack, Genre where Track.AlbumId = Album.AlbumId and Album.ArtistId = Artist.ArtistId and Track.GenreId = Genre.GenreId and Track.TrackId = PlaylistTrack.TrackId and Playlist.PlaylistId = PlaylistTrack.PlaylistId and Track.Name like \"%%" + trackname + "%%\" and Playlist.Name like \"%%" + playlistname + "%%\" and Artist.Name like \"%%" + artistname + "%%\" and Genre.Name like \"%%" + genrename + "%%\" group by Name"

            result = Playlist.objects.raw(query)
            person = None
            if request.user.is_authenticated():
                person = Person.objects.get(username=request.user.get_username())
            # make a new form for the next search
            form = PlaylistSearchForm()
            variables = RequestContext(request, {'result': result, 'person': person, 'form': form})
            return render_to_response('search/search_playlists.html', variables,)
        else:
            print("Search form fields not valid.")
            person = None
            if request.user.is_authenticated():
                person = Person.objects.get(username=request.user.get_username())
            variables = RequestContext(request, {'person': person})
            return render_to_response('/search/failure.html', variables,)
    elif request.method == 'POST' and 'add_playlist' in request.POST:
        playlist_name = request.POST['playlist']
        playlistid = request.POST['playlistid']
        return add_epl_to_cart(request, playlistid)
    elif request.method == 'POST' and 'view_playlist' in request.POST:
        request.session['eplplaylist'] = request.POST['playlistid']
        request.session.modified = True
        return HttpResponseRedirect("/playlist_details/")
    else:
        form = PlaylistSearchForm()
        person = None
        if request.user.is_authenticated():
            person = Person.objects.get(username=request.user.get_username())
        variables = RequestContext(request, {'form': form, 'person': person})
        return render_to_response('search/search_playlists.html', variables)


@login_required
def checkout(request):
    track_cart = request.session.get('track_cart', None)
    upl_cart = request.session.get('upl_cart', None)
    epl_cart = request.session.get('epl_cart', None)
    if request.method == 'POST':
        null_check = track_cart is None and upl_cart is None and epl_cart is None
        if null_check or (len(track_cart) == 0 and len(upl_cart) == 0 and len(epl_cart) == 0):
            # either null or empty shopping carts. can't check out.
            return HttpResponseRedirect('/checkout/failure/')
        if 'confirm' in request.POST:
            # user hit the confirmation button, so we clear the cart
            request.session['track_cart'] = list()
            request.session['upl_cart'] = list()
            request.session['epl_cart'] = list()
            request.session.modified = True
            # the old carts should still be in those 3 cart variables.
            return checkout_success(request, track_cart, upl_cart, epl_cart)

    total_price = 0
    if track_cart:
        # Calculate price.
        for item in track_cart:
            total_price += float(item[2][1:])
    if upl_cart:
        # Calculate price.
        for item in upl_cart:
            total_price += float(item[2][1:])
    if epl_cart:
        # Calculate price.
        for item in epl_cart:
            total_price += float(item[2][1:])

    total_price = float('%.2f'%total_price)
    person = None
    if request.user.is_authenticated():
        person = Person.objects.get(username=request.user.get_username())
    show_confirm_button = person.email != None and person.postalcode != None and person.city != None and person.country != None and (person.creditcardnumber != None or person.paypalemail != None or person.googlepayid != None or person.applepayid != None)
    variables = RequestContext(request, {'person': person, 'user': request.user, 'track_cart': track_cart, 'upl_cart': upl_cart, 'epl_cart': epl_cart, 'total_price': str(total_price), 'show_confirm_button': show_confirm_button})
    return render_to_response('checkout/checkout.html', variables,)

@login_required
def checkout_failure(request):
    person = None
    if request.user.is_authenticated():
        person = Person.objects.get(username=request.user.get_username())
    variables = RequestContext(request, {'person': person})
    return render_to_response('checkout/failure.html', variables,)

@login_required
def checkout_success(request, track_cart, upl_cart, epl_cart):
    person = None
    if request.user.is_authenticated():
        person = Person.objects.get(username=request.user.get_username())
    # customer = select * from Customer 
        # where Customer.PersonID = person.PersonID
    customer = Customer.objects.get(custpersonid=person.personid)

    # Total price of each respective order.
    total_track = 0
    total_upl = 0
    total_epl = 0

    # Get the current date and time.
    now = datetime.datetime.now()
    sql_date_obj = now.strftime('%Y-%m-%d')
    # Price is in the form "$2.99", so we will strip the first char, the $.
    # then convert it to float

    # Case 1: We have track items in the track cart to check out.
    if track_cart:
        # Calculate price.
        for item in track_cart:
            total_track += float(item[2][1:])
        total_track = float('%.2f'%(total_track))
        # Insert into Order.
        order = Order(customerid=customer, price=str(total_track), dateentered=sql_date_obj, confirmed='f')
        order.save()
        # Insert into OrderTrack (m:n relationship). 
        # Need to insert each track.
        for item in track_cart: # item: (trackid, trackname, trackprice)
            track_id = int(item[0])
            track_obj = Track.objects.get(trackid=track_id)
            ordertrack = Ordertrack(orderid=order, ordertrackid=track_obj)
            ordertrack.save()
    # Case 2: We have playlist items in user-made playlists to check out.
    if upl_cart:
        # Calculate price.
        for item in upl_cart:
            total_upl += float(item[2][1:])
        total_upl = float('%.2f'%(total_upl))
        # Insert into Order.
        order = Order(customerid=customer, playlistmadby="Customer",price=str(total_upl), dateentered=sql_date_obj, confirmed='f')
        order.save()
        # Insert into OrderCustPlaylist (m:n relationship).
        # Need to insert each playlist.
        for item in upl_cart: # item: (id, name, price)
            playlistid = int(item[0]) 
            ordercustplaylist = Ordercustplaylist(ordercustid=customer, custplaylistid=playlistid)
            ordercustplaylist.save()
    # Case 3: We have playlist items in employee-made playlists to check out.
    if epl_cart:
        # Calculate price.
        for item in epl_cart:
            total_epl += float(item[2][1:])
        total_epl = float('%.2f'%(total_epl))
        # Insert into Order.
        order = Order(customerid=customer.customerid, playlistmadby="Employee",price=str(total_upl), dateentered=sql_date_obj, confirmed='f')
        order.save()
        # Insert into OrderEmpPlaylist (m:n relationship).
        # Need to insert each playlist.
        for item in epl_cart: #item: (id, name, price)
            playlistid = int(item[0]) # I guess orderempid is really the customer id.... lolwut. bad naming.
            orderempplaylist = Orderempplaylist(orderempid=customer.customerid, empplaylistid=playlistid)
            orderempplaylist.save()

    variables = RequestContext(request, {'person': person})
    return render_to_response('checkout/success.html', variables,)

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
def sales_reporting(request):
    if request.method == 'POST' and 'view_order_details' in request.POST:
        return view_order_details(request, request.POST['orderid'])
    if request.method == 'POST' and 'search' in request.POST:
        # We have a received a search.
        form = SalesReportingForm(request.POST)
        if form.is_valid():
            print("Search form is valid!")
            orders_found = None
            month = form.cleaned_data['month']
            begin_date = form.cleaned_data['begin_date']
            end_date = form.cleaned_data['end_date']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            country = form.cleaned_data['country']
            firstname = form.cleaned_data['firstname']
            lastname = form.cleaned_data['lastname']
                
            orders_query = "SELECT * from Person, `Order`, Customer where Person.PersonID = Customer.CustPersonID and Customer.CustomerId = Order.CustomerID and Person.City like \"%%" + city + "%%\" and Person.State like \"%%" + state + "%%\" and Person.Country like \"%%" + country + "%%\" and Person.FirstName like \"%%" + firstname + "%%\" and Person.LastName like \"%%" + lastname + "%%\""
            
            if month != "":
                orders_query += " and `Order`.DateEntered like \"%%-" + month + "-%%\""
            if begin_date != "":
                orders_query +=  "and `Order`.DateEntered >= " + begin_date
            if end_date != "":
                orders_query += "and `Order`.DateEntered <= " + end_date

            orders_found = Order.objects.raw(orders_query)
            num_orders_found = str(len(list(orders_found)))
            print("Number of orders found: " + num_orders_found)

            tracks_query = "SELECT * from Person, `Order`, Customer, OrderTrack, Track where Person.PersonID = Customer.CustPersonID and Customer.CustomerId = `Order`.CustomerID and OrderTrack.OrderId = `Order`.OrderID and OrderTrack.OrderTrackId = Track.TrackId and Person.City like \"%%" + city + "%%\" and Person.State like \"%%" + state + "%%\" and Person.Country like \"%%" + country + "%%\" and Person.FirstName like \"%%" + firstname + "%%\" and Person.LastName like \"%%" + lastname + "%%\""

            if begin_date != "":
                tracks_query +=  "and `Order`.DateEntered >= " + begin_date
            if end_date != "":
                tracks_query += "and `Order`.DateEntered <= " + end_date

            tracks_found = Track.objects.raw(tracks_query)
            num_tracks_found = str(len(list(tracks_found)))
            print("Number of tracks found: " + num_tracks_found)

            total_price = 0
            for order in orders_found:
                total_price += float(order.price)
            total_price = str(total_price)

            person = None
            if request.user.is_authenticated():
                person = Person.objects.get(username=request.user.get_username())
            # make a new form for the next search
            form = SalesReportingForm()
            variables = RequestContext(request, {'person': person, 'form': form, 'orders_found': orders_found, 'num_orders_found': num_orders_found, 'tracks_found': tracks_found, 'num_tracks_found': num_tracks_found, 'total_price': total_price})
            return render_to_response('reporting/sales.html', variables,)
        else:
            print("Search form fields not valid.")
            person = None
            if request.user.is_authenticated():
                person = Person.objects.get(username=request.user.get_username())
            variables = RequestContext(request, {'person': person})
            return render_to_response('/search/failure.html', variables,)
    else:
        print("did i get here")
        form = SalesReportingForm()
        person = None
        if request.user.is_authenticated():
            person = Person.objects.get(username=request.user.get_username())
        variables = RequestContext(request, {'person': person, 'form':form})
        return render_to_response('reporting/sales.html', variables,)

@login_required
def inventory_reporting(request):
    if request.method == 'POST' and 'track' in request.POST:
        # We have a received a search.
        form = InventoryReportingForm(request.POST)
        if form.is_valid():
            print("Search form is valid!")
            tracks_found = None
            trackname = form.cleaned_data['track']
            albumname = form.cleaned_data['album']
            artistname = form.cleaned_data['artist']
            composername = form.cleaned_data['composer']
            genrename = form.cleaned_data['genre']
            medianame = form.cleaned_data['media']
            
            query = "SELECT Track.TrackId, Track.Name, Artist.Name as artistname from Track, Album, Artist, Genre, MediaType where Track.AlbumId = Album.AlbumId and Album.ArtistId = Artist.ArtistId and Track.GenreId = Genre.GenreId and Track.MediaTypeId = MediaType.MediaTypeId and Track.Name like \"%%" + trackname + "%%\" and Album.Title like \"%%" + albumname + "%%\" and Artist.Name like \"%%" + artistname + "%%\" and Track.Composer like \"%%" + composername + "%%\" and Genre.Name like \"%%" + genrename + "%%\" and MediaType.Name like \"%%" + medianame + "%%\""

            tracks_found = Track.objects.raw(query)
            num_tracks_found = str(len(list(tracks_found)))
            print("Found " + num_tracks_found + " results in search!")

            person = None
            if request.user.is_authenticated():
                person = Person.objects.get(username=request.user.get_username())
            # make a new form for the next search
            form = SearchForm()
            variables = RequestContext(request, {'tracks_found': tracks_found, 'person': person, 'form': form, 'num_tracks_found': num_tracks_found})
            return render_to_response('reporting/inventory.html', variables,)
        else:
            print("Search form fields not valid.")
            person = None
            if request.user.is_authenticated():
                person = Person.objects.get(username=request.user.get_username())
            variables = RequestContext(request, {'person': person})
            return render_to_response('reporting/inventory-failure.html', variables,)
    else:
        form = InventoryReportingForm()
        person = None
        if request.user.is_authenticated():
            person = Person.objects.get(username=request.user.get_username())
        variables = RequestContext(request, {'form': form, 'person': person})
        return render_to_response('reporting/inventory.html', variables)

@login_required
def demographics(request):
    customer_numbers = Person.objects.all().count()
    customer_country_numbers = Person.objects.values('country').distinct().count()
    if request.method == 'POST' and 'search' in request.POST:
        # We have a received a search.
        form = DemographicsForm(request.POST)
        if form.is_valid():
            print("Search form is valid!")
            result = None
            firstname = form.cleaned_data['firstname']
            lastname = form.cleaned_data['lastname']
            phonenum = form.cleaned_data['phone']
            email = form.cleaned_data['email']
            zipcode = form.cleaned_data['postalcode']
            address = form.cleaned_data['address']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            country = form.cleaned_data['country']
            fax = form.cleaned_data['fax']
            
            query = "SELECT * FROM Person WHERE Person.Affiliation='Customer' AND (Person.FirstName like \"%%" + firstname + "%%\" OR Person.FirstName is NULL) AND (Person.LastName like \"%%" + lastname + "%%\" OR Person.LastName is NULL) AND (Person.Phone like \"%%" + phonenum + "%%\" OR Person.Phone is NULL) AND (Person.Email like \"%%" + email + "%%\" OR Person.Email is NULL) AND (Person.PostalCode like \"%%" + zipcode + "%%\" OR Person.PostalCode is NULL) AND (Person.Address like \"%%" + address + "%%\" OR Person.Address is NULL) AND (Person.City like \"%%" + city + "%%\" OR Person.City is NULL) AND (Person.State like \"%%" + state + "%%\" OR Person.State is NULL) AND (Person.Country like \"%%" + country + "%%\" OR Person.Country is NULL) AND (Person.Fax like \"%%" + fax + "%%\" or Person.Fax is NULL)"

            result = Person.objects.raw(query)
            print("Found " + str(len(list(result))) + " results in search!")

            person = None
            if request.user.is_authenticated():
                person = Person.objects.get(username=request.user.get_username())
            # make a new form for the next search
            form = DemographicsForm()
            variables = RequestContext(request, {'result': result, 'person': person, 'form': form, 'customer_country_numbers': customer_country_numbers, 'customer_numbers': customer_numbers})
            return render_to_response('demographics/demographics.html', variables,)
        else:
            print("Search form fields not valid.")
            person = None
            if request.user.is_authenticated():
                person = Person.objects.get(username=request.user.get_username())
            variables = RequestContext(request, {'person': person, 'customer_country_numbers': customer_country_numbers, 'customer_numbers': customer_numbers})
            return render_to_response('/demographics/failure.html', variables,)
    else:
        print("GET request on demographics")
        form = DemographicsForm()
        person = None
        if request.user.is_authenticated():
            person = Person.objects.get(username=request.user.get_username())
        variables = RequestContext(request, {'form': form, 'person': person, 'customer_country_numbers': customer_country_numbers, 'customer_numbers': customer_numbers})
        return render_to_response('demographics/demographics.html', variables,)

@login_required
def add_tracks(request):
    if request.method == 'POST':
        form = AddTrack(request.POST)
        if form.is_valid():
            print("Form is valid!")

            # Get the information from the fields
            trackname  = form.cleaned_data['trackname']
            artistname = form.cleaned_data['artistname']
            albumname = form.cleaned_data['albumname']
            genrename = form.cleaned_data['genre']
            mediatype = form.cleaned_data['mediatype']
            composer = form.cleaned_data['composer']
            length = form.cleaned_data['length']
            size = form.cleaned_data['size']
            price = form.cleaned_data['price']
            album_id_object = None
            album_id = None
            track_exists_object = None
            track_exists = None
            genre_id = None
            genre_id_object = None
            mediatype_id = None
            mediatype_id_object = None
            # Get the information we need
            artist_id_object = Artist.objects.raw("SELECT * FROM Artist WHERE Name=%s", [artistname])
            if list(artist_id_object):
                artist_id = list(artist_id_object)[0].artistid
                album_id_object = Album.objects.raw("SELECT * FROM Album WHERE Title=%s AND ArtistId=%s", [albumname, artist_id])
                if list(album_id_object):
                    album_id = list(album_id_object)[0].albumid
            genre_id_object = Genre.objects.raw("SELECT * FROM Genre WHERE Name=%s", [genrename])
            if list(genre_id_object):
                genre_id = list(genre_id_object)[0].genreid
            mediatype_id_object = Mediatype.objects.raw("SELECT * FROM MediaType WHERE Name=%s", [mediatype])
            if list(mediatype_id_object):
                mediatype_id = list(mediatype_id_object)[0].mediatypeid

            # First, make sure that this track does not already exist. We treat a track with the same artist and album
            # This leaves open the possiblility for the same track name and artist on multiple albums, as you see with compilation albums or live albums
            if album_id != None:
                print("AlbumID != NONE!")
                track_exists = Track.objects.raw("SELECT TrackId FROM Track WHERE Name=%s AND AlbumId=%s", [trackname, album_id])

            #Handle the track existing
            if track_exists != None:
                print("Track already exists!")
                return add_tracks_exists(request)
            # Create relevant IDs, if they do not exist already
            else:
                if not list(artist_id_object):
                    newartist = Artist(name = artistname)
                    newartist.save()
                    artist_id = newartist.artistid
                if album_id is None:
                    artist_id_object = Artist.objects.raw("SELECT ArtistId FROM Artist WHERE Name=%s", [artistname])[0]
                    newalbum = Album(title = albumname, artistid = artist_id_object)
                    newalbum.save()
                    album_id = newalbum.albumid
                    album_id_object = Album.objects.raw("SELECT AlbumId FROM Album WHERE Title=%s AND ArtistId=%s", [albumname, artist_id])[0]
                if genre_id is None:
                    newgenre = Genre(name = genrename)
                    newgenre.save()
                    genre_id = newgenre.genreid
                    genre_id_object = Genre.objects.raw("SELECT GenreId FROM Genre WHERE Name=%s", [genrename])[0]
                if mediatype_id is None:
                    newmediatype = Mediatype(name = mediatype)
                    newmediatype.save()
                    mediatype_id_object = Mediatype.objects.raw("SELECT MediaTypeId FROM MediaType WHERE Name=%s", [mediatype])[0]
                # Finally, create the track
                newtrack = Track(
                    name=trackname,
                    albumid=album_id_object,
                    mediatypeid=mediatype_id_object,
                    genreid=genre_id_object,
                    composer=composer,
                    milliseconds=length,
                    bytes=size,
                    unitprice=price,
                )
                newtrack.save()

            print("Update was successful.")
            return add_tracks_success(request)
        else:
            print("Update was not valid.")
            return add_tracks_failure(request)
    else:
        form = AddTrack()
        person = None
        if request.user.is_authenticated():
            person = Person.objects.get(username=request.user.get_username())
        variables = RequestContext(request, {'form': form, 'person': person})
        return render_to_response('addtracks/add_tracks.html', variables)

@login_required
def add_tracks_failure(request):
    person = None
    if request.user.is_authenticated():
        person = Person.objects.get(username=request.user.get_username())
    variables = RequestContext(request, {'person': person})
    return render_to_response('addtracks/failure.html', variables,)

@login_required
def add_tracks_success(request):
    person = None
    if request.user.is_authenticated():
        person = Person.objects.get(username=request.user.get_username())
    variables = RequestContext(request, {'person': person})
    return render_to_response('addtracks/success.html', variables,)

@login_required
def add_tracks_exists(request):
    person = None
    if request.user.is_authenticated():
        person = Person.objects.get(username=request.user.get_username())
    variables = RequestContext(request, {'person': person})
    return render_to_response('addtracks/track_exists.html', variables,)

@login_required
def view_MyPlaylist(request):
    person = None
    form = MyPlaylistCreateForm(request.POST)
    if request.user.is_authenticated():
        person = Person.objects.get(username=request.user.get_username())
    print(person.personid)
    query = "SELECT * from Person, Customer, MyPlaylist where Person.PersonId = Customer.CustPersonID and Customer.CustomerId = MyPlaylist.CustomerID and Person.PersonId = " + str(person.personid)
    result = Myplaylist.objects.raw(query)
    # make a new form for the next search
    if request.method == 'POST' and 'myplaylist' in request.POST and 'add_myplaylist' in request.POST:# in request.POST and 'add_myplaylist'in request.POST:
        playlist_name = request.POST['myplaylist']
        playlistid = request.POST['myplaylistid']
        return add_upl_to_cart(request, playlistid)
    elif request.method == 'POST' and 'myplaylist' in request.POST and 'view_myplaylist' in request.POST:# in request.POST and 'add_myplaylist'in request.POST:
        request.session['userplaylist'] = request.POST['myplaylistid']
        request.session.modified = True
        return HttpResponseRedirect("/edit_MyPlaylist/")
    elif request.method == 'POST' and 'create_upl' in request.POST:
        if form.is_valid():
            if form.cleaned_data['name'] != '':
                getcustomer = Customer.objects.get(custpersonid = person.personid)
                myplaylist = Myplaylist(name = form.cleaned_data['name'], customerid = getcustomer)
                myplaylist.save()
                form= MyPlaylistCreateForm()
    variables = RequestContext(request, {'form':form, 'result': result, 'person': person})
    return render_to_response('MyPlaylist/view_MyPlaylist.html', variables,)

def edit_upl(request):
    trackresult = None
    myplaylistid = request.session.get('userplaylist', None)
    if myplaylistid != None:
        query1= "SELECT Track.TrackId, Track.Name, Artist.Name as artistname from Track, Album, Artist, MyPlaylistTracks where Track.AlbumId = Album.AlbumId and Album.ArtistId = Artist.ArtistId and Track.TrackId = MyPlaylistTracks.TrackID and MyPlaylistTracks.MyPlaylistID =" + myplaylistid
        trackresult = Track.objects.raw(query1)
        print("does this happen?")
    else:
        trackresult = None
    if request.method == 'POST' and 'search_track' in request.POST:
        # We have a received a search.
        print("now does this happen?")
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
            
            query2 = "SELECT Track.TrackId, Track.Name, Artist.Name as artistname from Track, Album, Artist, Genre, MediaType where Track.AlbumId = Album.AlbumId and Album.ArtistId = Artist.ArtistId and Track.GenreId = Genre.GenreId and Track.MediaTypeId = MediaType.MediaTypeId and Track.Name like \"%%" + trackname + "%%\" and Album.Title like \"%%" + albumname + "%%\" and Artist.Name like \"%%" + artistname + "%%\" and Track.Composer like \"%%" + composername + "%%\" and Genre.Name like \"%%" + genrename + "%%\" and MediaType.Name like \"%%" + medianame + "%%\""

            tracksearchresult = Track.objects.raw(query2)

            person = None
            if request.user.is_authenticated():
                person = Person.objects.get(username=request.user.get_username())
            # make a new form for the next search
            form = SearchForm()
            variables = RequestContext(request, {'tracksearchresult': tracksearchresult, 'person': person, 'form': form, 'trackresult':trackresult})
            return render_to_response('MyPlaylist/edit_MyPlaylist.html', variables,)
        else:
            print("Search form fields not valid.")
            person = None
            if request.user.is_authenticated():
                person = Person.objects.get(username=request.user.get_username())
            variables = RequestContext(request, {'person': person})
            return render_to_response('/search/failure.html', variables,)
    elif request.method == 'POST' and 'searchtrackname' in request.POST:
        track_name = request.POST['searchtrackname']
        print("You are trying to add the item " + track_name + " to the playlist!")
        trackid = request.POST['searchtrackid']
        return add_track_to_upl(request, trackid)
    elif request.method == 'POST' and 'remove_track_upl' in request.POST:
        print("deleting?")
        trackid = request.POST['playlisttrackid']
        print(str(trackid))
        print(str(myplaylistid))
        trackobjid = Track.objects.get(trackid=trackid)
        myplaylistobj = Myplaylist.objects.get(myplaylistid=myplaylistid)
        cursor = connection.cursor()
        cursor.execute("DELETE FROM MyPlaylistTracks WHERE MyPlaylistTracks.TrackId = %s and MyPlaylistTracks.MyPlaylistID =%s", [trackobjid.trackid, myplaylistobj.myplaylistid])
    print("i guess this happens")
    form = SearchForm()
    person = None
    if request.user.is_authenticated():
        person = Person.objects.get(username=request.user.get_username())
    variables = RequestContext(request, {'form': form, 'person': person, 'trackresult':trackresult})
    return render_to_response('MyPlaylist/edit_MyPlaylist.html', variables)


def add_track_to_upl(request, trackidnum):
    print("got into add")
    myplaylistid = request.session['userplaylist']
    print(str(myplaylistid))
    if myplaylistid != None:
        print("do i add?")
        uplobj = Myplaylist.objects.get(myplaylistid = myplaylistid)
        trackobj = Track.objects.get(trackid= trackidnum)
        newUPLTrack = Myplaylisttracks(myplaylistid = uplobj, trackid = trackobj)
        newUPLTrack.save()
    return HttpResponseRedirect("/edit_MyPlaylist/")

def edit_epl(request):
    trackresult = None
    playlistid = request.session.get('eplplaylist', None)
    if playlistid != None:
        query1= "SELECT Track.TrackId, Track.Name, Artist.Name as artistname from Track, Album, Artist, PlaylistTrack where Track.AlbumId = Album.AlbumId and Album.ArtistId = Artist.ArtistId and Track.TrackId = PlaylistTrack.TrackId and PlaylistTrack.PlaylistId =" + playlistid
        trackresult = Track.objects.raw(query1)
        print("does this happen?")
    else:
        trackresult = None
    if request.method == 'POST' and 'search_track' in request.POST:
        # We have a received a search.
        print("now does this happen?")
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
            
            query2 = "SELECT Track.TrackId, Track.Name, Artist.Name as artistname from Track, Album, Artist, Genre, MediaType where Track.AlbumId = Album.AlbumId and Album.ArtistId = Artist.ArtistId and Track.GenreId = Genre.GenreId and Track.MediaTypeId = MediaType.MediaTypeId and Track.Name like \"%%" + trackname + "%%\" and Album.Title like \"%%" + albumname + "%%\" and Artist.Name like \"%%" + artistname + "%%\" and Track.Composer like \"%%" + composername + "%%\" and Genre.Name like \"%%" + genrename + "%%\" and MediaType.Name like \"%%" + medianame + "%%\""

            tracksearchresult = Track.objects.raw(query2)

            person = None
            if request.user.is_authenticated():
                person = Person.objects.get(username=request.user.get_username())
            # make a new form for the next search
            form = SearchForm()
            variables = RequestContext(request, {'tracksearchresult': tracksearchresult, 'person': person, 'form': form, 'trackresult':trackresult})
            return render_to_response('search/playlist_details.html', variables,)
        else:
            print("Search form fields not valid.")
            person = None
            if request.user.is_authenticated():
                person = Person.objects.get(username=request.user.get_username())
            variables = RequestContext(request, {'person': person})
            return render_to_response('/search/failure.html', variables,)
    elif request.method == 'POST' and 'searchtrackname' in request.POST:
        track_name = request.POST['searchtrackname']
        print("You are trying to add the item " + track_name + " to the playlist!")
        trackid = request.POST['searchtrackid']
        return add_track_to_epl(request, trackid)
    elif request.method == 'POST' and 'remove_track_upl' in request.POST:
        print("deleting?")
        trackid = request.POST['playlisttrackid']
        trackobjid = Track.objects.get(trackid=trackid)
        playlistobj = Playlist.objects.get(playlistid=playlistid)
        cursor = connection.cursor()
        cursor.execute("DELETE FROM PlaylistTrack WHERE PlaylistTrack.TrackId = %s and PlaylistTrack.PlaylistId =%s", [trackobjid.trackid, playlistobj.playlistid])
    print("i guess this happens")
    form = SearchForm()
    person = None
    if request.user.is_authenticated():
        person = Person.objects.get(username=request.user.get_username())
    variables = RequestContext(request, {'form': form, 'person': person, 'trackresult':trackresult})
    return render_to_response('search/playlist_details.html', variables)


def add_track_to_epl(request, trackidnum):
    playlistid = request.session['eplplaylist']
    if playlistid != None:
        uplobj = Playlist.objects.get(playlistid = playlistid)
        trackobj = Track.objects.get(trackid= trackidnum)
        newEPLTrack = Playlisttrack(playlistid = uplobj, trackid = trackobj)
        newEPLTrack.save()
    return HttpResponseRedirect("/playlist_details/")


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
    if request.method == 'POST':
        if 'remove_track' in request.POST:
            # we're trying to remove something.
            print(request.POST)
            print("Clicked remove track.")
            trackid = request.POST['trackid']
            return remove_track_from_cart(request, trackid)
        elif 'checkout' in request.POST:
            print("User clicked checkout.")
            return HttpResponseRedirect('/checkout/')
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
    print("Added " + data[0] + " to cart, which costs $" + data[1] + "!")

    if track_cart:
        print("CART NOT EMPTY")
        track_cart.append(data)
    else:
        print("CART EMPTY")
        request.session['track_cart'] = list()
        track_cart = request.session.get('track_cart', None)
        track_cart.append(data)

    request.session.modified = True
    print("Cart contains:")
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
    data = (idnum, upl_obj.name, "Derp")
    print("Added " + data[0] + " to cart, which costs $" + data[1] + "!")

    if upl_cart:
        print("CART NOT EMPTY")
        upl_cart.append(data)
    else:
        print("CART EMPTY")
        request.session['upl_cart'] = list()
        upl_cart = request.session.get('upl_cart', None)
        upl_cart.append(data)

    request.session.modified = True
    print("Cart contains:")
    for item in upl_cart:
        print(item)
    return view_cart(request)

@login_required
def remove_item_from_cart(request, idnum):
    if request.method=='POST' and 'remove_upl_from_cart' in request.POST:
        track_cart = request.session.get('track_cart', None)
        if track_cart[trackid]:
            del track_cart[trackid]
        else:
            track_cart=track_cart
        request.session.modified = True
        return view_cart(request)
    elif request.method=='POST' and 'remove_upl_from_cart' in request.POST: 
        upl_cart = request.session.get('upl_cart', None)
        if upl_cart[idnum]:
            del upl_cart[idnum]
        request.session.modified = True
        return view_cart(request)
    elif request.method=='POST' and 'remove_epl_from_cart' in request.POST: 
        print("test")
    return view_cart(request)


@login_required
def remove_upl_from_cart(request, idnum):
    upl_cart = request.session.get('upl_cart', None)
    if upl_cart[idnum]:
        del upl_cart[idnum]
    return view_cart(request)

@login_required
def add_epl_to_cart(request, idnum):
    epl_cart = request.session.get('epl_cart', None)
    epl_obj = Playlist.objects.get(playlistid=idnum)
    data = (idnum, epl_obj.name, "$Derp Dollars")
    print("Added " + data[0] + " to cart, which costs $" + data[1] + "!")

    if epl_cart:
        print("CART NOT EMPTY")
        epl_cart.append(data)
    else:
        print("CART EMPTY")
        request.session['epl_cart'] = list()
        epl_cart = request.session.get('epl_cart', None)
        epl_cart.append(data)

    request.session.modified = True
    print("Cart contains:")
    for item in epl_cart:
        print(item)
    return view_cart(request)

@login_required
def remove_epl_from_cart(request, idnum):
    epl_cart = request.session.get('upl_cart', None)
    if epl_cart[idnum]:
        del epl_cart[idnum]
    return view_cart(request)

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
            for playlist in result:
                print(playlist.name)
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
    elif request.method == 'POST' and 'playlist' in request.POST:
        playlist_name = request.POST['playlist']
        print("You are trying to add the item " + playlist_name + " to the cart!")
        playlistid = request.POST['playlistid']
        return add_epl_to_cart(request, playlistid)
    else:
        form = PlaylistSearchForm()
        person = None
        if request.user.is_authenticated():
            person = Person.objects.get(username=request.user.get_username())
        variables = RequestContext(request, {'form': form, 'person': person})
        return render_to_response('search/search_playlists.html', variables)


@login_required
def checkout(request):
    if request.method == 'POST':
        track_cart = request.session.get('track_cart', None)
        upl_cart = request.session.get('upl_cart', None)
        epl_cart = request.session.get('epl_cart', None)
        if track_cart is None and upl_cart is None and epl_cart is None:
            return HttpResponseRedirect('/checkout/failure/')
        if 'confirm' in request.POST:
            # user hit the confirmation button, so we clear the cart
            request.session['track_cart'] = list()
            request.session['upl_cart'] = list()
            request.session['epl_cart'] = list()
            request.session.modified = True
            # the old carts should still be in those 3 cart variables.
            return checkout_success(request, track_cart, upl_cart, epl_cart)
        person = None
        if request.user.is_authenticated():
            person = Person.objects.get(username=request.user.get_username())
        variables = RequestContext(request, {'person': person})        
        return re('checkout/checkout/')
    else:
        return HttpResponseRedirect('/checkout/failure/')

@login_required
def checkout_failure(request):
    person = None
    if request.user.is_authenticated():
        person = Person.objects.get(username=request.user.get_username())
    variables = RequestContext(request, {'person': person})
    return render_to_response('checkout/failure.html', variables,)

@login_required
def checkout_success(request, track_cart, upl_cart, epl_cart):
    total = 0
    # Price is in the form "$2.99", so we will strip the first char, the $.
    # then convert it to int.
    for item in track_cart:
        total += int(item[2][1:])
    for item in upl_cart:
        total += int(item[2][1:])
    for item in epl_cart:
        total += int(item[2][1:])
    print("The total price of all the items is " + total)
    person = None
    if request.user.is_authenticated():
        person = Person.objects.get(username=request.user.get_username())
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
            album_id = None
            track_exists = None
            # Get the information we need
            artist_id = Artist.objects.raw("SELECT ArtistId FROM Artist WHERE Name=%s", [artistname])
            if list(artist_id):
                artist_id = list(artist_id)[0].artistid
                album_id = Album.objects.raw("SELECT AlbumId FROM Album WHERE Title=%s AND ArtistId=%s", [albumname, artist_id])
                album_id = list(album_id)[0].albumid
            genre_id = Genre.objects.raw("SELECT GenreId FROM Genre WHERE Name=%s", [genrename])
            genre_id = list(genre_id)[0].genreid
            mediatype_id = Mediatype.objects.raw("SELECT MediaTypeId FROM MediaType WHERE Name=%s", [mediatype])
            mediatype_id = list(mediatype_id)[0].mediatypeid

            # First, make sure that this track does not already exist. We treat a track with the same artist and album
            # This leaves open the possiblility for the same track name and artist on multiple albums, as you see with compilation albums or live albums
            if album_id != None:
                track_exists = Track.objects.raw("SELECT TrackId FROM Track WHERE Name=%s AND AlbumId=%s", [trackname, album_id])

            #Handle the track existing
            if track_exists != None:
                print("Track already exists!")
                return render_to_response('addtracks/track_exists.html')

            # Create relevant IDs, if they do not exist already
            else:
                if not list(artist_id):
                    newartist = Artist(name = artistname)
                    newartist.save()
                    artist_id = newartist.artistid
                if album_id is None:
                    newalbum = Album(title = albumname, artistid = artist_id)
                    newalbum.save()
                    album_id = newalbum.albumid
                if not list(genre_id):
                    newgenre = Genre(name = genrename)
                    newgenre.save()
                    genre_id = newgenre.genreid
                if not list(mediatype_id):
                    newmediatype = Mediatype(name = mediatype)
                    newmediatype.save()
                    mediatype_id = newmediatype.mediatypeid
                # Finally, create the track
                newtrack = Track(
                    name=trackname,
                    albumid=album_id,
                    mediatypeid=mediatype_id,
                    genreid=genre_id,
                    composer=composer,
                    milliseconds=length,
                    bytes=size,
                    unitprice=price,
                )
                newtrack.save()

            print("Update was successful.")
            return render_to_response('addtracks/success.html')
        else:
            print("Update was not valid.")
            person = None
            if request.user.is_authenticated():
                person = Person.objects.get(username=request.user.get_username())
            variables = RequestContext(request, {'person': person})
            return render_to_response('addtracks/failure.html', variables,)
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
        playlist_name = request.POST['myplaylist']
        playlistid = request.POST['myplaylistid']
        return edit_upl(request, playlistid)
    variables = RequestContext(request, {'form':form, 'result': result, 'person': person})
    return render_to_response('MyPlaylist/view_MyPlaylist.html', variables,)

def edit_upl(request, idnum):
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

            person = None
            if request.user.is_authenticated():
                person = Person.objects.get(username=request.user.get_username())
            # make a new form for the next search
            form = SearchForm()
            variables = RequestContext(request, {'result': result, 'person': person, 'form': form})
            return render_to_response('MyPlaylist/edit_MyPlaylist.html', variables,)
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
        return render_to_response('MyPlaylist/edit_MyPlaylist.html', variables)


def edit_epl(request, idnum):
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


"""
@login_required
def edit_MyPlaylist(request, myplaylistid):

@login_required
def edit_Playlist(request):
"""

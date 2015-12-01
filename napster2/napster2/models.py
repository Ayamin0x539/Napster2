# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin sqlcustom [app_label]'
# into your database.
from __future__ import unicode_literals

from django.db import models


class Album(models.Model):
    albumid = models.IntegerField(db_column='AlbumId', primary_key=True)  # Field name made lowercase.
    title = models.CharField(db_column='Title', max_length=160)  # Field name made lowercase.
    artistid = models.ForeignKey('Artist', db_column='ArtistId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Album'


class Applepay(models.Model):
    appleinvoiceid = models.OneToOneField('Invoice', db_column='AppleInvoiceID', primary_key=True)  # Field name made lowercase.
    appleid = models.CharField(db_column='AppleID', max_length=60, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ApplePay'


class Artist(models.Model):
    artistid = models.IntegerField(db_column='ArtistId', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=120, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Artist'


class Clips(models.Model):
    clipstrackid = models.OneToOneField('Track', db_column='ClipsTrackId', primary_key=True)  # Field name made lowercase.
    itunesurl = models.CharField(db_column='ItunesURL', max_length=205, blank=True, null=True)  # Field name made lowercase.
    googleurl = models.CharField(db_column='GoogleURL', max_length=205, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Clips'


class Creditcard(models.Model):
    ccinvoiceid = models.OneToOneField('Invoice', db_column='CCInvoiceID', primary_key=True)  # Field name made lowercase.
    ccnum = models.CharField(db_column='CCNum', max_length=60, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CreditCard'


class Customer(models.Model):
    customerid = models.IntegerField(db_column='CustomerId', primary_key=True)  # Field name made lowercase.
    supportrepid = models.ForeignKey('Employee', db_column='SupportRepId', blank=True, null=True)  # Field name made lowercase.
    custpersonid = models.ForeignKey('Person', db_column='CustPersonID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Customer'


class Employee(models.Model):
    employeeid = models.IntegerField(db_column='EmployeeId', primary_key=True)  # Field name made lowercase.
    title = models.CharField(db_column='Title', max_length=30, blank=True, null=True)  # Field name made lowercase.
    reportsto = models.ForeignKey('self', db_column='ReportsTo', blank=True, null=True)  # Field name made lowercase.
    birthdate = models.DateTimeField(db_column='BirthDate', blank=True, null=True)  # Field name made lowercase.
    hiredate = models.DateTimeField(db_column='HireDate', blank=True, null=True)  # Field name made lowercase.
    personid = models.IntegerField(db_column='PersonID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Employee'


class Genre(models.Model):
    genreid = models.IntegerField(db_column='GenreId', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=120, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Genre'


class Google(models.Model):
    googleinvoiceid = models.OneToOneField('Invoice', db_column='GoogleInvoiceID', primary_key=True)  # Field name made lowercase.
    googleid = models.CharField(db_column='GoogleID', max_length=60, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Google'


class Invoice(models.Model):
    invoiceid = models.IntegerField(db_column='InvoiceId', primary_key=True)  # Field name made lowercase.
    customerid = models.ForeignKey(Customer, db_column='CustomerId')  # Field name made lowercase.
    invoicedate = models.DateTimeField(db_column='InvoiceDate')  # Field name made lowercase.
    billingaddress = models.CharField(db_column='BillingAddress', max_length=70, blank=True, null=True)  # Field name made lowercase.
    billingcity = models.CharField(db_column='BillingCity', max_length=40, blank=True, null=True)  # Field name made lowercase.
    billingstate = models.CharField(db_column='BillingState', max_length=40, blank=True, null=True)  # Field name made lowercase.
    billingcountry = models.CharField(db_column='BillingCountry', max_length=40, blank=True, null=True)  # Field name made lowercase.
    billingpostalcode = models.CharField(db_column='BillingPostalCode', max_length=10, blank=True, null=True)  # Field name made lowercase.
    total = models.DecimalField(db_column='Total', max_digits=10, decimal_places=2)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Invoice'


class Invoiceline(models.Model):
    invoicelineid = models.IntegerField(db_column='InvoiceLineId', primary_key=True)  # Field name made lowercase.
    invoiceid = models.ForeignKey(Invoice, db_column='InvoiceId')  # Field name made lowercase.
    trackid = models.ForeignKey('Track', db_column='TrackId')  # Field name made lowercase.
    unitprice = models.DecimalField(db_column='UnitPrice', max_digits=10, decimal_places=2)  # Field name made lowercase.
    quantity = models.IntegerField(db_column='Quantity')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'InvoiceLine'


class Mediatype(models.Model):
    mediatypeid = models.IntegerField(db_column='MediaTypeId', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=120, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'MediaType'


class Myplaylist(models.Model):
    myplaylistid = models.IntegerField(db_column='MyPlaylistID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=45)  # Field name made lowercase.
    customerid = models.ForeignKey(Customer, db_column='CustomerID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'MyPlaylist'


class Myplaylisttracks(models.Model):
    myplaylistid = models.ForeignKey(Myplaylist, db_column='MyPlaylistID')  # Field name made lowercase.
    trackid = models.ForeignKey('Track', db_column='TrackID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'MyPlaylistTracks'
        unique_together = (('myplaylistid', 'trackid'),)


class Order(models.Model):
    orderid = models.IntegerField(db_column='OrderID', primary_key=True)  # Field name made lowercase.
    customerid = models.ForeignKey(Customer, db_column='CustomerID')  # Field name made lowercase.
    playlistmadby = models.CharField(db_column='PlaylistMadBy', max_length=45, blank=True, null=True)  # Field name made lowercase.
    price = models.CharField(db_column='Price', max_length=45, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Order'


class Ordercustplaylist(models.Model):
    ordercustid = models.ForeignKey(Order, db_column='OrderCustID')  # Field name made lowercase.
    custplaylistid = models.ForeignKey(Myplaylist, db_column='CustPlaylistID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'OrderCustPlaylist'
        unique_together = (('ordercustid', 'custplaylistid'),)


class Orderempplaylist(models.Model):
    orderempid = models.ForeignKey(Order, db_column='OrderEmpID')  # Field name made lowercase.
    empplaylistid = models.ForeignKey('Playlist', db_column='EmpPlaylistID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'OrderEmpPlaylist'
        unique_together = (('orderempid', 'empplaylistid'),)


class Payment(models.Model):
    paymentid = models.IntegerField(db_column='PaymentID', primary_key=True)  # Field name made lowercase.
    type = models.CharField(db_column='Type', max_length=45, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Payment'


class Paypal(models.Model):
    paypalinvoiceid = models.OneToOneField(Invoice, db_column='PaypalInvoiceID', primary_key=True)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=60, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Paypal'


class Person(models.Model):
    personid = models.AutoField(db_column='PersonID', primary_key=True)  # Field name made lowercase.
    username = models.CharField(db_column='Username', max_length=30, blank=True, null=True) # This is technically also a primary key... shhhh...
    group = models.CharField(db_column='Group', max_length=15, blank=True, null=True) # Customer, Employee, Administrator (also Employee)
    lastname = models.CharField(db_column='LastName', max_length=20, blank=True, null=True)  # Field name made lowercase.
    firstname = models.CharField(db_column='FirstName', max_length=40, blank=True, null=True)  # Field name made lowercase.
    postalcode = models.CharField(db_column='PostalCode', max_length=10, blank=True, null=True)  # Field name made lowercase.
    address = models.CharField(db_column='Address', max_length=70, blank=True, null=True)  # Field name made lowercase.
    city = models.CharField(db_column='City', max_length=40, blank=True, null=True)  # Field name made lowercase.
    state = models.CharField(db_column='State', max_length=40, blank=True, null=True)  # Field name made lowercase.
    country = models.CharField(db_column='Country', max_length=45, blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=60, blank=True, null=True)  # Field name made lowercase.
    fax = models.CharField(db_column='Fax', max_length=45, blank=True, null=True)  # Field name made lowercase.
    phone = models.CharField(db_column='Phone', max_length=60, blank=True, null=True)  # Field name made lowercase.
    creditcardnumber = models.CharField(db_column='CreditCardNumber', max_length=16, blank=True, null=True)
    googlepayid = models.CharField(db_column='GooglepayID', max_length=30, blank=True, null=True)
    applepayid = models.CharField(db_column='ApplepayID', max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Person'

class Playlist(models.Model):
    playlistid = models.IntegerField(db_column='PlaylistId', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=120, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Playlist'


class Playlisttrack(models.Model):
    playlistid = models.ForeignKey(Playlist, db_column='PlaylistId')  # Field name made lowercase.
    trackid = models.ForeignKey('Track', db_column='TrackId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PlaylistTrack'
        unique_together = (('playlistid', 'trackid'),)


class Track(models.Model):
    trackid = models.IntegerField(db_column='TrackId', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=200)  # Field name made lowercase.
    albumid = models.ForeignKey(Album, db_column='AlbumId', blank=True, null=True)  # Field name made lowercase.
    mediatypeid = models.ForeignKey(Mediatype, db_column='MediaTypeId')  # Field name made lowercase.
    genreid = models.ForeignKey(Genre, db_column='GenreId', blank=True, null=True)  # Field name made lowercase.
    composer = models.CharField(db_column='Composer', max_length=220, blank=True, null=True)  # Field name made lowercase.
    milliseconds = models.IntegerField(db_column='Milliseconds')  # Field name made lowercase.
    bytes = models.IntegerField(db_column='Bytes', blank=True, null=True)  # Field name made lowercase.
    unitprice = models.DecimalField(db_column='UnitPrice', max_digits=10, decimal_places=2)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Track'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group_id = models.ForeignKey(AuthGroup)
    permission_id = models.ForeignKey('AuthPermission')

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group_id', 'permission_id'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type_id = models.ForeignKey('DjangoContentType')
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type_id', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user_id = models.ForeignKey(AuthUser)
    group_id = models.ForeignKey(AuthGroup)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user_id', 'group_id'),)


class AuthUserUserPermissions(models.Model):
    user_id = models.ForeignKey(AuthUser)
    permission_id = models.ForeignKey(AuthPermission)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user_id', 'permission_id'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', blank=True, null=True)
    user = models.ForeignKey(AuthUser)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'

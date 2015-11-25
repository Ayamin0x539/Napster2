from django.db import models

class Album(models.Model):
	AlbumId = models.IntegerField(primary_key=true)
	Title = models.CharField(max_length=160)
	ArtistId= models.ForeignKey('Artist')

class ApplePay(models.Model):
	AppleInvoiceID = models.ForeignKey('Invoice',primary_key=true) 
	AppleID = models.CharField(max_length=60)

class Artist(models.Model)
	ArtistId = models.IntegerField(primary_key=true) 
	Name = models.CharField(max_length=120)

class Clips(models.Model)
	ClipsTrackId = models.ForeignKey('Track',primary_key=true)
	ItunesURL = models.CharField(max_length=205)
	GoogleURl = models.CharField(max_length=205)

class CreditCard(models.Model)
	CCInvoiceID = models.ForeignKey('Invoice',primary_key=true)
	CCNum = models.CharField(max_length=60)

class Customer(models.Model)
	CustomerId = models.IntegerField(primary_key=true)
	SupportRepId = models.ForeignKey('Employee')
	CustPersonID = models.ForeignKey('Person')

class Employee(models.Model)
	EmployeeId = models.IntegerField(primary_key=true)
	Title = models.CharField(max_length=30)
	ReportsTo = models.ForeignKey('Employee')
	BirthDate = models.DateField()
	HireDate = models.DateField()
	PersonID = models.ForeignKey('Person')

class Genre(models.Model)
	GenreId = models.IntegerField(primary_key=true)
	Name = models.CharField(max_length=120)

class Google(models.Model)
	GoogleInvoiceID = models.ForeignKey('Invoice', primary_key=true)
	GoogleID = models.CharField(max_length=60)

class Invoice(models.Model)
	InvoiceId = models.IntegerField(primary_key=true)
	CustomerId = models.ForeignKey('Customer')
	InvoiceDate = models.DateField()
	BillingAddress = models.CharField(max_length=70)
	BillingCity = models.CharField(max_length=40)
	Billing State = models.CharField(max_length=40)#could be a dropdown
	BillingCountry = models.CharField(max_length=40)#could also be a dropdown
	BillingPostalCode = models.CharField(max_length=10)
	Total = models.DecimalField(max_digits=100, decimal_places=2)

class InvoiceLine(models.Model)
	InvoiceLineId = models.IntegerField(primary_key=true)
	InvoiceId = models.ForeignKey('Invoice')
	TrackId = models('Track')
	UnitPrice = models.DecimalField(max_digits=10, decimal_places=2)
	Quantity = models.IntegerField()

class MediaType(models.Model)
	MediaTypeId = models.IntegerField(primary_key=true)
	Name = models.CharField(max_length=120)

class MyPlaylist(models.Model)
	MyPlaylistID = models.IntegerField(primary_key=true)
	Name = models.CharField(max_length=120)
	CustomerId = models.ForeignKey('Customer')

class MyPlaylistTracks(models.Model)
	MyPlaylistID = models.ForeignKey('MyPlaylist')
	TrackID = models.ForeignKey('Track')

class Order(models.Model)
	OrderID = models.IntegerField(primary_key=true)
	CustomerID = models.ForeignKey('Customer')
	PlaylistMadBy = models.CharField(max_length=45)
	Price = models.CharField(max_length=45)#should probably be a decimal, may have to propogate change in DB

class OrderCustPlaylist(models.Model)
	OrderCustID = models.ForeignKey('Order')
	CustPlaylistID = models.ForeignKey('MyPlaylist')

class OrderEmpPlaylist(models.Model)
	OrderEmpID = models.ForeignKey('Order')
	EmpPlaylistID = models.ForeignKey('Playlist')

class Payment(models.Model)
	PaymentID = models.IntegerField(primary_key=true)
	Type = models.CharField(max_length=45)#should probably be an enumerated value

class Paypal(models.Model)
	PaypalInvoiceID = models.ForeignKey('Invoice')
	Email = models.CharField(max_length=60)

class Person(models.Model)
	PersonID = models.IntegerField(primary_key=true)
	LastName = models.CharField(max_length=20)
	FirstName = models.CharField(max_length=40)
	PostalCode = models.CharField(max_length=10)
	Address = models.CharField(max_length=70)
	City = models.CharField(max_length=40)
	State = models.CharField(max_length=45)
	Country = models.CharField(max_length=45)
	Email = models.CharField(max_length=60)
	Fax = models.CharField(max_length=45)
	Phone = models.CharField(max_length=60)

class Playlist(models.Model)
	PlaylistID = models.IntegerField(primary_key=true)
	Name = models.CharField(max_length=120)

class PlaylistTrack(models.Model)
	PlaylistID = models.ForeignKey('Playlist')
	TrackID = models.ForeignKey('Track')

class Track(models.Model)
	TrackID = models.IntegerField(primary_key=true)
	Name = models.CharField(max_length=200)
	AlbumId = models.ForeignKey('Album')	
	MediaTypeId = models.ForeignKey('MediaType')
	GenreId = models.ForeignKey('Genre')
	Composer = models.CharField(max_length=220)
	Miliseconds = models.IntegerField()
	Bytes = models.IntegerField()
	UnitPrice = models.DecimalField(max_digits=10, decimal_places=2)
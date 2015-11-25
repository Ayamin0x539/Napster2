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
	CustPersonID = models.IntegerField() #seems like a foreign key, should probably check

class Employee(models.Model)
	EmployeeId = models.IntegerField(primary_key=true)
	Title = models.CharField(max_length=30)
	ReportsTo = models.ForeignKey('Employee')
	BirthDate = models.DateField()
	HireDate = models.DateField()

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
	Billing State = models.CharField(max_length=40) #could be a dropdown
	BillingCountry = models.C
from django.db import models

class Album(models.Model):
	AlbumId = models.IntegerField(primary_key=true)
	Title = models.CharField(max_length=160)
	ArtistId= models.ForeignKey('Artist')

class ApplePay(models.Model):
	AppleInvoiceID = models.ForeignKey('Invoice') #probably a forgein key
	AppleID = models.CharField(max_length=60)

class Artist(models.Model)
	ArtistId = models.IntegerField(primary_key=true) 
	Name = models.CharField(max_length=120)

class Clips(models.Model)
	ClipsTrackId = models.ForeignKey('Track')
	ItunesURL = models.CharField(max_length=205)
	GoogleURl = models.CharField(max_length=205)

class CreditCard
	CCInvoiceID = models.IntegerField	

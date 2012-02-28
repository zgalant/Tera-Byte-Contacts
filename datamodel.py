from google.appengine.ext import db
from google.appengine.api import users

class Week(db.Model):
	year = db.StringProperty(multiline = False)
	week = db.StringProperty(multiline = False)
	
class Tag(db.Model):
	tag = db.StringProperty(multiline = False)

	
class Contact(db.Model):
	firstName = db.StringProperty(multiline = False)
	lastName = db.StringProperty(multiline = False)
	email = db.StringProperty(multiline = False)
	cellPhone = db.StringProperty(multiline = False)
	homePhone = db.StringProperty(multiline = False)
	school = db.StringProperty(multiline = False)
	contactType = db.StringProperty(multiline = False) # CAMPER | PARENT | COUNSELOR
	relations = db.ListProperty(db.Key) # list of Contact
	weeks = db.ListProperty(db.Key) # list of Week
	picture = db.BlobProperty()
	address = db.StringProperty(multiline = True)
	tags = db.ListProperty(db.Key) # list of Tag
	notes = db.StringProperty(multiline = True)

	

import cgi

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

import os
from google.appengine.ext.webapp import template

import datamodel

def footer(klass):
	template_values = {
	}

	path = os.path.join(os.path.dirname(__file__), 'HTML/footer.html')
	klass.response.out.write(template.render(path, template_values))	
	
def header(klass):
	if users.get_current_user():
		login_url = users.create_logout_url(klass.request.uri)
		login_url_text = 'Logout'
	else:
		login_url = users.create_login_url(klass.request.uri)
		login_url_text = 'Login'

	user = users.get_current_user()

	template_values = {
		'login_url':login_url,
		'login_url_text':login_url_text,
		'user':user
	}

	path = os.path.join(os.path.dirname(__file__), 'HTML/header.html')
	klass.response.out.write(template.render(path, template_values))

def contact(klass, contact):
	weeks = []
	for wid in contact.weeks:
		week = datamodel.Week.get_by_id(wid.id())
		weeks.append(week)
	
	if contact.address == None: # if the address wasn't entered, make it the default value
		contact.address = ''
	if contact.notes == None: # if the address wasn't entered, make it the default value
		contact.notes = ''
	
	template_values = {
		'contact':contact,
		'weeks':weeks
	}

	path = os.path.join(os.path.dirname(__file__), 'HTML/contact.html')
	klass.response.out.write(template.render(path, template_values))
	
	
def editContact(klass, contact):
	template_values = {
		'contact':contact
	}

	path = os.path.join(os.path.dirname(__file__), 'HTML/editContact.html')
	klass.response.out.write(template.render(path, template_values))

def listing(klass, contact):
	template_values = {
		'contact':contact
	}

	path = os.path.join(os.path.dirname(__file__), 'HTML/listing.html')
	klass.response.out.write(template.render(path, template_values))
	
	
def weekFilter(klass):
	weeks = datamodel.Week.all().order('-year')
	template_values = {	
		'weeks':weeks
	}
	path = os.path.join(os.path.dirname(__file__), 'HTML/weekFilter.html')
	klass.response.out.write(template.render(path, template_values))
	
def form(klass):
	#if users.get_current_user():
		weeks = datamodel.Week.all().order('-year')
		contacts = datamodel.Contact.all().order('lastName')
		template_values = {
			'weeks':weeks,
			'contacts':contacts
		}

		path = os.path.join(os.path.dirname(__file__), 'HTML/form.html')
		klass.response.out.write(template.render(path, template_values))
	#else:
	#	klass.response.out.write('<div class = "story">Please Log In.</div>')
	
def weekForm(klass):
	#if users.get_current_user():
		template_values = {
		}

		path = os.path.join(os.path.dirname(__file__), 'HTML/weekForm.html')
		klass.response.out.write(template.render(path, template_values))
	#else:
	#	klass.response.out.write('<div class = "story">Please Log In.</div>')
	
def addRelation(klass, contact):
	#if users.get_current_user():
		contacts = datamodel.Contact.all().order('lastName')
		weeks = datamodel.Week.all().order('-year')
		template_values = {
			'contact':contact,
			'contacts':contacts,
			'weeks':weeks
		}

		path = os.path.join(os.path.dirname(__file__), 'HTML/addRelation.html')
		klass.response.out.write(template.render(path, template_values))
	#else:
	#	klass.response.out.write('<div class = "story">Please Log In.</div>')


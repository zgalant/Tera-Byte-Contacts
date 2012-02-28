import cgi

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

import os
from google.appengine.ext.webapp import template

import datamodel
import html

import string
import math

class AddContact(webapp.RequestHandler):
	def post(self):
		contact = datamodel.Contact()
		contact.firstName = cgi.escape(self.request.get('firstName'))
		contact.lastName = cgi.escape(self.request.get('lastName'))
		contact.email = cgi.escape(self.request.get('email'))
		contact.cellPhone = cgi.escape(self.request.get('cellPhone'))
		contact.homePhone = cgi.escape(self.request.get('homePhone'))
		contact.school = cgi.escape(self.request.get('school'))
		contact.contactType = cgi.escape(self.request.get('contactType'))
		contact.address = cgi.escape(self.request.get('address'))
		contact.notes = cgi.escape(self.request.get('notes'))
		widString = self.request.get('week')
		relString = self.request.get('relation')
		if widString != '':
			wid = int(float(widString))
			week = datamodel.Week.get_by_id(wid)
			contact.weeks.append(week.key())
		if relString != '':
			rel = int(float(relString))
			relation = datamodel.Contact.get_by_id(rel)
			for r in relation.relations:
				contact.relations.append(r)
				contact.put()
				rContact = datamodel.Contact.get_by_id(r.id())
				rContact.relations.append(contact.key())
				rContact.put()
			contact.relations.append(relation.key())
			contact.put()
			relation.relations.append(contact.key())
			relation.put()
			
		contact.put()
		self.redirect('/')
		
class EditContact(webapp.RequestHandler):
	def post(self):
		cid = int(float(self.request.get('contact')))
		contact = datamodel.Contact.get_by_id(cid)
		
		contact.firstName = cgi.escape(self.request.get('firstName'))
		contact.lastName = cgi.escape(self.request.get('lastName'))
		contact.email = cgi.escape(self.request.get('email'))
		contact.cellPhone = cgi.escape(self.request.get('cellPhone'))
		contact.homePhone = cgi.escape(self.request.get('homePhone'))
		contact.school = cgi.escape(self.request.get('school'))
		contact.contactType = cgi.escape(self.request.get('contactType'))
		contact.address = cgi.escape(self.request.get('address'))
		contact.notes = cgi.escape(self.request.get('notes'))
		contact.put()
		self.redirect('/contact/' + self.request.get('contact'))

class AddForm(webapp.RequestHandler):
	def get(self):
		html.header(self)
		html.form(self)
		html.footer(self)
		
class ContactView(webapp.RequestHandler):
	def get(self):
		html.header(self)
		id = int(float(string.lstrip(self.request.path, 'contact/')))
		contact = datamodel.Contact.get_by_id(id)
		html.contact(self, contact)
		html.addRelation(self, contact)
		
		self.response.out.write('<br/><div class="header">Relations</div>')
		for rel in contact.relations:
			r = datamodel.Contact.get_by_id(rel.id())
			html.contact(self, r)
		
		
		html.footer(self)
		
class EditContactView(webapp.RequestHandler):
	def get(self):
		html.header(self)
		cid = int(float(string.lstrip(self.request.path, 'edit/contact/')))
		contact = datamodel.Contact.get_by_id(cid)
		html.editContact(self, contact)
		html.footer(self)

class ViewAll(webapp.RequestHandler):
	def get(self):
		html.header(self)
		self.response.out.write('<form action = "/add" method = "get"><input type = "submit" value = "Add Contact" class = "submit"></input></form>')
		self.response.out.write('<form action = "/addWeek" method = "get"><input type = "submit" value = "Add Week" class = "submit"></input></form>')
		self.response.out.write('<form action = "/mailingList" method = "get"><input type = "submit" value = "Mailing List" class = "submit"></input></form><br/>')
		self.response.out.write('<form action = "/search" method = "post"><input type="text" name="search" rows="1" class = "post-form-textarea"></input><br/><input type = "submit" value = "Search" class = "submit"></input></form><br/>')
		html.weekFilter(self)
		contacts = datamodel.Contact.all().order('lastName')		
		for contact in contacts:
			html.listing(self, contact)
		html.footer(self)
		
class FilterByWeek(webapp.RequestHandler):
	def post(self):
		html.header(self)
		wid = cgi.escape(self.request.get('week'))
		if wid != '-1':
			self.redirect('/week/' + wid)
		else:
			self.redirect('/')
		
		
class ViewWeek(webapp.RequestHandler):
	def get(self):
		html.header(self)
		wid = int(float(string.lstrip(self.request.path, 'week/')))
		week = datamodel.Week.get_by_id(wid)
		self.response.out.write('<form action = "/add" method = "get"><input type = "submit" value = "Add Contact" class = "submit"></input></form>')
		self.response.out.write('<form action = "/addWeek" method = "get"><input type = "submit" value = "Add Week" class = "submit"></input></form>')
		self.response.out.write('<form action = "/mailingList" method = "get"><input type="hidden" name="week" value="' + str(wid) + '"></input><input type = "submit" value = "Mailing List" class = "submit"></input></form><br/>')
		self.response.out.write('<form action = "/search" method = "post"><input type="text" name="search" rows="1" class = "post-form-textarea"></input><br/><input type = "submit" value = "Search" class = "submit"></input></form><br/>')
		html.weekFilter(self)
		contacts = datamodel.Contact.all()
		contacts.filter('weeks = ', week.key())
		for contact in contacts:
			html.listing(self, contact)
		html.footer(self)
		
		
class Search(webapp.RequestHandler):
	def post(self):
		html.header(self)
		self.response.out.write('<form action = "/add" method = "get"><input type = "submit" value = "Add Contact" class = "submit"></input></form>')
		self.response.out.write('<form action = "/addWeek" method = "get"><input type = "submit" value = "Add Week" class = "submit"></input></form>')
		self.response.out.write('<form action = "/mailingList" method = "get"><input type = "submit" value = "Mailing List" class = "submit"></input></form><br/>')
		self.response.out.write('<form action = "/search" method = "post"><input type="text" name="search" rows="1" class = "post-form-textarea"></input><br/><input type = "submit" value = "Search" class = "submit"></input></form><br/>')
		html.weekFilter(self)
		search_query = cgi.escape(self.request.get('search'))
		name_query = search_query.title()
		contacts = datamodel.Contact.all()
		contacts.filter('firstName = ', name_query)
		for contact in contacts:
			html.listing(self, contact)
		
		contacts = datamodel.Contact.all()
		contacts.filter('lastName = ', name_query)
		for contact in contacts:
			html.listing(self, contact)
			
		contacts = datamodel.Contact.all()
		contacts.filter('email = ', search_query)
		for contact in contacts:
			html.listing(self, contact)
		html.footer(self)

class AddWeek(webapp.RequestHandler):
	def get(self):
		html.header(self)
		html.weekForm(self)
		html.footer(self)
		
class AddWeekAction(webapp.RequestHandler):
	def post(self):		
		week = datamodel.Week()	
		week.year = cgi.escape(self.request.get('year'))
		week.week = cgi.escape(self.request.get('week'))	
		week.put()
		self.redirect('/')


class AddRelation(webapp.RequestHandler):
	def post(self):
		if self.request.get('relation') != "":
			cid = int(float(self.request.get('contact')))
			rid = int(float(self.request.get('relation')))
			contact = datamodel.Contact.get_by_id(cid)
			rel = datamodel.Contact.get_by_id(rid)
			contact.relations.append(rel.key())
			contact.put()
			rel.relations.append(contact.key())
			rel.put()
		
		self.redirect('/contact/' + self.request.get('contact'))
		
class AddWeekForUser(webapp.RequestHandler):
	def post(self):
		if self.request.get('week') != "":
			cid = int(float(self.request.get('contact')))
			wid = int(float(self.request.get('week')))
			contact = datamodel.Contact.get_by_id(cid)
			week = datamodel.Week.get_by_id(wid)
			contact.weeks.append(week.key())
			contact.put()

		self.redirect('/contact/' + self.request.get('contact'))	
		
class MailingList(webapp.RequestHandler):
	def get(self):
		self.response.out.write('zach@terabytegames.com') #email me first
		contacts = datamodel.Contact.all()
		# wid_string = self.request.get('week')
		# if wid_string != "":
		# 	wid = int(float(wid_string))
		# 	week = datamodel.Week.get_by_id(wid)
		# 	contacts.filter('weeks = ', week.key())
		for contact in contacts:
			if contact.email != "":
				self.response.out.write(', ' + contact.email) #adds the email for every contact in a CSV format
				
class AllContactsJSON(webapp.RequestHandler):
	def get(self):
		self.response.out.write('{')
		contacts = datamodel.Contact.all()		
		for contact in contacts:
			cid = contact.key().id()
			self.response.out.write('"' + str(cid) + '"<br/>')
			self.response.out.write(':{"email":"' + contact.email + '"<br/>')
			self.response.out.write(',"firstName":"' + contact.firstName + '"<br/>')
			self.response.out.write(',"lastName":"' + contact.lastName + '"<br/>')
			self.response.out.write(',"cellPhone":"' + contact.cellPhone + '"<br/>')
			self.response.out.write(',"homePhone":"' + contact.homePhone + '"<br/>')
			self.response.out.write(',"school":"' + contact.school + '"<br/>')
			self.response.out.write(',"contactType":"' + contact.contactType + '"<br/>')
			address = ''
			if contact.address:
				address = contact.address
			self.response.out.write('","address":"' + address + '"<br/>')
			self.response.out.write('},')
		self.response.out.write('}')
									
def main():
	application = webapp.WSGIApplication(
		[
			('/add', AddForm),
			('/addWeek', AddWeek),
			('/addWeekAction', AddWeekAction),
			('/addContact', AddContact),
			('/addRelation', AddRelation),
			('/addWeekForUser', AddWeekForUser),
			('/contact/edit/.*', EditContactView),
			('/editContact', EditContact),
			('/contact/.*', ContactView),
			('/search', Search),
			('/mailingList', MailingList),
			('/allContacts.json', AllContactsJSON),
			('/filter/week', FilterByWeek),
			('/week/.*', ViewWeek),
			('/.*', ViewAll),
		],
		debug=True)
		
	run_wsgi_app(application)


if __name__ == "__main__":
	main()
	
	
	
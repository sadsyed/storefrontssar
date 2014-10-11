import cloudstorage as gcs
from google.appengine.api import app_identity
from google.appengine.api import files, images
from google.appengine.api import users
from google.appengine.ext import ndb
import os
import webapp2
import jinja2
import logging
import cgi
import urllib
import datetime
import json
import re
import uuid


#Probably not necessary to change default retry params, but here for example
my_default_retry_params = gcs.RetryParams(initial_delay=0.2,
                                          max_delay=5.0,
                                          backoff_factor=2,
                                          max_retry_period=15)
#TODO - Not sure this is the right place for this.
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__) + '/templates'),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainPage(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('index.html')
        #templateVars = { "app_id" : AP_ID_GLOBAL, "other_html" : ""}
      	fullhtml = template.render()
       	self.response.write(fullhtml)

application = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
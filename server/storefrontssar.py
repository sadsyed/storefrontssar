import os
import cloudstorage as gcs
from google.appengine.api import app_identity
from google.appengine.api import files, images
from google.appengine.api import users
from google.appengine.ext import ndb
import webapp2
import logging
import cgi
import urllib
import datetime
import json
import re
import uuid
import string
import jinja2

#Probably not necessary to change default retry params, but here for example
my_default_retry_params = gcs.RetryParams(initial_delay=0.2,
                                          max_delay=5.0,
                                          backoff_factor=2,
                                          max_retry_period=15)

JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__) + '/templates'), extensions=['jinja2.ext.autoescape'], autoescape=True)


class MainPage(webapp2.RequestHandler):
    def get(self):
    	logging.info("Environment: " + str(os.path.dirname(__file__) + '/templates'))
       	self.response.write("teststring")

application = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
import cloudstorage as gcs
from google.appengine.api import users
from google.appengine.api import urlfetch
from google.appengine.api import files, images
from google.appengine.ext import db
from google.appengine.ext import blobstore, deferred
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.api import app_identity
import datetime
from datetime import timedelta
from time import gmtime, strftime
from google.appengine.ext import ndb
import webapp2
import logging
import json
import cgi
import urllib
import urllib2
from urlparse import urlparse
import re
import os
import uuid
import base64
import string
import jinja2


APP_ID_GLOBAL = 'storefrontssar.appspot.com'
#Probably not necessary to change default retry params, but here for example
my_default_retry_params = gcs.RetryParams(initial_delay=0.2,
                                          max_delay=5.0,
                                          backoff_factor=2,
                                          max_retry_period=15)
tmp_filenames_to_clean_up = []
gcs.set_default_retry_params(my_default_retry_params)
#this is the list of streams, keys are the userid that owns the stream, each value is a list of stream
ds_key = ndb.Key('storefrontssar', 'storefrontssar')

JINJA_ENVIRONMENT = jinja2.Environment(
  loader=jinja2.FileSystemLoader(os.path.dirname(__file__) + '/templates'),
  extensions=['jinja2.ext.autoescape'],
  autoescape=True)


class myArticle(ndb.Model):
  articlename = ndb.StringProperty()
  articleid = ndb.StringProperty()
  articletype = ndb.StringProperty()
  articleimageurl = ndb.StringProperty()
  articlelastused = ndb.StringProperty(repeated=True)
  articletimesused = ndb.IntegerProperty()
  articletags = ndb.StringProperty(repeated=True)
  articleprice = ndb.FloatProperty()
  articledescription = ndb.StringProperty()


class MainPage(webapp2.RequestHandler):
  def get(self):
    template = JINJA_ENVIRONMENT.get_template('index.html')
    template2 = JINJA_ENVIRONMENT.get_template('merch.html')
    merchhtml = template2.render()
    templateVars = { "pagehtml" : merchhtml}
    fullhtml = template.render(templateVars)
    self.response.write(fullhtml)

class CreateArticle(webapp2.RequestHandler):
  def post(self):
    try:
      data = json.loads(self.request.body)
      logging.info('Json data sent to this function: ' + str(data))
      logging.info("ARticle: " + str(data['articlename']))
      present_query = myArticle.query(myArticle.articlename == data['articlename'])
      logging.info('Created query')
      try:
        existsarticle = present_query.get()
        logging.info('Query returned: ' + str(existsarticle))
        if(existsarticle == None):
          thisArticle = myArticle(parent=ndb.Key('storefrontssar', 'storefrontssar'))
          logging.info('Got key')
          thisArticle.articlename = data['articlename']
          logging.info('After article name')
          thisArticle.articledescription = data['articledescription']
          logging.info('After article description')
          thisArticle.articleid = data['articleid']
          thisArticle.articletype = data['articletype']
          logging.info('After article type')
          thisArticle.articleimageurl = data['articleimageurl']
          logging.info('After imageurl')
          thisArticle.articlelastused = data['articlelastused']
          logging.info('After article last used')
          thisArticle.articletags = data['articletags']
          thisArticle.articleprice = data['articleprice']
          logging.info('This article: ' + str(thisArticle))
          thisArticle.put()
          result = json.dumps({'errorcode':0}) # Error code 0: Success
        else:
          result = json.dumps({'errorcode':5}) # Error code 5: Article already exists
      except:
        result = json.dumps({'errorcode':2}) # Error code 2: error writing to datastore
    except:
      result = json.dumps({'errorcode':1}) # No corred json data
    self.response.write(result)

class DeleteArticle(webapp2.RequestHandler):
  def post(self):
    try:
      data = json.loads(self.request.body)
      logging.info('Json data sent to this function: ' + str(data))
      articlenamestodelete = data['articlenamestodelete'] # list of article names to delete
      logging.info('Articlenames are: ' + str(articlenamestodelete))
      article_keys = list()
      tempresult = ""
      for deletearticle in articlenamestodelete:
        logging.info("Delete article is: " + str(deletearticle))
        article_query = myArticle.query(myArticle.articlename == deletearticle)
        logging.info('Created query: ' + str(article_query))
        mydeletearticle = article_query.get()
        logging.info('past get from query')
        if(not mydeletearticle == None):
          logging.info('Delete article is: ' + str(mydeletearticle))
          article_keys.append(mydeletearticle.key)
        else:
          logging.info('Delete article was equal to none, query to delete returned no result')
          tempresult = {'errorcode':4} # Error code 4: Warning, not all articles deleted
        ## Todo, write delete.
        ## Todo, delete actual image.
      ndb.delete_multi(article_keys)
      if (not tempresult == {'errorcode':4}):
        result = json.dumps({'errorcode':0})
      else:
        result = json.dumps(tempresult)
    except:
      result = json.dumps({'errorcode':1}) # Error code 1: Article name already exists or is not found, or no json data
    self.response.write(result)


class UseArticle(webapp2.RequestHandler):
  def post(self):
    try:
      data = json.loads(self.request.body)
      logging.info('Json data sent to this function: ' + str(data))
      result = json.dumps({'errorcode':0})
    except:
      result = json.dumps({'errorcode':1}) # Error code 1: Article already exists or no json data

class ViewArticle(webapp2.RequestHandler):
  def post(self):
    try:
      data = json.loads(self.request.body)
      logging.info('Json data sent to this function: ' + str(data))
      result = json.dumps({'errorcode':0})
    except:
      result = json.dumps({'errorcode':1}) # Error code 1: Article already exists or no json data

class GetMerch(webapp2.RequestHandler):
    def get(self):
      logging.info('Returning merchandise.')
      allarticle_query = myArticle.query().order(myArticle.articletimesused)
      allarticlesbyused = allarticle_query.fetch()
      mymerch = list()
      for thisarticle in allarticlesbyused:
        thismerch = {'imageurl':thisarticle.articleimageurl,'productName':thisarticle.articlename,'productDescription':thisarticle.articledescription,'productPrice':thisarticle.articleprice}
        mymerch.append(thismerch)
      logging.info("The merch list: " + str(mymerch))
      result = json.dumps({'myMerch': mymerch}) #[{merchandise},{merchandise}]
      logging.info("Result is: " + str(result))
      self.response.write(result)

application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/GetMerch', GetMerch),
    ('/CreateArticle', CreateArticle),
    ('/DeleteArticle', DeleteArticle),
    ('/UseArticle', UseArticle),
    ('/ViewArticle', ViewArticle)
], debug=True)



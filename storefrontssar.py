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


APP_ID_GLOBAL = 'storefrontssar2.appspot.com'
#Probably not necessary to change default retry params, but here for example
my_default_retry_params = gcs.RetryParams(initial_delay=0.2,
                                          max_delay=5.0,
                                          backoff_factor=2,
                                          max_retry_period=15)
tmp_filenames_to_clean_up = []
gcs.set_default_retry_params(my_default_retry_params)
ds_key = ndb.Key('storefrontssar2', 'storefrontssar2')

JINJA_ENVIRONMENT = jinja2.Environment(
  loader=jinja2.FileSystemLoader(os.path.dirname(__file__) + '/templates'),
  extensions=['jinja2.ext.autoescape'],
  autoescape=True)

class articleImage(ndb.Model):
  imageid = ndb.StringProperty()
  comments = ndb.StringProperty()
  imagefileurl = ndb.StringProperty()
  imagecreationdate = ndb.StringProperty()
  imagearticleid = ndb.StringProperty()

class myArticle(ndb.Model):
  articlename = ndb.StringProperty()
  articleowner = ndb.StringProperty()
  articleid = ndb.StringProperty()
  articletype = ndb.StringProperty()
  articleimageurl = ndb.StringProperty()
  articlelastused = ndb.StringProperty(repeated=True)
  articletimesused = ndb.IntegerProperty()
  articletags = ndb.StringProperty(repeated=True)
  articleprice = ndb.FloatProperty()
  articledescription = ndb.StringProperty()
  articleoktosell = ndb.BooleanProperty()


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
      logging.info("Article Name: " + str(data['articleName']))
      present_query = myArticle.query(myArticle.articlename == data['articleName'])
      logging.info('Created query')
      articlereturnid = str(uuid.uuid1())
      try:
        existsarticle = present_query.get()
        logging.info('Query returned: ' + str(existsarticle))
        if(existsarticle == None):
          thisArticle = myArticle(parent=ndb.Key('storefrontssar2', 'storefrontssar2'))
          logging.info('Got key')
          thisArticle.articlename = data['articleName']
          logging.info('After article name')
          thisArticle.articledescription = data['articleDescription']
          thisArticle.articleid = articlereturnid
          thisArticle.articleowner = data['articleOwner']
          thisArticle.articletype = data['articleType']
          logging.info('After article type')
          #TODO: Create a list processor for tags
          tags = list()
          tags.append(data['articleTags'])
          logging.info('pulled tag list')
          thisArticle.articletags = tags
          logging.info('done with taglist')
          #TODO: Process price
          val = 0.0
          try:
            val = int(data['articlePrice'])
          except ValueError:
            val = float(data['articlePrice'])
          thisArticle.articleprice = val
          logging.info("Got article price")
          oktosell = False
          if data['articleOkToSell'] == 'true':
            oktosell = True
          thisArticle.articleoktosell = oktosell
          logging.info('This article: ' + str(thisArticle))
          thisArticle.put()
          result = json.dumps({'returnval':articlereturnid}) # Error code 0: Success
        else:
          result = json.dumps({'returnval':5}) # Error code 5: Article already exists
      except:
        result = json.dumps({'returnval':2}) # Error code 2: error writing to datastore
    except:
      result = json.dumps({'returnval':1}) # No corred json data
    self.response.write(result)

class AndroidUploadHandler(blobstore_handlers.BlobstoreUploadHandler):

    def initialize(self, request, response):
        super(AndroidUploadHandler, self).initialize(request, response)
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers[
            'Access-Control-Allow-Methods'
        ] = 'OPTIONS, HEAD, GET, POST, PUT'
        self.response.headers[
            'Access-Control-Allow-Headers'
        ] = 'Content-Type, Content-Range, Content-Disposition'


    def handle_android_upload(self):
        try:
            articleid = self.request.headers['articleid']
            logging.info('Article ID is: ' + str(articleid))
            logging.info('Check if article exists')
            present_query = myArticle.query(myArticle.articleid  == articleid)
            existsarticle = present_query.get()
            comments = ""
            if not existsarticle == None:
              imageid = str(uuid.uuid1())
              bucket_name = os.environ.get('BUCKET_NAME', app_identity.get_default_gcs_bucket_name())
              logging.info("My bucket name is: " + str(bucket_name))
              bucket = '/' + bucket_name
              filename = bucket + '/' + articleid + '/' + imageid
              try:
                myimagefile = self.request.get('imageFile')
              except:
                logging.info("Imagefile not retrieved from self.request")
              result = {}
              creationdate = str(datetime.datetime.now().date())
              logging.info("starting to write file to store")
            # Create a GCS file with GCS client.
              with gcs.open(filename, 'w') as f:
                f.write(myimagefile)
            # Blobstore API requires extra /gs to distinguish against blobstore files.
              blobstore_filename = '/gs' + filename
              blob_key = blobstore.create_gs_key(blobstore_filename)
              logging.info("Trying to get url for blob key: " + str(blob_key))
              try:
                result['url'] = images.get_serving_url(
                    blob_key,
                )
              except:
                logging.info("Could not get serving url")
                result['url'] = ""
              logging.info("Result url" + str(result['url']))
              myimage = articleImage(parent=ndb.Key('storefrontssar2', 'storefrontssar2'))
              logging.info("Got key")
              myimage.imageid = imageid
              logging.info('after image id')
              myimage.imagefileurl = result['url']
              logging.info('after url')
              myimage.imagecreationdate = creationdate
              logging.info('after creation date')
              myimage.imagearticleid = articleid
              myimage.put()
              logging.info("The image url being assigned is: " + myimage.imagefileurl)
              existsarticle.articleimageurl = myimage.imagefileurl
              existsarticle.put()
        except:
            logging.info("exception uploading files")
        logging.info("Result of image upload is: " + str(result))
        return result

    def options(self):
        pass

    def head(self):
        pass

    def get(self):
        pass

    def post(self):
        logging.info("Post request: " + str(self.request))
        result = {'file': self.handle_android_upload()['url']}
        logging.info("Post result: " + str(result))
        s = json.dumps(result)
        logging.info("Post result writing is: " + str(s))
        self.response.write(s)

class DeleteArticle(webapp2.RequestHandler):
  def post(self):
    try:
      data = json.loads(self.request.body)
      logging.info('Json data sent to this function: ' + str(data))
      articleidstodelete = data['articleidstodelete'] # list of article names to delete
      logging.info('Articleids are: ' + str(articleidstodelete))
      article_keys = list()
      image_keys = list()
      tempresult = ""
      for deletearticle in articleidstodelete:
        logging.info("Delete article is: " + str(deletearticle))
        article_query = myArticle.query(myArticle.articleid == deletearticle)
        logging.info('Created query: ' + str(article_query))
        mydeletearticle = article_query.get()
        logging.info('past get from query')
        if(not mydeletearticle == None):
          logging.info('Delete article is: ' + str(mydeletearticle))
          article_keys.append(mydeletearticle.key)
          deleteurl = mydeletearticle.articleimageurl
          image_query = articleImage.query(articleImage.imagefileurl == deleteurl)
          mydeleteimage = image_query.get()
          if(not mydeleteimage == None):
            logging.info("delete image is: " + str(mydeleteimage))
            image_keys.append(mydeleteimage.key)
          else:
            logging.info('No image found for this article')
        else:
          logging.info('Delete article was equal to none, query to delete returned no result')
          tempresult = {'errorcode':4} # Error code 4: Warning, not all articles deleted
      ndb.delete_multi(article_keys)
      ndb.delete_multi(image_keys)
      if (not tempresult == {'errorcode':4}):
        result = json.dumps({'errorcode':0})
      else:
        result = json.dumps(tempresult)
    except:
      result = json.dumps({'errorcode':1}) # Error code 1: Article name already exists or is not found, or no json data
    self.response.write(result)

class CreateArticlePage(webapp2.RequestHandler):
  def get(self):
    logging.info('In create article')
    template = JINJA_ENVIRONMENT.get_template('index.html')
    template2 = JINJA_ENVIRONMENT.get_template('createarticle.html')
    logging.info('Got the templates')
    createhtml = template2.render()
    templateVars = { "pagehtml" : createhtml}
    fullhtml = template.render(templateVars)
    logging.info('Writing response')
    self.response.write(fullhtml)

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
    ('/AndroidUploadHandler', AndroidUploadHandler),
    ('/DeleteArticle', DeleteArticle),
    ('/UseArticle', UseArticle),
    ('/ViewArticle', ViewArticle),
    ('/CreateArticlePage', CreateArticlePage)
], debug=True)



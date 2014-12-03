#!/usr/bin/env python
import cloudstorage as gcs
from google.appengine.api import users
from google.appengine.api import urlfetch
from google.appengine.api import mail
from google.appengine.api import files, images
from google.appengine.ext import db
from google.appengine.ext import blobstore, deferred
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.api import app_identity
import datetime
from datetime import timedelta
from time import gmtime, strftime
from google.appengine.ext import ndb
from google.appengine.ext.webapp import template
import webapp2
from webapp2_extras import auth
from webapp2_extras import sessions
from webapp2_extras import security
from webapp2_extras.auth import InvalidAuthIdError
from webapp2_extras.auth import InvalidPasswordError
import logging
import json
import cgi
import urllib
import urllib2
from urlparse import urlparse
import re
import os
import os.path
import uuid
import base64
import string


APP_ID_GLOBAL = 'storefrontssar2.appspot.com'
STORAGE_ID_GLOBAL = 'storefrontssar2'
#Probably not necessary to change default retry params, but here for example
my_default_retry_params = gcs.RetryParams(initial_delay=0.2,
                                          max_delay=5.0,
                                          backoff_factor=2,
                                          max_retry_period=15)
tmp_filenames_to_clean_up = []
gcs.set_default_retry_params(my_default_retry_params)
ds_key = ndb.Key(STORAGE_ID_GLOBAL, STORAGE_ID_GLOBAL)

class smartClosetUser(ndb.Model):
  userPin = ndb.StringProperty()
  userName = ndb.StringProperty()
  userEmail = ndb.StringProperty()
  userMarkdown = ndb.StringProperty()
  displayitemsnotusedwindow = ndb.StringProperty()


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
  articleprivate = ndb.BooleanProperty()

class Category:
  def __init__(self, categoryName, lastUsedArticleImageUrl):
    self.categoryName = categoryName
    self.lastUsedArticleImageUrl = lastUsedArticleImageUrl

def user_required(handler):
  """
    Decorator that checks if there's a user associated with the current session.
    Will also fail if there's no session present.
  """
  def check_login(self, *args, **kwargs):
    auth = self.auth
    if not auth.get_user_by_session():
      self.redirect(self.uri_for('login'), abort=True)
    else:
      return handler(self, *args, **kwargs)

  return check_login

class BaseHandler(webapp2.RequestHandler):
  @webapp2.cached_property
  def auth(self):
    """Shortcut to access the auth instance as a property."""
    return auth.get_auth()

  @webapp2.cached_property
  def user_info(self):
    """Shortcut to access a subset of the user attributes that are stored
    in the session.
    The list of attributes to store in the session is specified in
      config['webapp2_extras.auth']['user_attributes'].
    :returns
      A dictionary with most user information
    """
    return self.auth.get_user_by_session()

  @webapp2.cached_property
  def user(self):
    """Shortcut to access the current logged in user.
    Unlike user_info, it fetches information from the persistence layer and
    returns an instance of the underlying model.
    :returns
      The instance of the user model associated to the logged in user.
    """
    u = self.user_info
    return self.user_model.get_by_id(u['user_id']) if u else None

  @webapp2.cached_property
  def user_model(self):
    """Returns the implementation of the user model.
    It is consistent with config['webapp2_extras.auth']['user_model'], if set.
    """    
    return self.auth.store.user_model

  @webapp2.cached_property
  def session(self):
      """Shortcut to access the current session."""
      return self.session_store.get_session(backend="datastore")

  def render_template(self, view_filename, params=None):
    if not params:
      params = {}
    user = self.user_info
    params['user'] = user
    path = os.path.join(os.path.dirname(__file__), 'views', view_filename)
    self.response.out.write(template.render(path, params))

  def render_template2(self, view_filename, params=None):
    if not params:
      params = {}
    user = self.user_info
    params['user'] = user
    path = os.path.join(os.path.dirname(__file__), 'views', view_filename)
    return template.render(path, params)

  def display_message(self, message):
    """Utility function to display a template with a simple message."""
    params = {
      'message': message
    }
    self.render_template('message.html', params)

  # this is needed for webapp2 sessions to work
  def dispatch(self):
      # Get a session store for this request.
      self.session_store = sessions.get_store(request=self.request)

      try:
          # Dispatch the request.
          webapp2.RequestHandler.dispatch(self)
      finally:
          # Save all sessions.
          self.session_store.save_sessions(self.response)

class MainHandler(BaseHandler):
  def get(self):
    self.render_template('closetcontent.html')

class SignupHandlerAndroid(BaseHandler):

  def post(self):
    try:
      url = 'http://' + APP_ID_GLOBAL + '/CreateProfile'
      logging.info('URL for CreateProfile is : ' + str(url))
      data = json.loads(self.request.body)
      logging.info('Json data sent to this function: ' + str(data))

      user_name = data['username']
      logging.info('user_name: ' + str(user_name))
      email = data['email']
      logging.info('email: ' + str(email))
      name = data['name']
      logging.info('name: ' + str(name))
      password = data['password']
      logging.info('password: ' + str(password))
      last_name = data['lastname']
      logging.info('lastname: ' +str(last_name))

      unique_properties = ['email_address']
      user_data = self.user_model.create_user(user_name,
        unique_properties,
        email_address=email, name=name, password_raw=password,
        last_name=last_name, verified=False)
      if not user_data[0]: #user_data is a tuple
        self.display_message('Unable to create user for email %s because of \
          duplicate keys %s' % (user_name, user_data[1]))
        return

      createParams = json.dumps({'username':user_name, 'email':email, 'name':name, 'password':password, 'lastname':last_name})
      result = urlfetch.fetch(url=url, payload=createParams, method=urlfetch.POST, headers={'Content-Type': 'application/json'}, deadline=30)
      logging.info('CreateProfile Result is: ' + str(result.content))
      jsonresult = json.loads(result.content)
      if jsonresult['errorcode'] == 0:
        user = user_data[1]
        user_id = user.get_id() 

        token = self.user_model.create_signup_token(user_id)

        verification_url = self.uri_for('verification', type='v', user_id=user_id,
          signup_token=token, _full=True)


        logging.info("User is: " + str(user_name))
        emailSenderAddress = "smart.closet.service@gmail.com"
        logging.info("set email address")
        content = "Verify your smart closet account at: " + verification_url
        logging.info('set content')

        message = mail.EmailMessage(sender=emailSenderAddress, subject="Smart Closet Email Verification ")

        if not mail.is_email_valid(email):
          logging.info("The email is not valid.")
          self.response.out.write("Email address is not valid.")

        message.to = email
        message.body = """%s""" %(content)
        message.send()
        logging.info("Verification url: " + verification_url)
        result = json.dumps({'errorcode':0})
    except:
      result = json.dumps({'errorcode':1})
      logging.info('Create Profile failed with errorcode: ' + str(result))
    self.response.write(result)

class SignupHandler(BaseHandler):
  def get(self):
    self.render_template('signup.html')

  def post(self):
    url = 'http://' + APP_ID_GLOBAL + '/CreateProfile'
    logging.info('URL for CreateProfile is : ' + str(url))
    user_name = self.request.get('username')
    email = self.request.get('email')
    name = self.request.get('name')
    password = self.request.get('password')
    last_name = self.request.get('lastname')

    unique_properties = ['email_address']
    user_data = self.user_model.create_user(user_name,
      unique_properties,
      email_address=email, name=name, password_raw=password,
      last_name=last_name, verified=False)
    if not user_data[0]: #user_data is a tuple
      self.display_message('Unable to create user for email %s because of \
        duplicate keys %s' % (user_name, user_data[1]))
      return

    createParams = json.dumps({'username':user_name, 'email':email, 'name':name, 'password':password, 'lastname':last_name})
    result = urlfetch.fetch(url=url, payload=createParams, method=urlfetch.POST, headers={'Content-Type': 'application/json'}, deadline=30)
    logging.info('CreateProfile Result is: ' + str(result.content))
    jsonresult = json.loads(result.content)
    if jsonresult['errorcode'] == 0:
      user = user_data[1]
      user_id = user.get_id() 

      token = self.user_model.create_signup_token(user_id)

      verification_url = self.uri_for('verification', type='v', user_id=user_id,
        signup_token=token, _full=True)

      logging.info("User is: " + str(user_name))
      emailSenderAddress = "smart.closet.service@gmail.com"
      logging.info("set email address")
      content = "Verify your smart closet account at: " + verification_url
      logging.info('set content')

      message = mail.EmailMessage(sender=emailSenderAddress, subject="Smart Closet Email Verification ")

      if not mail.is_email_valid(email):
        logging.info("The email is not valid.")
        self.response.out.write("Email address is not valid.")

      message.to = email
      message.body = """%s""" %(content)
      message.send()
    
    msg = "Verification message has been sent to: " + email
    self.display_message(msg)


class ForgotPasswordHandler(BaseHandler):
  def get(self):
    self._serve_page()

  def post(self):
    username = self.request.get('username')

    user = self.user_model.get_by_auth_id(username)
    if not user:
      logging.info('Could not find any user entry for username %s', username)
      self._serve_page(not_found=True)
      return

    user_id = user.get_id()
    token = self.user_model.create_signup_token(user_id)

    verification_url = self.uri_for('verification', type='p', user_id=user_id,
      signup_token=token, _full=True)

    #msg = 'Reset password link:  <a href="{url}">{url}</a>'

    email = user.email_address
    logging.info('got target email')
    emailSenderAddress = "smart.closet.service@gmail.com"
    logging.info("set email address")
    content = "Reset your smart closet password at: " + verification_url
    logging.info('set content')

    message = mail.EmailMessage(sender=emailSenderAddress, subject="Smart Closet Password Reset Notification ")

    if not mail.is_email_valid(email):
      logging.info("The email is not valid.")
      self.response.out.write("Email address is not valid.")

    message.to = email
    message.body = """%s""" %(content)
    message.send()

    self.display_message("Reset password link sent to: " + str(email)) 
  
  def _serve_page(self, not_found=False):
    username = self.request.get('username')
    params = {
      'username': username,
      'not_found': not_found
    }
    self.render_template('forgot.html', params)


class VerificationHandler(BaseHandler):
  def get(self, *args, **kwargs):
    user = None
    user_id = kwargs['user_id']
    signup_token = kwargs['signup_token']
    verification_type = kwargs['type']

    # it should be something more concise like
    # self.auth.get_user_by_token(user_id, signup_token)
    # unfortunately the auth interface does not (yet) allow to manipulate
    # signup tokens concisely
    user, ts = self.user_model.get_by_auth_token(int(user_id), signup_token,
      'signup')

    if not user:
      logging.info('Could not find any user with id "%s" signup token "%s"',
        user_id, signup_token)
      self.abort(404)
    
    # store user data in the session
    self.auth.set_session(self.auth.store.user_to_dict(user), remember=True)

    if verification_type == 'v':
      # remove signup token, we don't want users to come back with an old link
      self.user_model.delete_signup_token(user.get_id(), signup_token)

      if not user.verified:
        user.verified = True
        user.put()

      self.display_message('User email address has been verified.')
      return
    elif verification_type == 'p':
      # supply user to the page
      params = {
        'user': user,
        'token': signup_token
      }
      self.render_template('resetpassword.html', params)
    else:
      logging.info('verification type not supported')
      self.abort(404)

class SetPasswordHandler(BaseHandler):

  @user_required
  def post(self):
    password = self.request.get('password')
    old_token = self.request.get('t')

    if not password or password != self.request.get('confirm_password'):
      self.display_message('passwords do not match')
      return

    user = self.user
    user.set_password(password)
    user.put()

    # remove signup token, we don't want users to come back with an old link
    self.user_model.delete_signup_token(user.get_id(), old_token)
    
    self.display_message('Password updated')

class LoginHandler(BaseHandler):
  def get(self):
    self._serve_page()

  def post(self):
    username = self.request.get('username')
    password = self.request.get('password')
    try:
      u = self.auth.get_user_by_password(username, password, remember=True,
        save_session=True)
      self.redirect(self.uri_for('authenticated'))
    except (InvalidAuthIdError, InvalidPasswordError) as e:
      logging.info('Login failed for user %s because of %s', username, type(e))
      self._serve_page(True)

  def _serve_page(self, failed=False):
    username = self.request.get('username')
    params = {
      'username': username,
      'failed': failed
    }
    self.render_template('login.html', params)

class LogoutHandler(BaseHandler):
  def get(self):
    self.auth.unset_session()
    self.redirect(self.uri_for('home'))

class AuthenticatedHandler(BaseHandler):
  @user_required
  def get(self):
    user = self.user
    logging.info("User is: " + str(user))
    email = user.email_address
    logging.info("User email: " + email)
    present_query = smartClosetUser.query(smartClosetUser.userEmail == email)
    logging.info('Created query')
    try:
      existsuser = present_query.get()
      logging.info("Query returned: " + str(existsuser))
      params = {'userName':existsuser.userName,'userPin':existsuser.userPin,'userMarkdown':existsuser.userMarkdown,'displayitemsnotusedwindow':existsuser.displayitemsnotusedwindow,'userEmail':existsuser.userEmail}
    except:
      pass
    self.render_template('authenticated.html',params)

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
          thisArticle = myArticle(parent=ndb.Key(STORAGE_ID_GLOBAL, STORAGE_ID_GLOBAL))
          logging.info('Got key')
          thisArticle.articlename = data['articleName']
          logging.info('After article name')
          thisArticle.articledescription = data['articleDescription']
          thisArticle.articleid = articlereturnid
          thisArticle.articlelastused = list()
          thisArticle.articletimesused = 0
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
          aprivate = False
          if data['articlePrivate'] == 'true':
            aprivate = True
          thisArticle.articleprivate = aprivate
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
            myimage = articleImage(parent=ndb.Key(STORAGE_ID_GLOBAL, STORAGE_ID_GLOBAL))
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
      articleidstodelete = data['articleidstodelete'] # list of article ids to delete
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

class GetArticleInfo(BaseHandler):
  @user_required
  def post(self):
    logging.info('In GetArticleinfo article request is: ' + str(self.request))
    articleName = self.request.get('articleName')
    logging.info("The article name is: " + str(articleName))
    present_query = myArticle.query(myArticle.articlename == articleName)
    logging.info('Created query')
    returnarticle = None
    try:
      existsarticle = present_query.get()
      returnarticle = {'articleName':existsarticle.articlename,'articleOwner':existsarticle.articleowner,'articleId':existsarticle.articleid,'articleType':existsarticle.articletype,'articleImageUrl':existsarticle.articleimageurl,'articleLastUsed':existsarticle.articlelastused,'articleTimesUsed':existsarticle.articletimesused,'articleTags':existsarticle.articletags,'articlePrice':existsarticle.articleprice,'articleDescription':existsarticle.articledescription,'articleOkToSell':existsarticle.articleoktosell}
    except:
      returnarticle = {'error': 11}
    fullhtml = json.dumps(returnarticle)
    self.response.write(fullhtml)

class ReadArticle(webapp2.RequestHandler):
  def post(self):
    try:
      data = None
      articleId = None
      try:
        logging.info(str(self.request))
        try:
          data = json.loads(self.request.body)
          logging.info('json data received: ' + str(data)) 
          articleId = data['articleId']
        except:
          articleId = self.request.get('articleId')
          logging.info('Article id is: ' + str(articleId))
      except:
        logging.info('Error getting request data')
      present_query = myArticle.query(myArticle.articleid == articleId)
      logging.info('Created query')
      try:
        existsarticle = present_query.get()
        returnarticle = {'articleName':existsarticle.articlename,'articleOwner':existsarticle.articleowner,'articleId':existsarticle.articleid,'articleType':existsarticle.articletype,'articleImageUrl':existsarticle.articleimageurl,'articleLastUsed':existsarticle.articlelastused,'articleTimesUsed':existsarticle.articletimesused,'articleTags':existsarticle.articletags,'articlePrice':existsarticle.articleprice,'articleDescription':existsarticle.articledescription,'articleOkToSell':existsarticle.articleoktosell}
        logging.info('Query returned: ' + str(existsarticle))
        result = json.dumps(returnarticle)
      except:
        pass
    except:
      result = json.dumps({'errorcode':1}) # Error code 1: Article already exists or no json data
    self.response.write(result)

class UseArticle(webapp2.RequestHandler):
  def post(self):
    try:
      data = json.loads(self.request.body)
      logging.info('Json data sent to this function: ' + str(data))
      logging.info("Article ID: " + str(data['articleId']))
      present_query = myArticle.query(myArticle.articleid == data['articleId'])
      logging.info('Created query')
      try:
        existsarticle = present_query.get()
        logging.info('Query returned: ' + str(existsarticle))
        usedate = str(datetime.datetime.now().date())
        logging.info('Use date is: ' + usedate)
        tempusedlist = existsarticle.articlelastused
        tempusedlist.append(usedate)
        logging.info("Appended date")
        existsarticle.articletimesused = len(tempusedlist)
        logging.info('Times used is now: ' + str(len(tempusedlist)))
        existsarticle.articlelastused = tempusedlist
        existsarticle.put()
        result = json.dumps({'errorcode':0})
      except:
        result = json.dumps({'errorcode':8}) #Error code 8: unable to update uses for article
    except:
      result = json.dumps({'errorcode':1}) # Error code 1: Article already exists or no json data
    self.response.write(result)

class UpdateArticle(webapp2.RequestHandler):

  def post(self):
    result = {}
    try:
      data = json.loads(self.request.body)
      # for items that have values which are lsits, this specifies if you append or replace the item
      # does not apply to single items
      logging.info('Json data sent to this function: ' + str(data))
      logging.info("Article ID: " + str(data['articleId']))
      present_query = myArticle.query(myArticle.articleid == data['articleId'])
      logging.info('Created query')
      try:
        existsarticle = present_query.get()
        logging.info('Query returned: ' + str(existsarticle))
        if data['fieldToUpdate'] == 'articleName': 
          existsarticle.articlename = data['newValue']
          result = json.dumps({'errorcode':0})
        if data['fieldToUpdate'] == 'articleOwner': 
          existsarticle.articleowner = data['newValue']
          result = json.dumps({'errorcode':0})
        if data['fieldToUpdate'] == 'articleType': 
          existsarticle.articletype = data['newValue']
          result = json.dumps({'errorcode':0})
        if data['fieldToUpdate'] == 'articleLastUsed':
          try:
            if data['append'] == 'false':
              logging.info("Replacing whole last used list.")
              existsarticle.articlelastused = data['newValue']
              existsarticle.articletimesused = len(data['newValue'])
              result = json.dumps({'errorcode':0})
            else:
              logging.info('Appending item to last used list')
              templist = existsarticle.articlelastused
              templist.append(data['newValue'])
              existsarticle.articletimesused = len(templist)
              existsarticle.articlelastused = templist
              result = json.dumps({'errorcode':0})
          except:
            result = json.dumps({'errorcode':7}) # Errorcode 7: did not specify append or replace
        if data['fieldToUpdate'] == 'articleTags': 
          try:
            if data['append'] == 'false':
              logging.info("Replacing whole taglist.")
              existsarticle.articletags = data['newValue']
              result = json.dumps({'errorcode':0})
            else:
              logging.info('Appending item to tag list')
              templist = existsarticle.articletags
              templist.append(data['newValue'])
              existsarticle.articletags = templist
              result = json.dumps({'errorcode':0})
          except:
            result = json.dumps({'errorcode':7}) # Errorcode 7: did not specify append or replace
        if data['fieldToUpdate'] == 'articlePrice':
          val = 0.0
          logging.info("Trying to update: " + str(data['fieldToUpdate']))
          try:
            val = int(data['newValue'])
            logging.info("Got past int val.")
          except ValueError:
            val = float(data['newValue'])
            logging.info('got past float val.')
          existsarticle.articleprice = val
          result = json.dumps({'errorcode':0})
        if data['fieldToUpdate'] == 'articleDescription':
          existsarticle.articledescription = data['newValue']
          result = json.dumps({'errorcode':0})
        if data['fieldToUpdate'] == 'articleOkToSell':
          if data['newValue'] == 'true':
            existsarticle.articleoktosell = True
          else:
            existsarticle.articleoktosell = False
          result = json.dumps({'errorcode':0})
        logging.info("Seemed to get value, trying to write")
        existsarticle.put()
      except:
        pass
      
    except:
      result = json.dumps({'errorcode':1}) 
    self.response.write(result)


class GetUsers(webapp2.RequestHandler):

  def get(self):
    allusername_query = smartClosetUser.query().order(smartClosetUser.userName)
    allusers = allusername_query.fetch()
    logging.info('Created query')
    userlist = []
    try:
      for existsuser in allusers:
        userlist.append(existsuser.userName)
      result = json.dumps({'userList':userlist})
    except:
      result = json.dumps({'errorcode':9}) # Error code 9: Can't configure 
    self.response.write(result)

class GetAccountSettings(BaseHandler):
  @user_required
  def get(self):
    user = self.user
    logging.info("User is: " + str(user))
    email = user.email_address
    logging.info("User email: " + email)
    present_query = smartClosetUser.query(smartClosetUser.userEmail == email)
    logging.info('Created query')
    try:
      existsuser = present_query.get()
      logging.info("Query returned: " + str(existsuser))
      result = json.dumps({'userName':existsuser.userName,'userPin':existsuser.userPin,'userMarkdown':existsuser.userMarkdown,'displayitemsnotusedwindow':existsuser.displayitemsnotusedwindow,'userEmail':existsuser.userEmail})
    except:
      result = json.dumps({'errorcode':9}) # Error code 9: Can't configure 
    self.response.write(result)

class ConfigureAccount(BaseHandler):

  @user_required
  def post(self):
    try:
      logging.info('POST data sent to this function: ' + str(self.request))
      user = self.user
      logging.info("User is: " + str(user))
      email = user.email_address
      logging.info("User email: " + email)
      present_query = smartClosetUser.query(smartClosetUser.userEmail == email)
      logging.info('Created query')
      try:
        existsuser = present_query.get()
        logging.info("Query returned: " + str(existsuser))
        existsuser.userPin = self.request.get('pin')
        existsuser.userMarkdown = self.request.get('markdown')
        existsuser.displayitemsnotusedwindow = self.request.get('usedwindow')
        logging.info('trying to write all items for user' + str(existsuser))
        existsuser.put()
        result = json.dumps({'errorcode':0})
      except:
        result = json.dumps({'errorcode':9}) # Error code 9: Can't configure user because user not found.
    except:
      pass
    self.redirect("/")

class GetSaleCategories(webapp2.RequestHandler):
    def post(self):
      emailfilter = None
      try:
        data = json.loads(self.request.body)
        emailfilter = data['emailFilter']
      except:
        logging.info("No json data, no email filter.")
      allarticle_query = myArticle.query().order(myArticle.articletimesused)
      allarticlesbyused = allarticle_query.fetch()
      currentcategories = {}
      for thisarticle in allarticlesbyused:
        if not emailfilter == None:
          try:
            logging.info('trying to add for owner: ' + emailfilter + ' article is: ' + thisarticle.articleowner)
            if thisarticle.articleowner == emailfilter and thisarticle.articleoktosell: 
              currentcategories[thisarticle.articletype] = Category(thisarticle.articletype, thisarticle.articleimageurl)
          except:
            for thisowner in emailfilter:
              logging.info('is list, owner is: ' + thisowner)
              if thisarticle.articleowner == thisowner and thisarticle.articleoktosell: 
                logging.info('adding item for owner in list')
                currentcategories[thisarticle.articletype] = Category(thisarticle.articletype, thisarticle.articleimageurl)
        else:
          if thisarticle.articleoktosell:
            currentcategories[thisarticle.articletype] = Category(thisarticle.articletype, thisarticle.articleimageurl)
      returncategories = list()
      for item in currentcategories:
        category = {'name':currentcategories[item].categoryName, 'lastUsedArticleImageUrl':currentcategories[item].lastUsedArticleImageUrl}
        returncategories.append(category)
      result = json.dumps({'currentCategories':returncategories})
      logging.info("Returning: " + str(result))
      self.response.write(result)

class GetSaleCategories2(webapp2.RequestHandler):
    def post(self):
      emailfilter = None
      try:
        data = json.loads(self.request.body)
        emailfilter = data['emailFilter']
      except:
        logging.info("No json data, no email filter.")
      allarticle_query = myArticle.query().order(myArticle.articletimesused)
      allarticlesbyused = allarticle_query.fetch()
      currentcategories = {}
      for thisarticle in allarticlesbyused:
        if not emailfilter == None:
          try:
            logging.info('trying to add for owner: ' + emailfilter + ' article is: ' + thisarticle.articleowner)
            if thisarticle.articleowner == emailfilter and thisarticle.articleoktosell: 
              currentcategories[thisarticle.articletype] = Category(thisarticle.articletype, thisarticle.articleimageurl)
          except:
            for thisowner in emailfilter:
              logging.info('is list, owner is: ' + thisowner)
              if thisarticle.articleowner == thisowner and thisarticle.articleoktosell: 
                logging.info('adding item for owner in list')
                currentcategories[thisarticle.articletype] = Category(thisarticle.articletype, thisarticle.articleimageurl)
        else:
          if thisarticle.articleoktosell:
            currentcategories[thisarticle.articletype] = Category(thisarticle.articletype, thisarticle.articleimageurl)
      returncategories = list()
      for item in currentcategories:
        category = {'name':currentcategories[item].categoryName, 'lastUsedArticleImageUrl':currentcategories[item].lastUsedArticleImageUrl}
        returncategories.append(category)
      result = json.dumps({'currentCategories':returncategories})
      logging.info("Returning: " + str(result))
      self.response.write(result)

class GetCategories(webapp2.RequestHandler):
    def post(self):
      emailfilter = None
      try:
        data = json.loads(self.request.body)
        emailfilter = data['emailFilter']
      except:
        logging.info("No json data, no email filter.")
      allarticle_query = myArticle.query().order(myArticle.articletimesused)
      allarticlesbyused = allarticle_query.fetch()
      currentcategories = {}
      for thisarticle in allarticlesbyused:
        if not emailfilter == None:
          try:
            logging.info('trying to add for owner: ' + emailfilter + ' article is: ' + thisarticle.articleowner)
            if thisarticle.articleowner == emailfilter: 
              currentcategories[thisarticle.articletype] = Category(thisarticle.articletype, thisarticle.articleimageurl)
          except:
            for thisowner in emailfilter:
              logging.info('is list, owner is: ' + thisowner)
              if thisarticle.articleowner == thisowner: 
                logging.info('adding item for owner in list')
                currentcategories[thisarticle.articletype] = Category(thisarticle.articletype, thisarticle.articleimageurl)
        else:
            currentcategories[thisarticle.articletype] = Category(thisarticle.articletype, thisarticle.articleimageurl)
      returncategories = list()
      for item in currentcategories:
        category = {'name':currentcategories[item].categoryName, 'lastUsedArticleImageUrl':currentcategories[item].lastUsedArticleImageUrl}
        returncategories.append(category)
      result = json.dumps({'currentCategories':returncategories})
      logging.info("Returning: " + str(result))
      self.response.write(result)

class GetCategory(webapp2.RequestHandler):
  def post(self):
    try:
      emailfilter = None
      try:
        data = json.loads(self.request.body)
        emailfilter = data['emailFilter']
      except:
        logging.info("No json data for email filter.")
      present_query = myArticle.query(myArticle.articletype == data['category'])
      try:
        returnlist = list()
        existsarticles = present_query.fetch()
        returnarticle = {}
        for existsarticle in existsarticles:
          if not emailfilter == None:
            if type(emailfilter) is list:
              for thisowner in emailfilter:
                if existsarticle.articleowner == thisowner:
                  returnarticle = {'articleName':existsarticle.articlename,'articleOwner':existsarticle.articleowner,'articleId':existsarticle.articleid,'articleType':existsarticle.articletype,'articleImageUrl':existsarticle.articleimageurl,'articleLastUsed':existsarticle.articlelastused,'articleTimesUsed':existsarticle.articletimesused,'articleTags':existsarticle.articletags,'articlePrice':existsarticle.articleprice,'articleDescription':existsarticle.articledescription,'articleOkToSell':existsarticle.articleoktosell}
            else:
              if existsarticle.articleowner == emailfilter:
                logging.info('found match')
                returnarticle = {'articleName':existsarticle.articlename,'articleOwner':existsarticle.articleowner,'articleId':existsarticle.articleid,'articleType':existsarticle.articletype,'articleImageUrl':existsarticle.articleimageurl,'articleLastUsed':existsarticle.articlelastused,'articleTimesUsed':existsarticle.articletimesused,'articleTags':existsarticle.articletags,'articlePrice':existsarticle.articleprice,'articleDescription':existsarticle.articledescription,'articleOkToSell':existsarticle.articleoktosell}
          else:
            returnarticle = {'articleName':existsarticle.articlename,'articleOwner':existsarticle.articleowner,'articleId':existsarticle.articleid,'articleType':existsarticle.articletype,'articleImageUrl':existsarticle.articleimageurl,'articleLastUsed':existsarticle.articlelastused,'articleTimesUsed':existsarticle.articletimesused,'articleTags':existsarticle.articletags,'articlePrice':existsarticle.articleprice,'articleDescription':existsarticle.articledescription,'articleOkToSell':existsarticle.articleoktosell}
          if not returnarticle == {}:
            returnlist.append(returnarticle)
        result = json.dumps({'category':returnlist})
      except:
        result = json.dumps({'errorcode': 10}) # Error code 10: No article matched filter.
    except:
      result = json.dumps({'errorcode':1}) # Error code 1: Article already exists or no json data
    self.response.write(result)

class SendEmail(BaseHandler):
  @user_required
  def post(self):
    try:
      user = self.user
      logging.info("User is: " + str(user))
      email = user.email_address
      logging.info("User email: " + email)
      itemName = self.request.get('itemname')
      logging.info("Got itemname")
      present_query = myArticle.query(myArticle.articlename == itemName)
      logging.info('Created query')
      existsitem = None
      try:
        existsitem = present_query.get()
        logging.info("Query returned: " + str(existsitem))
      except:
        logging.info("Found no item by that name")
      logging.info("send email request info" + str(self.request))
      emailTargetAddress = existsitem.articleowner
      logging.info("Got article owner")
      emailSenderAddress = "smart.closet.service@gmail.com"
      logging.info("set email address")
      content = "Your received a message from: " + email + "\nThe message is: \n" + self.request.get('message')
      logging.info('set content')

      message = mail.EmailMessage(sender=emailSenderAddress, subject="Smart Closet Item Inquiry: " + itemName)

      if not mail.is_email_valid(emailTargetAddress):
        logging.info("The email is not valid.")
        self.response.out.write("Email address is not valid.")

      message.to = emailTargetAddress
      message.body = """%s""" %(content)
      message.send()
      self.display_message("Message successfully sent.")
    except:
      self.display_message("Unable to contact seller at this time or item is no longer available.")

class EmailPage(BaseHandler):
  @user_required
  def post(self):
    logging.info("Request is: " + str(self.request))
    data = self.request.get('itemName')
    logging.info('Json data sent to this function: ' + str(data))
    params = {'itemname': str(data)}
    teststring = self.render_template2('email.html', params)
    logging.info("Test string is: " + str(teststring))
    result = json.dumps({'htmlVal': teststring})
    self.response.write(result)

class SearchArticles(webapp2.RequestHandler):

    def testfunction(self,msg):
      try:
        logging.info('calling reduce by email in string search: ' + str(email) + 'and query results: ' + str(allarticlesbyused))
        templist = list()
        if type(email) == list:
          if len(email) > 0 :
            logging.info('Email list is greater than 0')
            for thisemail in email:
              logging.info('looking for email: ' + str(thisemail))
              for filteredarticle in allarticlesbyused:
                logging.info('article compare email: ' + str(filteredarticle.articleowner))
                if filteredarticle.articleowner == thisemail:
                  templist.append(filteredarticle)
            allarticlesbyused = templist
          else:
            logging.info('Count is zero')
        else:
          logging.info('email type is str')
          if not email == "":               
            for filteredarticle in allarticlesbyused:
              if filteredarticle.articleowner == email:
                templist.append(filteredarticle)
                logging.info("found an email match")
            allarticlesbyused = templist
          else:
            logging.info('Email is empty string')
        logging.info('all articles by used after email filter: ' + str(allarticlesbyused))
      except:
        logging.info('didnt get an email')

    def post(self):
      payload = {}
      data = None
      self.testfunction("this is a test")
      searchFilter = None
      filterType = None
      try:
        logging.info(str(self.request))
        try:
          data = json.loads(self.request.body)
          logging.info('This is what Im looking for: ' + str(data))
          searchFilter = data['filterString'].lower()
        except:
          searchFilter = self.request.get('filterString')
        logging.info('Filter: ' + str(searchFilter))
        email = ""
        try:
          email = data['email']       
        except:
          logging.info('didnt get email')
        try:  
          filterType = data['filterType']
        except:
          filterType = self.request.get('filterType')
        if filterType == 'string':
          logging.info('The filter type is string')
          allarticle_query = myArticle.query().order(myArticle.articletimesused)
          allarticlesbyused = allarticle_query.fetch()
          try:
            logging.info('calling reduce by email in string search: ' + str(email) + 'and query results: ' + str(allarticlesbyused))
            templist = list()
            if type(email) == list:
              if len(email) > 0 :
                logging.info('Email list is greater than 0')
                for thisemail in email:
                  logging.info('looking for email: ' + str(thisemail))
                  for filteredarticle in allarticlesbyused:
                    logging.info('article compare email: ' + str(filteredarticle.articleowner))
                    if filteredarticle.articleowner == thisemail:
                      templist.append(filteredarticle)
                allarticlesbyused = templist
              else:
                logging.info('Count is zero')
            else:
              logging.info('email type is str')
              if not email == "":               
                for filteredarticle in allarticlesbyused:
                  if filteredarticle.articleowner == email:
                    templist.append(filteredarticle)
                    logging.info("found an email match")
                allarticlesbyused = templist
              else:
                logging.info('Email is empty string')
            logging.info('all articles by used after email filter: ' + str(allarticlesbyused))
          except:
            logging.info('didnt get an email')
          searchResultArticles = {}
          searchResultList = list()
          for searchArticle in allarticlesbyused:
            articletype = searchArticle.articletype.lower()
            articlename = searchArticle.articlename.lower()
            logging.info("Type is: " + str(articletype) + " and name is: " + str(articlename))
            if not searchFilter == "":
              if searchFilter in articletype:
                searchResultArticles[searchArticle.articlename] = searchArticle
              if searchFilter in articlename:
                searchResultArticles[searchArticle.articlename] = searchArticle
              for thistag in searchArticle.articletags:
                lowertag = thistag.lower()
                if searchFilter in lowertag:
                  searchResultArticles[searchArticle.articlename] = searchArticle
            else:
              logging.info('search filter is null')

        elif filterType == 'usagefilter':
          searchdate = datetime.datetime.strptime(searchFilter, "%Y-%m-%d").date()
          logging.info('The usage filter searchdate is: ' + str(searchdate))
          allarticle_query = myArticle.query().order(myArticle.articletimesused)
          allarticlesbyused = allarticle_query.fetch()
          logging.info("Query results in ok to sell: " + str(allarticlesbyused))
          try:
            logging.info('calling reduce by email in string search: ' + str(email) + 'and query results: ' + str(allarticlesbyused))
            templist = list()
            if type(email) == list:
              if len(email) > 0 :
                logging.info('Email list is greater than 0')
                for thisemail in email:
                  for filteredarticle in allarticlesbyused:
                    if filteredarticle.articleowner == thisemail:
                      templist.append(filteredarticle)
                      logging.info('found a list match')
                allarticlesbyused = templist
              else:
                logging.info('Count is zero')
            else:
              logging.info('email type is str')
              if not email == "":               
                for filteredarticle in allarticlesbyused:
                  if filteredarticle.articleowner == email:
                    templist.append(filteredarticle)
                    logging.info("found an email match")
                allarticlesbyused = templist
              else:
                logging.info('Email is empty string')
          except:
            logging.info('didnt get an email')
          searchResultArticles = {}
          searchResultList = list()

          for searchArticle in allarticlesbyused:
            if not searchFilter == "":
              lastusedlist = searchArticle.articlelastused
              logging.info('last used list is: ' + str(lastusedlist))
              recentusefound = False
              for useddate in lastusedlist:
                logging.info("This use date is: " + str(useddate))
                articledate = datetime.datetime.strptime(str(useddate), "%Y-%m-%d").date()
                logging.info('changed to date: ' + str(articledate))
                logging.info('searchdate is: ' + str(searchdate))
                if articledate > searchdate:
                  logging.info("Found an article greater than search date")
                  recentusefound = True
                else:
                  logging.info('article not used recent enought')
              if not recentusefound:
                searchResultArticles[searchArticle.articlename] = searchArticle

        elif filterType == 'neverused':
          logging.info('The filter is neverused')  
          allarticle_query = myArticle.query().order(myArticle.articletimesused)
          allarticlesbyused = allarticle_query.fetch()
          try:
            logging.info('calling reduce by email in string search: ' + str(email) + 'and query results: ' + str(allarticlesbyused))
            templist = list()
            if type(email) == list:
              logging.info('email type is list')
              if len(email) > 0 :
                logging.info('Email list is greater than 0')
                for thisemail in email:
                  for filteredarticle in allarticlesbyused:
                    if filteredarticle.articleowner == thisemail:
                      templist.append(filteredarticle)
                      logging.info('found a list match')
                allarticlesbyused = templist
              else:
                logging.info('Count is zero')
            else:
              logging.info('email type is str')
              if not email == "":               
                for filteredarticle in allarticlesbyused:
                  if filteredarticle.articleowner == email:
                    templist.append(filteredarticle)
                    logging.info("found an email match")
                allarticlesbyused = templist
              else:
                logging.info('Email is empty string')
          except:
            logging.info('didnt get an email')
          searchResultArticles = {}
          searchResultList = list()
          for searchArticle in allarticlesbyused:
            timesused = str(searchArticle.articletimesused)
            if searchFilter == "true":
              if timesused == "0":
                searchResultArticles[searchArticle.articlename] = searchArticle
                logging.info('found an item neverused.')
            elif searchFilter == "":
              pass
            else:
              if timesused == "0":
                logging.info("timesued is zeron")
              elif timesused == None:
                pass
              else:
                searchResultArticles[searchArticle.articlename] = searchArticle
                logging.info('found an article used at least once.')

        elif filterType == 'oktosell':
          logging.info('The filter is oktosell')  
          allarticle_query = myArticle.query().order(myArticle.articletimesused)
          allarticlesbyused = allarticle_query.fetch()
          try:
            logging.info('calling reduce by email in string search: ' + str(email) + 'and query results: ' + str(allarticlesbyused))
            templist = list()
            if type(email) == list:
              logging.info('email type is list')
              if len(email) > 0 :
                logging.info('Email list is greater than 0')
                for thisemail in email:
                  for filteredarticle in allarticlesbyused:
                    if filteredarticle.articleowner == thisemail:
                      templist.append(filteredarticle)
                      logging.info('found a list match')
                  allarticlesbyused = templist
              else:
                logging.info('Count is zero')
            else:
              logging.info('email type is str')
              if not email == "":               
                for filteredarticle in allarticlesbyused:
                  if filteredarticle.articleowner == email:
                    templist.append(filteredarticle)
                    logging.info("found an email match")
                allarticlesbyused = templist
              else:
                logging.info('Email is empty string')
          except:
            logging.info('didnt get an email')
          searchResultArticles = {}
          searchResultList = list()

          for searchArticle in allarticlesbyused:
            oktosell = str(searchArticle.articleoktosell)
            oktosell = oktosell.lower()
            if oktosell == searchFilter:
              searchResultArticles[searchArticle.articlename] = searchArticle
              logging.info('found an item ok to sell.')

        logging.info("searchResultArticles" + str(searchResultArticles))    
        for thisArticle in searchResultArticles:
          existsarticle = searchResultArticles[thisArticle]
          logging.info("Adding to list article: " + str(existsarticle))
          appendArticle = {'articleName':existsarticle.articlename,'articleOwner':existsarticle.articleowner,'articleId':existsarticle.articleid,'articleType':existsarticle.articletype,'articleImageUrl':existsarticle.articleimageurl,'articleLastUsed':existsarticle.articlelastused,'articleTimesUsed':existsarticle.articletimesused,'articleTags':existsarticle.articletags,'articlePrice':existsarticle.articleprice,'articleDescription':existsarticle.articledescription,'articleOkToSell':existsarticle.articleoktosell}
          logging.info('created append article ' + str(appendArticle))
          searchResultList.append(appendArticle)

        payload = {'articleList':searchResultList}
        logging.info("SearchResultList: " + str(searchResultList))
      except:
        payload = {'errorcode':6}
      result = json.dumps(payload)
      self.response.write(result)

class ConfigureCategories(BaseHandler):
    @user_required
    def get(self):
      webapp2.Route('/ConfigureCategories', ConfigureCategories),
      user = self.user
      logging.info("User is: " + str(user))
      emailfilter = user.email_address
      logging.info("User email: " + emailfilter)
      logging.info('Returning merchandise.')
      allarticle_query = myArticle.query().order(myArticle.articletimesused)
      allarticlesbyused = allarticle_query.fetch()
      mymerch = list()
      try: 
        for thisarticle in allarticlesbyused:
          if thisarticle.articleoktosell == True:
            if thisarticle.articleowner == emailfilter:
              thismerch = {'imageurl':thisarticle.articleimageurl,'productName':thisarticle.articlename,'productDescription':thisarticle.articledescription,'productPrice':thisarticle.articleprice, 'productType':thisarticle.articletype}
              mymerch.append(thismerch)
      except:
        pass
      logging.info("The merch list: " + str(mymerch))
      result = json.dumps({'myMerch': mymerch}) #[{merchandise},{merchandise}]
      logging.info("Result is: " + str(result))
      self.response.write(result)

class GetMerch(webapp2.RequestHandler):
    def get(self):
      logging.info('Returning merchandise.')
      allarticle_query = myArticle.query().order(myArticle.articletimesused)
      allarticlesbyused = allarticle_query.fetch()
      mymerch = list()
      try: 
        for thisarticle in allarticlesbyused:
          if thisarticle.articleoktosell == True:
            thismerch = {'imageurl':thisarticle.articleimageurl,'productName':thisarticle.articlename,'productDescription':thisarticle.articledescription,'productPrice':thisarticle.articleprice, 'productType':thisarticle.articletype}
            mymerch.append(thismerch)
      except:
        pass
      logging.info("The merch list: " + str(mymerch))
      result = json.dumps({'myMerch': mymerch}) #[{merchandise},{merchandise}]
      logging.info("Result is: " + str(result))
      self.response.write(result)

config = {
  'webapp2_extras.auth': {
    'user_model': 'models.User',
    'user_attributes': ['name']
  },
  'webapp2_extras.sessions': {
    'secret_key': 'YOUR_SECRET_KEY'
  }
}

class CreateProfile(webapp2.RequestHandler):
  def post(self):
    try:
      data = json.loads(self.request.body)
      logging.info('Json data sent to this function: ' + str(data))

      user_name = data['username']
      logging.info('user_name: ' + str(user_name))
      email = data['email']
      logging.info('email: ' + str(email))
      name = data['name']
      logging.info('name: ' + str(name))
      password = data['password']
      logging.info('password: ' + str(password))
      last_name = data['lastname']
      logging.info('lastname: ' +str(last_name))
      
      thisUser = smartClosetUser(parent=ndb.Key(STORAGE_ID_GLOBAL, STORAGE_ID_GLOBAL))

      thisUser.userPin = None
      thisUser.userName = name
      thisUser.userEmail = email
      thisUser.userMarkdown = "0.0"
      thisUser.put()
      logging.info('User written to database.')
      result = json.dumps({'errorcode':0})
      logging.info('Create Profile successed with errorcode: ' + str(result))
    except:
      result = json.dumps({'errorcode':1})
      logging.info('Create Profile failed with errorcode: ' + str(result))
    self.response.write(result)


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler, name='home'),
    webapp2.Route('/signup', SignupHandler),
    webapp2.Route('/signup2', SignupHandlerAndroid),
    webapp2.Route('/GetArticleInfo', GetArticleInfo),
    webapp2.Route('/<type:v|p>/<user_id:\d+>-<signup_token:.+>',
      handler=VerificationHandler, name='verification'),
    webapp2.Route('/password', SetPasswordHandler),
    webapp2.Route('/login', LoginHandler, name='login'),
    webapp2.Route('/logout', LogoutHandler, name='logout'),
    webapp2.Route('/forgot', ForgotPasswordHandler, name='forgot'),
    webapp2.Route('/GetAccountSettings', GetAccountSettings),
    webapp2.Route('/authenticated', AuthenticatedHandler, name='authenticated'),
    ('/GetMerch', GetMerch),
    ('/ConfigureAccount', ConfigureAccount),
    ('/CreateArticle', CreateArticle),
    ('/AndroidUploadHandler', AndroidUploadHandler),
    ('/DeleteArticle', DeleteArticle),
    ('/UseArticle', UseArticle),
    ('/UpdateArticle', UpdateArticle),
    ('/ReadArticle', ReadArticle),
    ('/SendEmail', SendEmail),
    ('/GetUsers', GetUsers),
    ('/EmailPage', EmailPage),
    ('/SearchArticles', SearchArticles),
    ('/CreateArticlePage', CreateArticlePage),
    ('/ConfigureCategories', ConfigureCategories),
    ('/GetSaleCategories', GetSaleCategories),
    ('/GetSaleCategories2', GetSaleCategories2),
    ('/GetCategories', GetCategories),
    ('/GetCategory', GetCategory),
    ('/CreateProfile', CreateProfile)
], debug=True, config=config)

logging.getLogger().setLevel(logging.DEBUG)

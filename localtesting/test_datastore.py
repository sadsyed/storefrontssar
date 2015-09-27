import sys
# sys.path.insert(1, 'google-cloud-sdk/platform/google_appengine')
# sys.path.insert(1, 'google-cloud-sdk/platform/google_appengine/lib/yaml/lib')
sys.path.insert(1, '/Applications/GoogleAppEngineLauncher.app/Contents/Resources/GoogleAppEngine-default.bundle/Contents/Resources/google_appengine')
sys.path.insert(1, '/Applications/GoogleAppEngineLauncher.app/Contents/Resources/GoogleAppEngine-default.bundle/Contents/Resources/google_appengine/lib/yaml/lib')
sys.path.insert(1, 'storefrontssar/lib')

import unittest

from google.appengine.api import memcache
from google.appengine.ext import ndb
from google.appengine.ext import testbed

class TestArticleModel(ndb.Model):
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
	articlecolors = ndb.StringProperty(repeated=True)

class TestEntityGroupRoot(ndb.Model):
 	""" Entity group root """
 	pass

def GetEntityViaMemcache(entity_key):
 	""" Get entity from memcache if available, from datastore if not """
 	entity = memcache.get(entity_key)

 	if entity is not None:
 		return entity
 	key = ndb.Key(urlsafe=entity_key)
 	entity = key.get()

 	if entity is not None:
 		memcache.set(entity_key, entity)
 	return entity

class DatastoreTestCase(unittest.TestCase):

 	def setUp(self):
 		# First, create an instance of the Testbed class
 		self.testbed = testbed.Testbed()

 		# Then activate the testbed, which prepares the service stub for use
 		self.testbed.activate()

 		# Next, declare which service stub you want to use
 		self.testbed.init_datastore_v3_stub()
 		self.testbed.init_memcache_stub()

 		# Clear ndb's in-context cache between tests.
 		# This prevents data from leadking between tests.
 		# Alternatively, you could disable caching by using ndb.get_context().seet_cache_policy(False)
 		ndb.get_context().clear_cache()

 	def tearDown(self):
 		self.testbed.deactivate()

 	# def testInsertArticle(self):
 	# 	TestArticleModel().put
 	# 	self.assertEqual(1, len(TestArticleModel.query().fetch(2)))

 	def testCreateArticle(self):
 		entity_key = TestArticleModel(articlename="Test Article").put().urlsafe()

 		retrieved_entity = GetEntityViaMemcache(entity_key)

 		self.assertNotEqual(None, retrieved_entity)
 		self.assertEqual("Test Article", retrieved_entity.articlename)

if __name__ == '__main__':
 	unittest.main()

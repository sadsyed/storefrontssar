import unittest
from google.appengine.api import memcache
from google.appengine.ext import testbed
import webapp2
import webtest
import storefrontssar
import logging
import json

class CreateArticleTest(unittest.TestCase):
	def setUp(self):
		app = webapp2.WSGIApplication([(r'/CreateArticle', storefrontssar.CreateArticle)])
		self.testapp = webtest.TestApp(app)
		self.testbed = testbed.Testbed()
		self.testbed.activate()

	def tearDown(self):
		self.testbed.deactivate()

	def testCreateArticle(self):
		logging.info("Testing CreateArticle")

		self.testbed.init_memcache_stub()

		articleName = 'Article 1'
		articleDescription = 'Test Article 1 Desription'
		articlePrice = '14.00'
		articleOwner = 'sh.sadaf@gmail.com'
		articleType = 'Coats'
		articleTags = 'coattags'

		params = json.dumps({"articleName" : articleName, "articleDescription" : articleDescription, "articleType" : articleType, "articleTags": articleTags, "articlePrice" : articlePrice, "articleOwner" : articleOwner, "articleOkToSell" : True, "articlePrivate": False})
		logging.info("Test Article params are: " + str(params))

		response = self.testapp.post('/CreateArticle', params)
		logging.info("Test response status: " + response.status)
		logging.info("Test response content: " + str(response.normal_body))

		article_exists_failure_result = json.dumps({'returnval':5})
		datastore_failure_result = json.dumps({'returnval':2})
		corred_json_failure_result = json.dumps({'returnval':1})

		assert response.normal_body != article_exists_failure_result
		assert response.normal_body != datastore_failure_result
		assert response.normal_body != corred_json_failure_result 
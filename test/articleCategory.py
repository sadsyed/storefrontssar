import unittest
from google.appengine.api import memcache
from google.appengine.ext import testbed
import webapp2
import webtest
import storefrontssar
import logging
import json

class ArticleTest(unittest.TestCase):

	articleOwner = 'sh.sadaf@gmail.com'
	tokenId = '40560021354-iem950p1ti5ak8t0v2qb52vnk651atuh.apps.googleusercontent.com'
	articlePrice = "40.00"

	def setUp(self):
		app = webapp2.WSGIApplication([
			(r'/CreateArticle', storefrontssar.CreateArticle),
			(r'/GetCategories', storefrontssar.GetCategories),
			(r'/GetCategory', storefrontssar.GetCategory)])
		self.testapp = webtest.TestApp(app)
		self.testbed = testbed.Testbed()
		self.testbed.activate()

	def tearDown(self):
		self.testbed.deactivate()

	def testCreateArticle(self, articleName='Test Article', articleType='Scarves', articleTags='None', articleOkToSell='true'):
		logging.info("Testing CreateArticle")

		self.testbed.init_memcache_stub()

		articleDescription = 'Test Article 1 Desription'

		params = json.dumps({"tokenId": self.tokenId, "articleName" : articleName, "articleDescription" : articleDescription, "articleType" : articleType, "articleTags": articleTags, "articlePrice" : self.articlePrice, "articleOwner" : self.articleOwner, "articleOkToSell" : articleOkToSell, "articlePrivate": False})
		logging.info("Test Article params are: " + str(params))

		response = self.testapp.post('/CreateArticle', params)
		logging.info("Test response status: " + response.status)

		responseContent = json.loads(response.normal_body)
		logging.info("Test response content: " + str(responseContent))

		articleUuid = responseContent['returnval']
		logging.info("Test articleUuid: " + str(articleUuid))


		article_exists_failure_result = json.dumps({'returnval':5})
		datastore_failure_result = json.dumps({'returnval':2})
		corred_json_failure_result = json.dumps({'returnval':1})

		assert response.normal_body != article_exists_failure_result
		assert response.normal_body != datastore_failure_result
		assert response.normal_body != corred_json_failure_result 

		return articleUuid

	#1 - get all categories
	def testGetCategories(self):
		logging.info("Testing GetCategories")

		self.testbed.init_memcache_stub()

		article1Uuid = self.testCreateArticle('Article One', articleType="Scarves")
		article2Uuid = self.testCreateArticle('Article Two', articleType="Coats")
		article3Uuid = self.testCreateArticle('Article Three', articleType="Sweaters")

		# REQUEST
		# {  
		#    "emailFilter":"derezzed.titanium@gmail.com",
		#    "tokenId":"ya29.JgLbeQa3Nygq_C8GNN0Uh0UJhXXEqGvZuvXp9GFB-fOQMxZj1Uo5XQC8a2LzSdIyOOPwx8U"
		# }

		params = json.dumps({"tokenId": self.tokenId, "emailFilter": self.articleOwner})
		logging.info("Test GetCategories params are: " + str(params))

		response = self.testapp.post('/GetCategories', params)
		logging.info("Test GetCategories response status: " + response.status)

		# RESPONSE
		# {  
		#    "currentCategories":[  
		#       {  
		#          "lastUsedArticleImageUrl":"http://lh3.googleusercontent.com/bZXNgSbapAmb9BH9j78Z1BdXolLXOOvSuQxDuknLWrTGNe478UT6htNHb9_WpbbpZPUfRKG4VsZ-RE8ejM73F9BYNpImzio",
		#          "name":"Scarves"
		#       },
		#       {  
		#          "lastUsedArticleImageUrl":"http://lh3.googleusercontent.com/-MvZPfFYBJ82hzmJ511Pn5L2u4mOYYuroACK2gxCQxYZzUA-7oVHjZtakFVS4dhqEXA0Fv4KP4pQQ2UIQohTZw0jn5wou1E",
		#          "name":"Coats"
		#       },
		#       {  
		#          "lastUsedArticleImageUrl":"https://lh3.googleusercontent.com/s2i729v52OqpoABV3X9mqlwbx9Dr7rW146lUZqGdosePDL9hQTiknVEiZXGhmYyfwPuVwTBa9dv4FxZiRn2CklXLYdswtIr2",
		#          "name":"Sweaters"
		#       },
		#       {  
		#          "lastUsedArticleImageUrl":"http://lh3.googleusercontent.com/iY_rUdRNrv6yz5_F2XADecz7asoiW4Gnzs7VVWTMQfBTMMs0nxMbqGidCXBUYHKQievUt5qrkrhj_rhy9DnIV9cEo-YmqzHn",
		#          "name":"Shirts"
		#       }
		#    ]
		# }
		responseContent = json.loads(response.normal_body)
		logging.info("Test GetCategories response body: " + str(responseContent)) 

		categoryList = responseContent['currentCategories']
		self.assertFalse(len(categoryList)==0, "No categories found")

		logging.info("Test GetCategories articleList: " + str(categoryList))
		self.assertEqual(len(categoryList), 3, "Number of articles returned is not 3.")

		# for article in articleList:
		# 	logging.info("Test GetCategories articleName: " + str(article['articleName']))

		# 	self.assertEqual(article['articleOwner'], self.articleOwner, "Article returned is not owned by: " + str(self.articleOwner))

	#2 - get one category
	def testGetCategory(self):
		logging.info("Testing GetCategory")

		self.testbed.init_memcache_stub()

		article1Uuid = self.testCreateArticle('Article One', articleType="Scarves")
		article2Uuid = self.testCreateArticle('Article Two', articleType="Coats")
		article3Uuid = self.testCreateArticle('Article Three', articleType="Sweaters")
		article4Uuid = self.testCreateArticle('Article Four', articleType="Sweaters")

		# REQUEST
		# {  
		#    "category":"Scarves",
		#    "emailFilter":"derezzed.titanium@gmail.com",
		#    "tokenId":"ya29.JgLbeQa3Nygq_C8GNN0Uh0UJhXXEqGvZuvXp9GFB-fOQMxZj1Uo5XQC8a2LzSdIyOOPwx8U"
		# }

		params = json.dumps({"category": "Sweaters", "tokenId": self.tokenId, "emailFilter": self.articleOwner})
		logging.info("Test GetCategory params are: " + str(params))

		response = self.testapp.post('/GetCategory', params)
		logging.info("Test GetCategory response status: " + response.status)

		# RESPONSE
		# {  
		#    "category":[  
		#       {  
		#          "articleName":"Zigzag1506",
		#          "articleLastUsed":[  

		#          ],
		#          "articleColors":[  
		#             "white"
		#          ],
		#          "articlePrice":69.0,
		#          "articleDescription":"Zigzag",
		#          "articlePrivate":false,
		#          "articleId":"60e3f83d-6f8a-11e5-8663-f9af05023910",
		#          "articleTimesUsed":0,
		#          "articleImageUrl":"http://lh3.googleusercontent.com/tTuQBTB8MQtFcCaBcFw1TgsnVgP8CQTGJXi7QaZRLRi7U7v-UPajlYzIJszxTymwglyJEfWLNOgmG8hzoQJrpUgcB2Y3pVCucA",
		#          "articleOkToSell":false,
		#          "articleTags":[  
		#             "Zigzag "
		#          ],
		#          "articleOwner":"derezzed.titanium@gmail.com",
		#          "articleType":"Scarves"
		#       },
		#       {  
		#          "articleName":"Scarf 2341",
		#          "articleLastUsed":[  

		#          ],
		#          "articleColors":[  
		#             "white"
		#          ],
		#          "articlePrice":50.0,
		#          "articleDescription":"Scarf ",
		#          "articlePrivate":false,
		#          "articleId":"95d8a870-5451-11e5-baa0-373a21fd1710",
		#          "articleTimesUsed":0,
		#          "articleImageUrl":"http://lh3.googleusercontent.com/PyU095MAf5sMppZP2gIsDz9zZL51IySkTm720EGr7xpHjIjo-hrLMzQJYuKSMxKjAAQ6mtsHaLwx7WMba8X7qeuOej9dhzc0",
		#          "articleOkToSell":true,
		#          "articleTags":[  
		#             "Scarf"
		#          ],
		#          "articleOwner":"derezzed.titanium@gmail.com",
		#          "articleType":"Scarves"
		#       }
		#    ]
		# }

		responseContent = json.loads(response.normal_body)
		logging.info("Test GetCategory response body: " + str(responseContent)) 

		articleList = responseContent['category']
		self.assertFalse(len(articleList)==0, "No articles found for this catgeory")

		logging.info("Test GetCategory articleList: " + str(articleList))
		self.assertEqual(len(articleList), 2, "Number of articles returned is not 2.")


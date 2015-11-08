# import unittest
# from google.appengine.api import memcache
# from google.appengine.ext import testbed
# import webapp2
# import webtest
# import storefrontssar
# import logging
# import json

# class ArticleTest(unittest.TestCase):

# 	articleOwner = 'sh.sadaf@gmail.com'
# 	tokenId = '40560021354-iem950p1ti5ak8t0v2qb52vnk651atuh.apps.googleusercontent.com'
# 	articlePrice = "40.00"

# 	def setUp(self):
# 		app = webapp2.WSGIApplication([
# 			(r'/CreateArticle', storefrontssar.CreateArticle),
# 			(r'/SearchArticles', storefrontssar.SearchArticles),
# 			(r'/UseArticle', storefrontssar.UseArticle)])
# 		self.testapp = webtest.TestApp(app)
# 		self.testbed = testbed.Testbed()
# 		self.testbed.activate()

# 	def tearDown(self):
# 		self.testbed.deactivate()

# 	def testCreateArticle(self, articleName='Test Article', articleType='Scarves', articleTags='None', articleOkToSell='true'):
# 		logging.info("Testing CreateArticle")

# 		self.testbed.init_memcache_stub()

# 		articleDescription = 'Test Article 1 Desription'

# 		params = json.dumps({"tokenId": self.tokenId, "articleName" : articleName, "articleDescription" : articleDescription, "articleType" : articleType, "articleTags": articleTags, "articlePrice" : self.articlePrice, "articleOwner" : self.articleOwner, "articleOkToSell" : articleOkToSell, "articlePrivate": False})
# 		logging.info("Test Article params are: " + str(params))

# 		response = self.testapp.post('/CreateArticle', params)
# 		logging.info("Test response status: " + response.status)

# 		responseContent = json.loads(response.normal_body)
# 		logging.info("Test response content: " + str(responseContent))

# 		articleUuid = responseContent['returnval']
# 		logging.info("Test articleUuid: " + str(articleUuid))


# 		article_exists_failure_result = json.dumps({'returnval':5})
# 		datastore_failure_result = json.dumps({'returnval':2})
# 		corred_json_failure_result = json.dumps({'returnval':1})

# 		assert response.normal_body != article_exists_failure_result
# 		assert response.normal_body != datastore_failure_result
# 		assert response.normal_body != corred_json_failure_result 

# 		return articleUuid

# 	def testUseArticle(self, articleUuid=0):
# 		logging.info("Testing UseArticle")

# 		self.testbed.init_memcache_stub()

# 		if (articleUuid == 0):
# 			articleUuid = self.testCreateArticle();

# 		#tokenId = '40560021354-iem950p1ti5ak8t0v2qb52vnk651atuh.apps.googleusercontent.com'

# 		# REQUEST JSON
# 		# {  
# 		#    "articleId":"5bc228ae-7a16-11e5-8a06-a7d66fd2a274",
# 		#    "email":"derezzed.titanium@gmail.com",
# 		#    "tokenId":"ya29.IQIsnZOgpf534jJsNWiTlJDTyJPONXN97WGCTXL8gdtmsX-72ZqOaoHLen4Cg20S7RbCyVE"
# 		# }

# 		# use article created above
# 		params = json.dumps({"tokenId": self.tokenId, "articleId": articleUuid, "email": self.articleOwner})
# 		logging.info("Test UseArticle params are: " + str(params))

# 		response = self.testapp.post('/UseArticle', params)
# 		logging.info("Test UseArticle response status: " + response.status)

# 		responseContent = json.loads(response.normal_body)
# 		logging.info("Test UseArticle response body: " + str(responseContent)) 

# 		errorcode = responseContent['errorcode']

# 		self.assertEqual(errorcode, 0)
# 		self.assertFalse(errorcode==8, "Error code 8: unable to update uses for article")
# 		self.assertFalse(errorcode==-2, "Error code -2: invalid token")
# 		self.assertFalse(errorcode==1, "Error code1: Article already exists or no json data")

# 	#1 - serach all article that have never been used
# 	def testSearchNeverUsed(self):
# 		logging.info("Testing SearchNeverUsed")

# 		self.testbed.init_memcache_stub()

# 		article1Uuid = self.testCreateArticle('Article One')
# 		article2Uuid = self.testCreateArticle('Article Two')

# 		# REQUEST
# 		# {  
# 		#    "email":"derezzed.titanium@gmail.com",
# 		#    "filterType":"neverused",
# 		#    "filterString":"true",
# 		#    "tokenId":"ya29.JgJ1yfaP_B5shr9tOCqIFO6GMvrDDkRENTU0EslpZkhqhB4KkxBlcjeGBEUgw9xdPijFcYw"
# 		# }

# 		articleidstodelete = [article1Uuid, article2Uuid]
# 		# update article colors
# 		params = json.dumps({"tokenId": self.tokenId, "email": self.articleOwner, "filterType": "neverused", "filterString": "true"})
# 		logging.info("Test SearchNeverUsed params are: " + str(params))

# 		response = self.testapp.post('/SearchArticles', params)
# 		logging.info("Test SearchNeverUsed response status: " + response.status)

# 		# RESPONSE
# 		# {  
# 		#    "articleList" : [{"articleName": "Article One", "articleTimesUsed": 0, .....}
# 		#					  {"articleName": "Article Two", "articleTimesUsed": 0, .....}]
# 		# }

# 		responseContent = json.loads(response.normal_body)
# 		logging.info("Test SearchNeverUsed response body: " + str(responseContent)) 

# 		articleList = responseContent['articleList']
# 		logging.info("Test SearchNeverUsed articleList: " + str(articleList))
# 		self.assertEqual(len(articleList), 2, "Number of articles returned is not 2.")

# 		for article in articleList:
# 			logging.info("Test SearchNeverUsed articleName: " + str(article['articleName']))

# 			self.assertEqual(article['articleOwner'], self.articleOwner, "Article returned is not owned by: " + str(self.articleOwner))
# 			self.assertEqual(article['articleTimesUsed'], 0, "Article has been used")

# 	#2 - search all article that have been used 
# 	def testSearchUsed(self):
# 		logging.info("Testing SearchUsed")

# 		self.testbed.init_memcache_stub()

# 		article1Uuid = self.testCreateArticle('Article One')
# 		self.testUseArticle(article1Uuid)
# 		self.testUseArticle(article1Uuid)
# 		article2Uuid = self.testCreateArticle('Article Two')
# 		self.testUseArticle(article2Uuid)
# 		self.testUseArticle(article2Uuid)
# 		self.testUseArticle(article2Uuid)

# 		# REQUEST
# 		# {  
# 		#    "email":"derezzed.titanium@gmail.com",
# 		#    "filterType":"neverused",
# 		#    "filterString":"false",
# 		#    "tokenId":"ya29.JgJ1yfaP_B5shr9tOCqIFO6GMvrDDkRENTU0EslpZkhqhB4KkxBlcjeGBEUgw9xdPijFcYw"
# 		# }

# 		articleidstodelete = [article1Uuid, article2Uuid]
# 		# update article colors
# 		params = json.dumps({"tokenId": self.tokenId, "email": self.articleOwner, "filterType": "neverused", "filterString": "false"})
# 		logging.info("Test SearchUsed params are: " + str(params))

# 		response = self.testapp.post('/SearchArticles', params)
# 		logging.info("Test SearchUsed response status: " + response.status)

# 		# RESPONSE
# 		# {  
# 		#    "articleList" : [{"articleName": "Article One", "articleTimesUsed": 0, .....}
# 		#					  {"articleName": "Article Two", "articleTimesUsed": 0, .....}]
# 		# }

# 		responseContent = json.loads(response.normal_body)
# 		logging.info("Test SearchUsed response body: " + str(responseContent)) 

# 		articleList = responseContent['articleList']
# 		logging.info("Test SearchUsed articleList: " + str(articleList))
# 		logging.info("Test SearchUsed articles returned: " + str(len(articleList)))
# 		self.assertEqual(len(articleList), 2, "Number of articles returned is not 2.")

# 		for article in articleList:
# 			logging.info("Test SearchUsed articleName: " + str(article['articleName']))

# 			self.assertEqual(article['articleOwner'], self.articleOwner, "Article returned is not owned by: " + str(self.articleOwner))

# 			if (article['articleId'] == article1Uuid):
# 				self.assertEqual(article['articleTimesUsed'], 2)
# 			else:
# 				self.assertEqual(article['articleTimesUsed'], 3)

# 	#3 - search all articles with string type
# 	def testSearchString(self):
# 		logging.info("Testing SearchString")

# 		self.testbed.init_memcache_stub()

# 		article1Type = 'Coats'
# 		article1Uuid = self.testCreateArticle('Article One', article1Type)
# 		article2Type = 'Dresses'
# 		articleTags = 'Coat, Jacket'
# 		article2Uuid = self.testCreateArticle('Article Two', article2Type, articleTags)

# 		# REQUEST
# 		# {  
# 		#    "tokenId":"ya29.JgLv3T1D5NPtPFhFH8uB6agShJdYdtFjPqB_6EF7JkD1xs_7N8G27pBgMUAG8jbsZCWKXaQ",
# 		#    "filterType":"string",
# 		#    "filterString":"Coat",
# 		#    "email":"derezzed.titanium@gmail.com"
# 		# }

# 		articleidstodelete = [article1Uuid, article2Uuid]
# 		# update article colors
# 		params = json.dumps({"tokenId": self.tokenId, "email": self.articleOwner, "filterType": "string", "filterString": "Coat"})
# 		logging.info("Test SearchString params are: " + str(params))

# 		response = self.testapp.post('/SearchArticles', params)
# 		logging.info("Test SearchString response status: " + response.status)

# 		# RESPONSE
# 		# {  
# 		#    "articleList" : [{"articleName": "Article One", "articleTimesUsed": 0, .....}
# 		#					  {"articleName": "Article Two", "articleTimesUsed": 0, .....}]
# 		# }

# 		responseContent = json.loads(response.normal_body)
# 		logging.info("Test SearchString response body: " + str(responseContent)) 

# 		articleList = responseContent['articleList']
# 		logging.info("Test SearchString articleList: " + str(articleList))
# 		logging.info("Test SearchString articles returned: " + str(len(articleList)))
# 		self.assertEqual(len(articleList), 2, "Number of articles returned is not 2.")

# 		for article in articleList:
# 			logging.info("Test SearchString articleName: " + str(article['articleName']))

# 			self.assertEqual(article['articleOwner'], self.articleOwner, "Article returned is not owned by: " + str(self.articleOwner))

# 			if (article['articleId'] == article1Uuid):
# 				self.assertEqual(article['articleType'], article1Type)
# 			else:
# 				self.assertEqual(article['articleType'], article2Type)
# 				articleTagsReturned = article['articleTags']
# 				logging.info("Test SearchString article tags returned: " + str(articleTagsReturned))

# 	#4 - search all article that are OkToSell
# 	def testSearchOkToSell(self):
# 		logging.info("Testing SearchOkToSell")

# 		self.testbed.init_memcache_stub()

# 		article1Uuid = self.testCreateArticle('Article One', articleOkToSell='true')
# 		article2Uuid = self.testCreateArticle('Article Two', articleOkToSell='true')
# 		article3Uuid = self.testCreateArticle('Article Three', articleOkToSell='false')

# 		# REQUEST
# 		# {  
# 		#    "tokenId":"ya29.JgLv3T1D5NPtPFhFH8uB6agShJdYdtFjPqB_6EF7JkD1xs_7N8G27pBgMUAG8jbsZCWKXaQ",
# 		#    "filterType":"oktosell",
# 		#    "filterString":"false",
# 		#    "email":"derezzed.titanium@gmail.com"
# 		# }

# 		params = json.dumps({"tokenId": self.tokenId, "email": self.articleOwner, "filterType": "oktosell", "filterString": "true"})
# 		logging.info("Test SearchOkToSell params are: " + str(params))

# 		response = self.testapp.post('/SearchArticles', params)
# 		logging.info("Test SearchOkToSell response status: " + response.status)

# 		# RESPONSE
# 		# {  
# 		#    "articleList" : [{"articleName": "Article One", "articleTimesUsed": 0, .....}
# 		#					  {"articleName": "Article Two", "articleTimesUsed": 0, .....}]
# 		# }

# 		responseContent = json.loads(response.normal_body)
# 		logging.info("Test SearchOkToSell response body: " + str(responseContent)) 

# 		articleList = responseContent['articleList']
# 		logging.info("Test SearchOkToSell articleList: " + str(articleList))
# 		self.assertEqual(len(articleList), 2, "Number of articles returned is not 2.")

# 		for article in articleList:
# 			logging.info("Test SearchOkToSell articleName: " + str(article['articleName']))

# 			self.assertEqual(article['articleOwner'], self.articleOwner, "Article returned is not owned by: " + str(self.articleOwner))

# 	#5 - search all article that are not OkToSell
# 	def testSearchNotOkToSell(self):
# 		logging.info("Testing SearchNotOkToSell")

# 		self.testbed.init_memcache_stub()

# 		article1Uuid = self.testCreateArticle('Article One', articleOkToSell='true')
# 		article2Uuid = self.testCreateArticle('Article Two', articleOkToSell='true')
# 		article3Uuid = self.testCreateArticle('Article Three', articleOkToSell='false')

# 		# REQUEST
# 		# {  
# 		#    "tokenId":"ya29.JgLv3T1D5NPtPFhFH8uB6agShJdYdtFjPqB_6EF7JkD1xs_7N8G27pBgMUAG8jbsZCWKXaQ",
# 		#    "filterType":"oktosell",
# 		#    "filterString":"false",
# 		#    "email":"derezzed.titanium@gmail.com"
# 		# }

# 		params = json.dumps({"tokenId": self.tokenId, "email": self.articleOwner, "filterType": "oktosell", "filterString": "false"})
# 		logging.info("Test SearchNotOkToSell params are: " + str(params))

# 		response = self.testapp.post('/SearchArticles', params)
# 		logging.info("Test SearchNotOkToSell response status: " + response.status)

# 		# RESPONSE
# 		# {  
# 		#    "articleList" : [{"articleName": "Article One", "articleTimesUsed": 0, .....}
# 		#					  {"articleName": "Article Two", "articleTimesUsed": 0, .....}]
# 		# }

# 		responseContent = json.loads(response.normal_body)
# 		logging.info("Test SearchNotOkToSell response body: " + str(responseContent)) 

# 		articleList = responseContent['articleList']
# 		logging.info("Test SearchNotOkToSell articleList: " + str(articleList))
# 		self.assertEqual(len(articleList), 1, "Number of articles returned is not 1.")

# 		for article in articleList:
# 			logging.info("Test SearchNotOkToSell articleName: " + str(article['articleName']))

# 			self.assertEqual(article['articleOwner'], self.articleOwner, "Article returned is not owned by: " + str(self.articleOwner))

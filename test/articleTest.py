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
# 	articleType = 'Coats'
# 	articlePrice = "40.00"

# 	def setUp(self):
# 		app = webapp2.WSGIApplication([
# 			(r'/CreateArticle', storefrontssar.CreateArticle),
# 			(r'/ReadArticle', storefrontssar.ReadArticle),
# 			(r'/UseArticle', storefrontssar.UseArticle),
# 			(r'/UpdateArticle', storefrontssar.UpdateArticle),
# 			(r'/DeleteArticle', storefrontssar.DeleteArticle)])
# 		self.testapp = webtest.TestApp(app)
# 		self.testbed = testbed.Testbed()
# 		self.testbed.activate()

# 	def tearDown(self):
# 		self.testbed.deactivate()

# 	def testCreateArticle(self, articleName='Test Article'):
# 		logging.info("Testing CreateArticle")

# 		self.testbed.init_memcache_stub()

# 		#articleName = 'Article 1'
# 		articleDescription = 'Test Article 1 Desription'
# 		# articlePrice = '14.00'
# 		# articleOwner = 'sh.sadaf@gmail.com'
# 		# articleType = 'Coats'
# 		articleTags = 'coattags'

# 		params = json.dumps({"tokenId": self.tokenId, "articleName" : articleName, "articleDescription" : articleDescription, "articleType" : self.articleType, "articleTags": articleTags, "articlePrice" : self.articlePrice, "articleOwner" : self.articleOwner, "articleOkToSell" : True, "articlePrivate": False})
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

# 	def testReadArticle(self):
# 		logging.info("Testing ReadArticle")

# 		self.testbed.init_memcache_stub()

# 		#create a new article 
# 		# createArticle = createArticleTest.CreateArticleTest()
# 		# articleUuid = createArticle.testCreateArticle()
# 		# articleUuid = CreateArticleTest('testCreateArticle').testCreateArticle();

# 		articleUuid = self.testCreateArticle();

# 		#first create an article
# 		# articleName = 'ReadArticle'
# 		# articleDescription = 'Test Article 1 Desription'
# 		# articlePrice = '14.00'
# 		# articleOwner = 'sh.sadaf@gmail.com'
# 		# articleType = 'Coats'
# 		# articleTags = 'coattags'
# 		#tokenId = '40560021354-iem950p1ti5ak8t0v2qb52vnk651atuh.apps.googleusercontent.com'

# 		# params = json.dumps({"tokenId": tokenId, "articleName" : articleName, "articleDescription" : articleDescription, "articleType" : articleType, "articleTags": articleTags, "articlePrice" : articlePrice, "articleOwner" : articleOwner, "articleOkToSell" : True, "articlePrivate": False})
# 		# logging.info("Test Article params are: " + str(params))

# 		# response = self.testapp.post('/CreateArticle', params)
# 		# logging.info("Test response status: " + response.status)

# 		# responseContent = json.loads(response.normal_body)
# 		# logging.info("Test response content: " + str(responseContent))

# 		# articleUuid = responseContent['returnval']
# 		# logging.info("Test articleUuid: " + str(articleUuid))

# 		# article_exists_failure_result = json.dumps({'returnval':5})
# 		# datastore_failure_result = json.dumps({'returnval':2})
# 		# corred_json_failure_result = json.dumps({'returnval':1})

# 		# assert response.normal_body != article_exists_failure_result
# 		# assert response.normal_body != datastore_failure_result
# 		# assert response.normal_body != corred_json_failure_result 

# 		#articleUuid = '5b769f1e-84eb-11e5-b905-1367c65781a5'

# 		# read article created above
# 		params = json.dumps({"tokenId": self.tokenId, "articleId": articleUuid})
# 		logging.info("Test ReadArticle params are: " + str(params))

# 		response = self.testapp.post('/ReadArticle', params)
# 		logging.info("Test ReadArticle response status: " + response.status)

# 		responseContent = json.loads(response.normal_body)
# 		logging.info("Test ReadArticle response body: " + str(responseContent)) 

# 		self.assertEqual(articleUuid, responseContent['articleId'])
# 		#self.assertEqual(articleName, responseContent['articleName'])

# 	def testUseArticle(self):
# 		logging.info("Testing UseArticle")

# 		self.testbed.init_memcache_stub()

# 		articleUuid = self.testCreateArticle();

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
		
# 	def testUpdateColors(self):
# 		logging.info("Testing UpdateColors")

# 		self.testbed.init_memcache_stub()

# 		articleUuid = self.testCreateArticle();

# 		# REQUEST
# 		# {  
# 		#    "articleTags":"Scarf",
# 		#    "articleColors":"White,  red, black, gray",
# 		#    "articleId":"51b6a314-5455-11e5-b105-373a21fd1710",
# 		#    "append":"false",
# 		#    "tokenId":"ya29.HgImnIyMz6YrI856Bkq1DPFtZUcuhOwrgRKFenxc4CvbZZirBo9hNDeuz6Vg_wmUxaluew"
# 		# }

# 		# update article colors
# 		params = json.dumps({"tokenId": self.tokenId, "articleColors": "White, red, black", "articleId": articleUuid, "append": "false"})
# 		logging.info("Test UpdateArticle params are: " + str(params))

# 		response = self.testapp.post('/UpdateArticle', params)
# 		logging.info("Test UpdateArticle response status: " + response.status)

# 		# RESPONSE
# 		# {  
# 		#    "errorcode":0,
# 		#    "fieldsUpdated":[  
# 		#       "articleColors"
# 		#    ]
# 		# }

# 		responseContent = json.loads(response.normal_body)
# 		logging.info("Test UpdateArticle response body: " + str(responseContent)) 

# 		errorcode = responseContent['errorcode']
# 		fieldsUpdated = responseContent['fieldsUpdated']
# 		logging.info("Test UpdateArticle fieldsUpdated: " + str(fieldsUpdated))

# 		self.assertEqual(errorcode, 0)
# 		self.assertEqual(fieldsUpdated[0], "articleColors", "Article Colors not updated successfully")

# 	def testUpdateType(self):
# 		logging.info("Testing UpdateType")

# 		self.testbed.init_memcache_stub()

# 		articleUuid = self.testCreateArticle();
# 		newType = "Sweaters"

# 		# REQUEST
# 		# {  
# 		#    "articleId":"51b6a314-5455-11e5-b105-373a21fd1710",
# 		#    "articleType":"Sweaters",
# 		#    "tokenId":"ya29.HgImnIyMz6YrI856Bkq1DPFtZUcuhOwrgRKFenxc4CvbZZirBo9hNDeuz6Vg_wmUxaluew"
# 		#	 "append": "false"
# 		# }

# 		# update article colors
# 		params = json.dumps({"tokenId": self.tokenId, "articleId": articleUuid, "articleType": newType, "append": "false"})
# 		logging.info("Test UpdateType params are: " + str(params))

# 		response = self.testapp.post('/UpdateArticle', params)
# 		logging.info("Test UpdateType response status: " + response.status)

# 		# RESPONSE
# 		{  
# 		   "errorcode":0,
# 		   "fieldsUpdated":[  
# 		      "articleColors"
# 		   ]
# 		}

# 		responseContent = json.loads(response.normal_body)
# 		logging.info("Test UpdateType response body: " + str(responseContent)) 

# 		errorcode = responseContent['errorcode']
# 		fieldsUpdated = responseContent['fieldsUpdated']
# 		logging.info("Test UpdateType fieldsUpdated: " + str(fieldsUpdated))

# 		self.assertEqual(errorcode, 0)
# 		self.assertEqual(fieldsUpdated[0], "articleType", "Article type not updated successfully")

# 	def testUpdateTags(self):
# 		logging.info("Testing UpdateTags")

# 		self.testbed.init_memcache_stub()

# 		articleUuid = self.testCreateArticle();

# 		# REQUEST
# 		# {  
# 		#    "articleTags":"Scarf, red, black",
# 		#    "articleId":"51b6a314-5455-11e5-b105-373a21fd1710",
# 		#    "append":"false",
# 		#    "tokenId":"ya29.HgImnIyMz6YrI856Bkq1DPFtZUcuhOwrgRKFenxc4CvbZZirBo9hNDeuz6Vg_wmUxaluew"
# 		# }

# 		# update article colors
# 		params = json.dumps({"tokenId": self.tokenId, "articleTags": "Scarf, red, black", "articleId": articleUuid, "append": "false"})
# 		logging.info("Test UpdateTags params are: " + str(params))

# 		response = self.testapp.post('/UpdateArticle', params)
# 		logging.info("Test UpdateTags response status: " + response.status)

# 		# RESPONSE
# 		# {  
# 		#    "errorcode":0,
# 		#    "fieldsUpdated":[  
# 		#       "articleTags"
# 		#    ]
# 		# }

# 		responseContent = json.loads(response.normal_body)
# 		logging.info("Test UpdateTags response body: " + str(responseContent)) 

# 		errorcode = responseContent['errorcode']
# 		fieldsUpdated = responseContent['fieldsUpdated']
# 		logging.info("Test UpdateTags fieldsUpdated: " + str(fieldsUpdated))

# 		self.assertEqual(errorcode, 0)
# 		self.assertEqual(fieldsUpdated[0], "articleTags", "Article tags were not updated successfully")

# 	#7 - Verifies update to article price
# 	def testUpdatePrice(self):
# 		logging.info("Testing UpdatePrice")

# 		self.testbed.init_memcache_stub()

# 		articleUuid = self.testCreateArticle();

# 		# REQUEST
# 		# {  
# 		#    "articlePrice":"50.00",
# 		#    "articleId":"51b6a314-5455-11e5-b105-373a21fd1710",
# 		#    "append":"false",
# 		#    "tokenId":"ya29.HgImnIyMz6YrI856Bkq1DPFtZUcuhOwrgRKFenxc4CvbZZirBo9hNDeuz6Vg_wmUxaluew"
# 		# }

# 		# update article colors
# 		params = json.dumps({"tokenId": self.tokenId, "articlePrice": "50.00", "articleId": articleUuid, "append": "false"})
# 		logging.info("Test UpdatePrice params are: " + str(params))

# 		response = self.testapp.post('/UpdateArticle', params)
# 		logging.info("Test UpdatePrice response status: " + response.status)

# 		# RESPONSE
# 		# {  
# 		#    "errorcode":0,
# 		#    "fieldsUpdated":[  
# 		#       "articlePrice"
# 		#    ]
# 		# }

# 		responseContent = json.loads(response.normal_body)
# 		logging.info("Test UpdatePrice response body: " + str(responseContent)) 

# 		errorcode = responseContent['errorcode']
# 		fieldsUpdated = responseContent['fieldsUpdated']
# 		logging.info("Test UpdatePrice fieldsUpdated: " + str(fieldsUpdated))

# 		self.assertEqual(errorcode, 0)
# 		self.assertEqual(fieldsUpdated[0], "articlePrice", "Article tags were not updated successfully")

# 	#8 - Verifies update to article description
# 	def testUpdateDescription(self):
# 		logging.info("Testing UpdateDescription")

# 		self.testbed.init_memcache_stub()

# 		articleUuid = self.testCreateArticle();

# 		# REQUEST
# 		# {  
# 		#    "articleDescription":"article new description",
# 		#    "articleId":"51b6a314-5455-11e5-b105-373a21fd1710",
# 		#    "append":"false",
# 		#    "tokenId":"ya29.HgImnIyMz6YrI856Bkq1DPFtZUcuhOwrgRKFenxc4CvbZZirBo9hNDeuz6Vg_wmUxaluew"
# 		# }

# 		# update article colors
# 		params = json.dumps({"tokenId": self.tokenId, "articleDescription": "article new description", "articleId": articleUuid, "append": "false"})
# 		logging.info("Test UpdateDescription params are: " + str(params))

# 		response = self.testapp.post('/UpdateArticle', params)
# 		logging.info("Test UpdateDescription response status: " + response.status)

# 		# RESPONSE
# 		# {  
# 		#    "errorcode":0,
# 		#    "fieldsUpdated":[  
# 		#       "articleDescription"
# 		#    ]
# 		# }

# 		responseContent = json.loads(response.normal_body)
# 		logging.info("Test UpdateDescription response body: " + str(responseContent)) 

# 		errorcode = responseContent['errorcode']
# 		fieldsUpdated = responseContent['fieldsUpdated']
# 		logging.info("Test UpdateDescription fieldsUpdated: " + str(fieldsUpdated))

# 		self.assertEqual(errorcode, 0)
# 		self.assertEqual(fieldsUpdated[0], "articleDescription", "Article description was not updated successfully")

# 	#9 - Verifies update to OkToSell
# 	def testUpdateOkToSell(self):
# 		logging.info("Testing UpdateOkToSell")

# 		self.testbed.init_memcache_stub()

# 		articleUuid = self.testCreateArticle();

# 		# REQUEST
# 		# {  
# 		#    "articleOkToSell":"true",
# 		#    "articleId":"51b6a314-5455-11e5-b105-373a21fd1710",
# 		#    "append":"false",
# 		#    "tokenId":"ya29.HgImnIyMz6YrI856Bkq1DPFtZUcuhOwrgRKFenxc4CvbZZirBo9hNDeuz6Vg_wmUxaluew"
# 		# }

# 		# update article colors
# 		params = json.dumps({"tokenId": self.tokenId, "articleOkToSell": "true", "articleId": articleUuid, "append": "false"})
# 		logging.info("Test UpdateOkToSell params are: " + str(params))

# 		response = self.testapp.post('/UpdateArticle', params)
# 		logging.info("Test UpdateOkToSell response status: " + response.status)

# 		# RESPONSE
# 		# {  
# 		#    "errorcode":0,
# 		#    "fieldsUpdated":[  
# 		#       "articleOkToSell"
# 		#    ]
# 		# }

# 		responseContent = json.loads(response.normal_body)
# 		logging.info("Test UpdateOkToSell response body: " + str(responseContent)) 

# 		errorcode = responseContent['errorcode']
# 		fieldsUpdated = responseContent['fieldsUpdated']
# 		logging.info("Test UpdateOkToSell fieldsUpdated: " + str(fieldsUpdated))

# 		self.assertEqual(errorcode, 0)
# 		self.assertEqual(fieldsUpdated[0], "articleOkToSell", "Article OkToSell flag was not updated successfully")

# 	#10 - Verifies update to private
# 	def testUpdatePrivateFlag(self):
# 		logging.info("Testing UpdatePrivateFlag")

# 		self.testbed.init_memcache_stub()

# 		articleUuid = self.testCreateArticle();

# 		# REQUEST
# 		# {  
# 		#    "articlePrivate":"true",
# 		#    "articleId":"51b6a314-5455-11e5-b105-373a21fd1710",
# 		#    "append":"false",
# 		#    "tokenId":"ya29.HgImnIyMz6YrI856Bkq1DPFtZUcuhOwrgRKFenxc4CvbZZirBo9hNDeuz6Vg_wmUxaluew"
# 		# }

# 		# update article colors
# 		params = json.dumps({"tokenId": self.tokenId, "articlePrivate": "true", "articleId": articleUuid, "append": "false"})
# 		logging.info("Test UpdatePrivateFlag params are: " + str(params))

# 		response = self.testapp.post('/UpdateArticle', params)
# 		logging.info("Test UpdatePrivateFlag response status: " + response.status)

# 		# RESPONSE
# 		# {  
# 		#    "errorcode":0,
# 		#    "fieldsUpdated":[  
# 		#       "articleOkToSell"
# 		#    ]
# 		# }

# 		responseContent = json.loads(response.normal_body)
# 		logging.info("Test UpdatePrivateFlag response body: " + str(responseContent)) 

# 		errorcode = responseContent['errorcode']
# 		fieldsUpdated = responseContent['fieldsUpdated']
# 		logging.info("Test UpdatePrivateFlag fieldsUpdated: " + str(fieldsUpdated))

# 		self.assertEqual(errorcode, 0)
# 		self.assertEqual(fieldsUpdated[0], "articlePrivate", "Article articlePrivate flag was not updated successfully")

# 	#11 - delete articles
# 	def testDeleteArticle(self):
# 		logging.info("Testing DeleteArticle")

# 		self.testbed.init_memcache_stub()

# 		articleUuid = self.testCreateArticle('Article One')

# 		# REQUEST
# 		# {  
# 		#    "articleidstodelete":[  
# 		#       "847fa0ba-8511-11e5-8d68-1f1f53c13f4d"
# 		#    ]
# 		# }

# 		articleidstodelete = [articleUuid]
# 		# update article colors
# 		params = json.dumps({"articleidstodelete": articleidstodelete})
# 		logging.info("Test DeleteArticle params are: " + str(params))

# 		response = self.testapp.post('/DeleteArticle', params)
# 		logging.info("Test DeleteArticle response status: " + response.status)

# 		# RESPONSE
# 		# {  
# 		#    "errorcode":0
# 		# }

# 		responseContent = json.loads(response.normal_body)
# 		logging.info("Test DeleteArticle response body: " + str(responseContent)) 

# 		errorcode = responseContent['errorcode']
		
# 		self.assertEqual(errorcode, 0)

# 	#12 - delete multiple articles
# 	def testDeleteArticles(self):
# 		logging.info("Testing DeleteArticles")

# 		self.testbed.init_memcache_stub()

# 		article1Uuid = self.testCreateArticle('Article One')
# 		article2Uuid = self.testCreateArticle('Article Two')

# 		# REQUEST
# 		# {  
# 		#    "articleidstodelete":[  
# 		#       "847fa0ba-8511-11e5-8d68-1f1f53c13f4d", "547fa0ba-8511-11e5-8d68-1f1f53c13f4d"
# 		#    ]
# 		# }

# 		articleidstodelete = [article1Uuid, article2Uuid]
# 		# update article colors
# 		params = json.dumps({"articleidstodelete": articleidstodelete})
# 		logging.info("Test DeleteArticles params are: " + str(params))

# 		response = self.testapp.post('/DeleteArticle', params)
# 		logging.info("Test DeleteArticles response status: " + response.status)

# 		# RESPONSE
# 		# {  
# 		#    "errorcode":0
# 		# }

# 		responseContent = json.loads(response.normal_body)
# 		logging.info("Test DeleteArticles response body: " + str(responseContent)) 

# 		errorcode = responseContent['errorcode']
		
# 		self.assertEqual(errorcode, 0)

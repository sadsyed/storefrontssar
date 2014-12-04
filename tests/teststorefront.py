import json
import httplib
import urllib
import time

globals = {"server": "storefrontssar2.appspot.com","port":"80","headers": {"Content-type": "application/json", "Accept": "text/plain"},"userId": "amy_hindman@yahoo.com"}

conn = httplib.HTTPConnection(globals["server"],globals["port"])

sampleCategories = ['Coats','Dresses','Gloves','Hats','Pants','Scarves','Shirts','Shoes','Shorts','Skirts','Sweaters']

def send_request(conn, url, req, printinput):
    if(printinput):
        #Don't print if upload image json, too big.
        print "json request:"
        print '%s' % json.dumps(req)
    else:
        print 'Skipping json input due to size.'
    conn.request("POST", url, json.dumps(req), globals["headers"])
    resp = conn.getresponse()
    print "status reason"
    print resp.status, resp.reason
    response = resp.read()
    try:
        jsonresp = json.loads(response)
        print '  %s' % jsonresp
        return jsonresp
    except:
        print 'No json: ' + str(response)

def send_get_request(conn, url):

    conn.request("GET", url)
    resp = conn.getresponse()
    print "status reason"
    print resp.status, resp.reason
    response = resp.read()
    try:
        jsonresp = json.loads(response)
        print '  %s' % jsonresp
        return jsonresp
    except:
        print 'No json: ' + str(response)

if __name__ == '__main__':
    #Create a new stream
    print('Testing get categories')
    ServiceURL = '/GetCategories'
    serviceJSON = {}
    response = send_request(conn,ServiceURL,serviceJSON,True)
    categoryList = response['currentCategories']
    assertIndex = -1
    trackCategory = list()
    print("Length of response is: " + str(len(categoryList)))
    for returnVal in categoryList:
        actualCat = returnVal['name']
        trackCategory.append(actualCat)
        try:
            assertIndex = sampleCategories.index(actualCat)
        except:
            assertIndex = -1
        assert assertIndex >= 0
    for myCat in sampleCategories:
        count = trackCategory.count(myCat)
        assert count < 2
    time.sleep(1)

    #Create a new stream
    print('Testing get sale categories')
    ServiceURL = '/GetSaleCategories'
    serviceJSON = {}
    response = send_request(conn,ServiceURL,serviceJSON,True)
    categoryList = response['currentCategories']
    assertIndex = -1
    trackCategory = list()
    print("Length of response is: " + str(len(categoryList)))
    for returnVal in categoryList:
        actualCat = returnVal['name']
        trackCategory.append(actualCat)
        try:
            assertIndex = sampleCategories.index(actualCat)
        except:
            assertIndex = -1
        assert assertIndex >= 0
    for myCat in sampleCategories:
        count = trackCategory.count(myCat)
        assert count < 2
    time.sleep(1)

    print('Testing create and get users')
    ServiceURL = '/GetUsers'
    response = send_get_request(conn,ServiceURL)
    userList = response['userList']
    initlistlength = len(userList)
    ServiceURL = '/signup2'
    serviceJSON = {'username':'mytestuser','email':'fake@fake.com','name':'Fake','password':'password','lastname':'fake'}
    response = send_request(conn,ServiceURL,serviceJSON,True)
    assert response['errorcode'] == 0
    ServiceURL = '/GetUsers'
    response = send_get_request(conn,ServiceURL)
    userList = response['userList']
    countuser = userList.count('Fake')
    assert countuser == 1
    assert len(userList) == (initlistlength + 1)
    time.sleep(1)


import json
import datetime

testdate = str(datetime.datetime.now().date())
mystructure = {'testdate':testdate, 'articleidstodelete':['1103a078-6bae-11e4-9583-b1e246a0f8f9', '863397b3-6d97-11e4-84bb-b1e246a0f8f9','d636318a-6bac-11e4-a1c7-afdd40c63338','ca56af61-6d99-11e4-9010-7bcb04c4bd78','040183dc-6bad-11e4-bdce-b1e246a0f8f9','4487bfcf-6bac-11e4-90c6-afdd40c63338','a0be0394-6d97-11e4-9dc4-b1e246a0f8f9','92d803ab-6bac-11e4-b605-afdd40c63338','e1e47ff0-731a-11e4-9dce-0be08a85855e','d4d605eb-6d96-11e4-9ff3-b1e246a0f8f9']}
myjson = json.dumps(mystructure)
jsonfile = open("deletearticleidssamplejson.txt",'w')
jsonfile.write(str(myjson))
jsonfile.close()
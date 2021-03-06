import json
from datetime import datetime
import uuid

articlename = "Yellow Hat"
articleid = str(uuid.uuid1())
articletype = "Hat"
articleimageurl = 'http://lh3.ggpht.com/1_tyP1M_0Y7IWSNXn0JhBUAroU_HMhVix5laS-qBuoCPbmhU2aceVGrW-l8jF8w1bkmLxI5QmCXLmEbVXr9M0Xo'
articlelastused = ["2014-7-2"]
articletimesused = 2
articletags = ['#Yellow']
articledescription = "A comfortable light yellow hat to block the summer sun."
articleprice = 28.00
 
mystructure = {'articlename':articlename,'articleid':articleid,'articletype': articletype, 'articledescription': articledescription, 'articleimageurl':articleimageurl, 'articlelastused':articlelastused, 'articletimesused':articletimesused, 'articletags':articletags,'articleprice':articleprice}
myjson = json.dumps(mystructure)
jsonfile = open("createarticlesamplejson.txt",'w')
jsonfile.write(str(myjson))
jsonfile.close()


#"http://lh5.ggpht.com/cV5RC_BjfRHDB5Eypfvu4VTXcC89eU7pWKumK2AVdi1uxCDpKQLjGnsYOUVVBTmTTPCy-0nNpVgGdGTldghelsCH5A" 
#"http://lh3.ggpht.com/nlO8hk4TlCHddh9RNaoliNTUi1JlahhiJp6vjFC5ayciwUk2Wq85AN2_vDGeKxcEk1G0T8Q_x7t1TNTDLrniBnaPdA"
#"http://lh5.ggpht.com/Nh1UA5Ot2BxDqw5NqEkQcXo-VaJ50H8FyDb5YtOSgkkRscH-NSI2XAr-fV62-NEARDw4nAvLicKjdXzqDRSU2mwjxA"
#"http://lh4.ggpht.com/84Vyq_2MFH3oVu2KvsqJuucA_ZEjTR-zxt5AKlIYt89Gsg5DPKfnGbYz6Ylxd06MrdX0g9iJmoezeJ5hDn5ujH-45A" 
#"http://lh5.ggpht.com/M4eAhrqeMaoePoxOsuo62VPv1B27avez5-UZtdQ3vBXZNvqWPJbUeUh70PvHKSyxzYZq41G_s0zcJ-LsGpCoEvYDAw"
#"http://lh6.ggpht.com/wMJOQpJBHm3bG3ZPIz-z4xS2nZ9KNa4MElfBMyfve-sgboSdMfallE1dh2a35XvuiakC9h6tMnaP-pCMM35nvblt" 
#'http://lh4.ggpht.com/c5uoh26GDHjRzWFcmShN98BUgN3HUHnrNzyzbCOM0ycMQVw4Sq-smanONjp9-AJHGJK1hHH_6R-8MwFqZoWkZdGH'
#"http://lh3.ggpht.com/-cwUme6uHKiBSGe0898TTp-6VvnS51grHkbcNF_XpFajx8I-mGHGDbQv7VnBodh_HqhF2g8aQwWk_Jp9WI40Z4ncrQ" 
#"http://lh3.ggpht.com/1_tyP1M_0Y7IWSNXn0JhBUAroU_HMhVix5laS-qBuoCPbmhU2aceVGrW-l8jF8w1bkmLxI5QmCXLmEbVXr9M0Xo"
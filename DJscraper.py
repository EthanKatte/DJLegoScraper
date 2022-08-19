import sys
from requests_html import HTMLSession
import time


def getListedItems():
    codes = []
    unknownLinks = []
    numberTotal = 0
    moreItems = True
    offset=0
    while moreItems:
        time.sleep(2) #reduces chances of being blocked
        session = HTMLSession() #starts html session
        numberCurrent = 0 #number of elements currently found
        r = session.get('https://www.davidjones.com/kids/toys-and-books?src=fh&refine=brand_name:lego&size=90&offset={}'.format(offset)) #gets the data of the source for the session
        offset+=90 #migrates to the next page
        r.html.render() #renders the JS on the site

        pageContents = r.html.links #get all the links from the html element of the page

        r.session.close() #close the session - prevents hanging and timeout

        for link in pageContents: 
            if 'https://www.davidjones.com/product/lego' in link: #if the link is a product link
                if link[41].isdigit(): #deals with url's that dont match the format needed (i.e. ...product/lego/lego-{code}-...)
                    if link[40:45] not in codes: #ensures no double ups
                        codes.append(link[40:45])
                        numberTotal+=1 #the number of items found in total
                        numberCurrent+=1 #the number of items found on this page
                else:
                    unknownLinks.append(link)

        if numberCurrent == 0: #if no items were found on this page
            moreItems = False #therefore, there is no more items
        print("New Page: Current Number Total : {}".format(numberTotal)) #tracks page level and 
    return codes, unknownLinks



def readCurrentCodes():
    pass

def writeCurrentCodes(currentCodes);
    pass 

def update():
    
        if(len(sys.argv) == 3 and sys.argv[2] == "-a"):
            print("Here are all the item codes: ")
            print(currItemArr)

        currItemArr, unknownLinks = getListedItems() #gets the item codes and unkowns from DJ's
        
        if currItemArr == None: #if no items were found something probably fucked up
            print("An Error has occured - no items found")
            return
        


        


def check():
    ###GETTING THE CODES FROM DavidJones.com###
        currItemArr, unknownLinks = getListedItems() #gets the item codes and unkowns from DJ's

        if currItemArr == None: #if no items were found something probably fucked up
            print("An Error has occured - no items found")

        if len(unknownLinks) != 0: #if there are unknown links show them
            print("Some unknown links have been found:")
            for link in unknownLinks:
                print("     {}".format(link))
        ### -c option ###
        if(len(sys.argv) == 3 and (sys.argv[2] == "-check" or sys.argv[2] == "-c"):
            print("Here are all the item codes: ")
            print(currItemArr)

        print("Here are the new ones: ")
        controlArr = ['76945', '43204', '75337', '71410', '10975', '71033', '76401', '10972', '76396', '11026', '10938', '71406', '10973', '60354', '60339', '11024', '43203', '75333', '60345', '76398', '76402', '60341', '60340', '42135', '43206', '10970', '10965', '76946', '41715', '11025', '41717', '76403', '31131', '10283', '10971', '60349', '75334', '11019', '60342', '76949', '41718', '60346', '71408', '42137', '42139', '71767', '42144', '76944', '43205', '76948', '41705', '41710', '71768', '76206', '41711', '10969', '42140', '75336', '41702', '60316', '71032', '41696', '71774', '60353', '76217', '42145', '41716', '76216', '42138', '60350', '76397', '10302', '43209', '41703', '76400', '41714', '41708', '60337', '71403', '10942', '10962', '60348', '31123', '71769', '41699', '41701', '60344', '60321', '71397', '76205', '76185', '60322', '43198', '31124', '76207', '31125', '60338', '11023', '71765', '60355', '11017', '41704', '76203', '71760', '76195', '76237', '71404', '10960', '71773', '41712', '42125', '42127', '70688', '43199', '60317', '31132', '60312', '71402', '10967', '41720', '71764', '31126', '71407', '60328', '60315', '10966', '10964', '76204', '71401', '41694', '60325', '10977', '42134', '76184', '41679', '10980', '43208', '42133', '41700', '76943', '60320', '71757', '70690', '10932', '71759', '41713', '31127', '10282', '10281', '71772', '76193', '41684', '76389', '41719', '60343', '71775', '70689', '76182', '11018', '42123', '60318', '71766', '71770', '41697', '76399', '10974', '71771', '10941', '21046', '10959', '41695', '71400', '71387', '10968', '60288', '11015', '71755', '75318', '60300', '60283', '41681', '60293', '60281', '71365', '43196', '76387', '71396', '71703', '71398', '42122', '41448', '75948', '41441', '10291', '31119', '60330', '60287', '60295', '76183', '43197', '60256', '42118', '10944', '60319', '43180', '60314', '41439', '42126', '11006', '60276', '31120', '60299', '76145', '10930', '10948', '71737', '60301', '76154', '60285', '76156', '76157', '41689', '60242', '42129', '71382', '71393', '10696', '10961', '43195', '41677', '42111', '76238', '31113', '60323', 
    '41691', '60284', '60253', '31112', '71399', '76155', '60329', '10940', '41683', '41685', '75315', '10947', '41707', '60294', '71388', '71749', '60306', '60302', '71385', '60291']
        for item in currItemArr:
            if item not in controlArr:
                print(item)

def main():
    if(len(sys.argv)==1):
        print("Whatcha tryin to do pal? Your options are:\n\t -update : updates the recorded lego codes (currentCodes.txt)\n\t -check : checks for any new lego products\n\t")


    if(sys.argv[1] == "-update"):
        update()
    elif sys.argv[1] =="-check":
        check()
    



    
    
    



main()



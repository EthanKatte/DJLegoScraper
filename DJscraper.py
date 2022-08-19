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

def readCurrentCodes(): #reads and returns the most recent save of the codes on the website
    FcurrentCodes = open("currentCodes.txt", "r")
    readCodes = (FcurrentCodes.read()).split()
    FcurrentCodes.close

    FunknownLinks = open("unknownLinks.txt", "r")
    readLinks = (FunknownLinks.read()).split()
    FunknownLinks.close()

    return readCodes, readLinks

def writeCurrentCodes():
    currentCodes, unknownLinks = getListedItems() #get the new items

    if currentCodes == None: #if no items were found something probably fucked up
            print("An Error has occured - no items found")
            return 0, 0


    FcurrentCodes = open("currentCodes.txt", "w")

    for item in currentCodes:
        FcurrentCodes.write(" " + item)
    FcurrentCodes.close

    FunknownLinks = open("unknownLinks.txt", "w")
    for link in unknownLinks:
        FunknownLinks.write(" " + link)
    FunknownLinks.close()

def linebreak():
    print("---------------------------------------------------------------------------------------------------")


def update():
    
        oldItemArr, oldUnknownLinks = readCurrentCodes() #gets the item codes and unkowns from DJ's
        if oldItemArr == 0:
            return

        if(len(sys.argv) == 3 ) and (sys.argv[2] == "-a"):
            print("Here are all the old item codes: ")
            print(oldItemArr)

        removed = []
        new = []

        writeCurrentCodes()
        
        newItemArr, newUnknownLinks = readCurrentCodes() #gets the item codes and unkowns from DJ's

        for oldItem in oldItemArr: #checks to see if any items have been removed
            if oldItem not in newItemArr:
                removed.append(oldItem)

        for newItem in newItemArr: #checks to see if there are any new items
            if newItem not in oldItemArr:
                new.append(newItem)

        for oldLink in oldUnknownLinks: #checks if any links have been removed
            if oldLink not in newUnknownLinks:
                removed.append(oldLink)
        
        for newLink in newUnknownLinks: #checks if any new links have been added
            if newLink not in oldUnknownLinks:
                new.append(newLink)

        linebreak()
        if(len(new) == 0):
            print("No new items")
        else:
            
            print("Here are the new items: ")
            for item in new:
                print("\t"+item)
        linebreak()
        linebreak()
        if len(removed) == 0:
            print("No removed items")
        else:
            print("Here are the removed Items: ")
            for item in removed:
                print("\t"+item)
        linebreak()




        
        


        


def check():
    ###GETTING THE CODES FROM DavidJones.com###
        currItemArr, unknownLinks = getListedItems() #gets the item codes and unkowns from DJ's

        if currItemArr == None: #if no items were found something probably fucked up
            print("An Error has occured - no items found")

        if len(unknownLinks) != 0: #if there are unknown links show them
            print("Some unknown links have been found:")
            for link in unknownLinks:
                print("\t{}".format(link))
        ### -c option ###
        if(len(sys.argv) == 3 and (sys.argv[2] == "-all" or sys.argv[2] == "-a")):
            print("Here are all the currently stored item codes: ")
            print(currItemArr)

        controlItemArr, controlLinkArr = readCurrentCodes()
        new = []
        removed = []


        for item in currItemArr:
            if item not in controlItemArr:
                new.append(item)

        for item in controlItemArr:
            if item not in controlItemArr:
                removed.append(item)

        for Link in unknownLinks:
            if Link not in controlLinkArr:
                new.append(Link)

        for Link in controlLinkArr:
            if Link not in unknownLinks:
                removed.append(Link)

        linebreak()
        if(len(new) == 0):
            print("No new items")
        else:
            
            print("Here are the new items: ")
            for item in new:
                print("\t"+item)
        linebreak()
        linebreak()
        if len(removed) == 0:
            print("No removed items")
        else:
            print("Here are the removed Items: ")
            for item in removed:
                print("\t"+item)
        linebreak()
        linebreak()
        print("NO UPDATES WERE WRITTEN")
        linebreak()        
        


def main():
    if(len(sys.argv)==1):
        print("Whatcha tryin to do pal? Your options are:\n\t -update : updates the recorded lego codes (currentCodes.txt)\n\t -check : checks for any new lego products\n\t")
    if(sys.argv[1] == "-update"):
        update()
    elif sys.argv[1] =="-check":
        check()
    



    
    
    



main()
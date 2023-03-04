from concurrent.futures import process
import os
import sys
from requests_html import HTMLSession
import time
import requests
import webbrowser
import multiprocessing


def getListedItems(): #gets the product links for the DJ website
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

def writeCurrentCodes(): #writes the current codes to persistant files
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

def linebreak(): #prints a line break... so fancy
    print("---------------------------------------------------------------------------------------------------")

def update(): #updates the files and shows any new codes and removed ones
    
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

def check(): #shows any new codes and any removed ones - DOES NOT SAVE
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
            if item not in currItemArr:
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
        
def printFunc(): #prints all currently available codes on davidjones.com
    curritems, currLinks = readCurrentCodes()
    linebreak()
    for item in curritems:
        print(item)
    linebreak()
    linebreak()
    for link in currLinks:
        print(link)
    linebreak()

def searchFunc(): #allows for the checking of specific codes ... this is pretty useless... 
    
    argLength = len(sys.argv)
    if argLength == 3 and sys.argv[2] == "-new":
        curritems, currLinks = getListedItems()
    else:
        curritems, currLinks = readCurrentCodes()

    code = input("What code would you like to check? (type 'quit' to leave) ")
    while code != "quit":
        if code in curritems:
            print("\nYes, David Jones has {} in stock\n".format(code))
        else:
            print("\nNo, David Jones does not have {} in stock\n".format(code))
        code = input("What code would you like to check? (type 'quit' to leave) ")

def retire_status(code): #gets html from lego.com and looks for retired string
    legoURL = "https://www.lego.com/en-hu/product/{}".format(code)
    r = requests.get(legoURL)
    if('"availabilityText":"Retired product"' in r.text):
        print("\tRETIRED: {} | Link {}".format(code, legoURL))
        if len(sys.argv) == 3 and sys.argv[2] == "-open":
            webbrowser.open(legoURL)

def seperatecodes(codes): #seperates the codes into 4 subsets for the children
    
    code1 = []
    code2 = []
    code3 = []
    code4 = []
    codeNum = 0

    for code in codes:
        if codeNum == 0:
            code1.append(code)
            codeNum += 1
        elif codeNum == 1:
            code2.append(code)
            codeNum += 1
        elif codeNum == 2:
            code3.append(code)
            codeNum += 1
        elif codeNum == 3:
            code4.append(code)
            codeNum -= 3

    return code1,code2,code3,code4

def child_multi_retireCheck(codes, childNum): #run the retire check for each of the childrens lists
    count = 0
    for item in codes:
        print("{}:{} | processing code {}".format(childNum, count, item))
        retire_status(item)
        count+=1
    

def multi_rcheck(): #responsible for the creation, delegation, processing and destruction of the children
    start_time = time.perf_counter()
    linebreak()
    print("Starting retire status check - This may take a while... starting timer")
    print("Child:Index | Lego Code")

    currItems, unknownLinks = readCurrentCodes()

    code1, code2, code3, code4 = seperatecodes(currItems) #divy up the code arr to the 4 children

    proc1 = multiprocessing.Process(target=child_multi_retireCheck, args = (code1, 1)) #create the children
    proc2 = multiprocessing.Process(target=child_multi_retireCheck, args = (code2, 2))
    proc3 = multiprocessing.Process(target=child_multi_retireCheck, args = (code3, 3))
    proc4 = multiprocessing.Process(target=child_multi_retireCheck, args = (code4, 4))

    proc1.start() #start the children
    proc2.start()
    proc3.start()
    proc4.start()

    proc1.join() #join the children
    print("proc1  closed")
    proc2.join()
    print("proc2  closed")
    proc3.join()
    print("proc3  closed")
    proc4.join()
    print("proc4  closed")
    end_time = time.perf_counter()
    print("runtime : {}s".format(end_time - start_time))





def rcheck():
    start = time.process_time()
    linebreak()
    currItems, unknownLinks = readCurrentCodes()
    for item in currItems:
        print("Next item {}, pid: {}".format(item, os.getpid))
        retire_status(item)

    linebreak()
    stop = time.process_time()
    print("Time Elapsed : {}s".format(stop - start))

def main():
    if(len(sys.argv)==1):
        print("Whatcha tryin to do pal? Your options are:\n\t -update : updates the recorded lego codes (currentCodes.txt, currentLinks.txt)\n\t -check : checks for any new lego products\n\t -print : prints all the current records\n\t -search : search for a code (use -new to search through an updated list)\n\t -rcheck : compares the product codes to lego.com to see if they are retired (takes a long time)\n\t -multi_rcheck : performs the retired check across multiple cores, speeding up the check to ~20 min (use -open to open the retired products page automatically) ")
        return
    if(sys.argv[1] == "-update"):
        update()
    elif sys.argv[1] =="-check":
        check()
    elif sys.argv[1] == "-print":
        printFunc()
    elif sys.argv[1] == "-search":
        searchFunc()
    elif sys.argv[1] == "-retired" or sys.argv[1] == "-rcheck":
        rcheck()
    elif sys.argv[1] == "-multi_retired" or sys.argv[1] == "-multi_rcheck":
        multi_rcheck()

if __name__ == "__main__":
    main()
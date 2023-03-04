# David Jones Lego Scraper
##What is it?
This is a script that scrapes the DavidJones.com.au website for all lego products currently available. It then looks at the respective pages on Lego.com to find any sets that are retired. THIS IS NOT FAST. THIS WILL NOT BE OPTIMISED FURTHER. This was my first attempt at a webscraper and was unaware of the nuances of beautifulSoup or requests-html libraries. It ingests the full HTML of the site and then does substring search for specific formats to determine the available lego codes. A much better way to do this is to find by class or ID and then process from there.


![image](https://user-images.githubusercontent.com/61607335/222857918-e149b08f-f4c0-48bd-b112-4c94356ae99b.png)

##How To Use It
This has a few different options for CMD Controls
![image](https://user-images.githubusercontent.com/61607335/222863997-8ffbbd82-69d2-4282-bdb2-347d2d1cf35b.png)
To run the program use `python ./DJscraper.py [parameter]`

parameter options are:
         -update : updates the recorded lego codes (currentCodes.txt, currentLinks.txt)
         -check : checks for any new lego products
         -print : prints all the current records
         -search : search for a code (use -new to search through an updated list)
         -rcheck : compares the product codes to lego.com to see if they are retired (takes a long time)
         -multi_rcheck : performs the retired check across multiple cores, speeding up the check to ~30 min (use -open to open the retired products page automatically)
         
## How to install
clone the repository by using `git clone https://github.com/EthanKatte/DJLegoScraper.git`

Ensure that html-requests is installed using `pip install html-requests`

NOTE: html-requests has an issue when being used with the python versions installed from the windows store. you must use python versions installed from the official python installer available here https://www.python.org/downloads/



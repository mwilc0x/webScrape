#####################################################################################
#####################################################################################
#####################################################################################
#####										#####
#####										#####
#####										#####
##### 			CS 336 Databases					#####
#####			Author: Mike Wilcox					#####	
#####			Email: mwilcox@eden.rutgers.edu				#####
#####			Website: http://mjwilcox.net				#####
#####			Date: 2/8/2012						#####
#####										#####
#####										#####
#####										#####
#####################################################################################
#####################################################################################
#####################################################################################

README
------



Updates:

-------

	1. Script checks stock symbols against provided ticker_list
	2. Scripts run on i-Lab machines. Please note that some code had to be placed into the src folder for this to happen. All modules are still in the 
	   lib/ folder.

Use:
---

The way I set it up is that the scripts look for the BeautifulSoup modules in a subfolder. This was the only way I could get them to work on the iLab machines for the time being. They will work though.

To start scraping either forum section and generating a csv file, in src/ type either:

	python cram_scrape.py

		OR

	python fast_money_scrape.py


About:
-----


Two python scripts that target two different sections of of the forum www.onlinetradersforum.com. These scripts each extract stock symbols, positive/negative connotations, and the complete url of the stock recommendation.

The scripts both use the BeautifulSoup module for python. The module's source file is located in the lib/. Note that in order to get these scripts to properly run on the i-Lab machines some lib code was placed into the src folder which guarantees that these scripts will run on the machines.

Each script generates a csv file. It is safe to have each script generate a csv file of their own, and then when these scripts are done collecting the results merge the two csv files into one. Note that when a script is run it will automatically overwrite the contents of a csv file if there is already a file present in the directory with the same name. I am working on a script to take in all csv files that a user may want to merge together and do the process automatically. I hope to have this done by the next collection round.

I have included print statements that will display the date of the stock symbols that are being collected followed by each symbol. This is to help ensure that the script is properly functioning. These can easily be removed by either commenting them out with a hashtag or by removing them altogether.

Also, the script caches the ticker_list into an array to double check that each symbol is a correct symbol. This was a problem in my last script that has been updated.

Sometimes the script will come across a wierd tag in the the html and subsequently crash. In this case, I would backup any existing csv data to a new file and manually change the i variable in the script to reflect the next page number of the forum threads to start on. For instance:

http://www.onlinetradersforum.com/forumdisplay.php?f=12&order=desc&page=17 is the URL for the 17th page in the Cramer stock selection portion of the forum. Note the 17 at the end of the URL. My script loops through the integer value at the end constantly increasing until it reaches 59.

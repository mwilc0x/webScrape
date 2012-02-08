#####################################################################################
#####################################################################################
#####################################################################################
#####										#####
#####										#####
#####										#####
##### 			Cramer Stock Scraper					#####
#####			Author: Mike Wilcox					#####	
#####			Class: 198:336 Databases				#####
#####										#####
#####										#####
#####										#####
#####################################################################################
#####################################################################################
#####################################################################################


import urllib2,sys,csv,imp

BeautifulSoup = imp.load_source('BeautifulSoup', 'lib/python/lib/BeautifulSoup.py')

from BeautifulSoup import BeautifulSoup,NavigableString,re,SoupStrainer


complete_url = ''
stock_symbol = ''
direction = '' 
ruid = '133001494'
i=21
symbols = []

symbolReader = csv.reader(open('ticker_list.csv', 'rb'), delimiter=' ')
for row in symbolReader:
        symbols.append(''.join(e for e in str(row) if e.isalnum()))


#CHANGE NAME OF CSV FILE BELOW TO REFLECT NAME OF FILE WRITING TO
output = open('name_of_output.csv', 'wb')


stockWriter = csv.writer(output, delimiter = ',', quoting = csv.QUOTE_ALL)
stockWriter.writerow(["ruid"] + ["stock_symbol"] + ["rec_date"] + ["direction"] + ["complete_url"])

while i <= 63:
   
	response = urllib2.urlopen("http://www.onlinetradersforum.com/forumdisplay.php?f=12&order=desc&page=" + str(i)).read()
	
	for link in BeautifulSoup(response, parseOnlyThese=SoupStrainer('a')):
    		if link.has_key('href'):
			if 'showthread' in link['href']:
				array = link.findAll('a', text=re.compile('Stock Picks Recap .'))

				#Date conversion - a lot of code but gets the job done
				for date in array:
					date = date[date.find('Recap ')+6:len(date)]
					month = date[0:date.find('/')]
					date = date[date.find('/')+1:len(date)]
					day = date[0: date.find('/')]
					month2 = date[0: date.find(' ')]

					if month == '1':
						month = '01'
					elif month == '2':
						month = '02'
					elif month == '3':
						month = '03'
					elif month == '4':
						month = '04'
					elif month == '5':
						month = '05'
					elif month == '6':
						month = '06'
					elif month == '7':
						month = '07'
					elif month == '8':
						month = '08'
					elif month == '9':
						month = '09'
					elif month == '10':
						month = '10'
					elif month == '11':
						month = '11'
					else:
						month = '12'	
					
					if day == '1':
						day = '01'
					elif day == '2':
						day = '02'
					elif day == '3':
						day = '03'
					elif day == '4':
						day = '04'
					elif day == '5':
						day = '05'
					elif day == '6':
						day = '06'
					elif day == '7':
						day = '07'
					elif day == '8':
						day = '08'
					elif day == '9':
						day = '09'	

					year = date[date.find('/')+1: len(date)]

					if year == '10':
						year = '2010'
					elif year == '09':
						year = '2009'
					elif year == '08':
						year = '2008'
					else:
						year = '2007'
				
					rec_date = year + month + day
					print rec_date

					url = str(link['href'])
                                        url = url[url.find('&')+1:len(url)]

					#Parse individual thread getting buy and sell picks
					if 'showthread.php?p=1023#post1023' not in link['href']:
						complete_url = "http://www.onlinetradersforum.com/showthread.php?" + url
						soup = BeautifulSoup(urllib2.urlopen("http://www.onlinetradersforum.com/showthread.php?" + url))
						node = soup.find("div", id=re.compile('^post_message.*'))						

						for node in soup.findAll('b', text='Bullish'):
    							while node is not soup.find('b', text='Bearish'):
								if node in soup.findAll('u'):
									temp_node = node
									temp_node = str(temp_node)
									temp_node = temp_node[temp_node.index('">')+2:temp_node.index('</a>')]
									stock_symbol = temp_node
									direction = 'positive'
									complete_url = "http://www.onlinetradersforum.com/showthread.php?" + url
									
									if stock_symbol in symbols:
										stockWriter.writerow([ruid] + [stock_symbol] + [rec_date] + [direction] + [complete_url])
										print stock_symbol + " is in the ticker list"
	
								if soup.find('b', text='Bearish'):
								
									if node.next is soup.find('b', text='Bearish'):
										node2 = node.next
										while node2 is not soup.find('font', text='Top 50 Trending Stocks'):
											if node2 in soup.findAll('u'):
												temp_node2 = node2
												temp_node2 = str(temp_node2)
												temp_node2 = temp_node2[temp_node2.index('">')+2:temp_node2.index('</a>')]
												
												stock_symbol = temp_node2
												direction = 'negative'
												complete_url = "http://www.onlinetradersforum.com/showthread.php?" + url
	
												if stock_symbol in symbols:
													stockWriter.writerow([ruid] + [stock_symbol] + [rec_date] + [direction] + [complete_url])
													print stock_symbol + " is in the ticker list"
												node2 = node2.next
											
											else:
												node2 = node2.next
											
										
								node = node.next
								if not soup.find('b', text='Bearish'):
									break			
	i+= 1

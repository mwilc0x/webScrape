#####################################################################################
#####################################################################################
#####################################################################################
#####										#####
#####										#####
#####										#####
##### 			Fast Money Stock Scraper				#####
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
i=20
symbols = []

symbolReader = csv.reader(open('ticker_list.csv', 'rb'), delimiter=' ')
for row in symbolReader:
        symbols.append(''.join(e for e in str(row) if e.isalnum()))

#CHANGE NAME OF CSV FILE BELOW TO REFLECT NAME OF FILE WRITING TO
output = open('name_of_output.csv', 'wb')


stockWriter = csv.writer(output, delimiter = ',', quoting = csv.QUOTE_ALL)
stockWriter.writerow(["ruid"] + ["stock_symbol"] + ["rec_date"] + ["direction"] + ["complete_url"])

while i <= 59:
   
	response = urllib2.urlopen("http://www.onlinetradersforum.com/forumdisplay.php?f=50&order=desc&page=" + str(i)).read()
	
	for link in BeautifulSoup(response, parseOnlyThese=SoupStrainer('a')):
    		if link.has_key('href'):
			if 'showthread' in link['href']:
				array = link.findAll('a', text=re.compile('Recap .'))

				#Please forgive the really hack-y date conversion thing going on
				for date in array:
					date = date[date.find(', ')+2:len(date)]
					day = date[date.find(' ')+1:date.find(',')]
					month = date[0: date.find(' ')]
					month2 = date[0: date.find(' ')]
					if month == 'January':
						month = '01'
					elif month == 'February':
						month = '02'
					elif month == 'March':
						month = '03'
					elif month == 'April':
						month = '04'
					elif month == 'May':
						month = '05'
					elif month == 'June':
						month = '06'
					elif month == 'July':
						month = '07'
					elif month == 'August':
						month = '08'
					elif month == 'September':
						month = '09'
					elif month == 'October':
						month = '10'
					elif month == 'November':
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
					year = date[date.find(', ')+2: len(date)]
					rec_date = year + month + day
					print rec_date

					url = str(link['href'])
                                        url = url[url.find('&')+1:len(url)]

					#Go into the individual thread and start parsing all the necessary variable
					if 'showthread.php?p=1023#post1023' not in link['href']:
						complete_url = "http://www.onlinetradersforum.com/showthread.php?" + url
						soup = BeautifulSoup(urllib2.urlopen("http://www.onlinetradersforum.com/showthread.php?" + url))
						node = soup.find("div", id=re.compile('^post_message.*'))						

						for node in soup.findAll('b', text='Buy'):
    							while node is not soup.find('b', text='Sell'):
								if node in soup.findAll('u'):
									temp_node = node
									temp_node = str(temp_node)
									temp_node = temp_node[temp_node.index('">')+2:temp_node.index('</a>')]
									stock_symbol = temp_node
									direction = 'positive'
									complete_url = "http://www.onlinetradersforum.com/showthread.php?" + url
									
									if stock_symbol in symbols:
										stockWriter.writerow([ruid] + [stock_symbol] + [rec_date] + [direction] + [complete_url])	
										print stock_symbol								

								if node.next is soup.find('b', text='Sell'):
									node2 = node.next
									while node2 is not soup.find('i', text='We do our best to list all the stocks mentioned, but mistakes may occur. This list is provided as a free public service, and we have no affiliation with CNBC or the show "Fast Money." Please consult a professional financial advisor before trading or investing, as loss of capital may result. This summary is not intended to replace watching the actual shows, where specific comments are made about each stock.'):
										if node2 in soup.findAll('u'):
											temp_node2 = node2
											temp_node2 = str(temp_node2)
											temp_node2 = temp_node2[temp_node2.index('">')+2:temp_node2.index('</a>')]
											stock_symbol = temp_node2
											direction = 'negative'
											complete_url = "http://www.onlinetradersforum.com/showthread.php?" + url

											if stock_symbol in symbols:
												stockWriter.writerow([ruid] + [stock_symbol] + [rec_date] + [direction] + [complete_url])
												print stock_symbol
											node2 = node2.next
										else:
											node2 = node2.next
								node = node.next			
	i+= 1

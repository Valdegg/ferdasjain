# scrape 
# nær í html töflur og vistar í gagnagrunn

# .

import requests
from bs4 import BeautifulSoup
import pandas as pd
import re 

print("import virkar")

# use: s = beforeComma(string)	
# before: string is a string that includes a comma 
# after: s is the part of string that's before the comma 
def beforeComma(string):
	return string.split(",")[0]


# ef headers eru ekki í fyrstu <td> röð þá 
	# skoða srome.github.io sem er með allar töflurnar á síðunni
	# table.find_all('table') skilar lista af <table> </table>
# use: list = getHTMLTabless(url)   # list of many? hverju skilar soup.find.find_all? lista af html lokuðum tag svigum 
# before: the url contains only one table?   with first row as headers/names 
# after: df is a list of dataframes with data from tables from url, with column names as headers from tables from url
def getHTMLTables(url):
	res = []
	
	r = requests.get(url)
	
	soup = BeautifulSoup(r.text, 'lxml') # spurning með 'lxml', fer eftir töflunni
	
	tables = soup.find_all('table')
	#print(tables[2])
	print(len(tables))
	nrOfTables = 0
	for table in tables:
		# first nrOfTables tables have been added to res as data frames 
		print("Yoho")
		
		#print(table.find_all('tr')[0]) #.find_all('td'))
		print("boho")
		nrOfColumns = len( table.find_all('tr')[0].find_all('th') ) # number of headers 
		
		columns = [[] for _ in table.find_all('tr')[0].find_all('th')]
		
		if len(columns) > 0:
			print("hy")
			# data is stored in the columns
			nrOfRows = 0 
			# how many rows have been traversed
			for row in table.find_all('tr')[1:]:
				# first nrOfRows rows have been added to c[0..nrOfRows] where c are in columns
				rowData = row.find_all('td')
				nrOfRows += 1 
				for columnNr in range(nrOfColumns):
					#print(rowData[columnNr].string)
					columns[columnNr].append( rowData[columnNr].string )
			
			# data in table has been loaded into columns 
			headers = []
			for header in table.find_all('tr')[0].find_all('th'):
				headers.append(header.string)
			print(headers)
			print(len(headers))
			res.append(pd.DataFrame(dict(zip(headers, columns))))
			# data frame with data from table with headers as key has been added to res
			nrOfTables += 1

	return res
	
#### Numbeo

# Fyrirsjáanleg nöfn
# dæmi: https://www.numbeo.com/crime/in/Reykjavik   https://www.numbeo.com/health-care/in/Reykjavik     https://www.numbeo.com/health-care/in/Berlin
# náum í verðlagið fyrir allar borgirnar og lífsgæðin fyrir hverja borg 



### Evropa, merkt með E í endann 

# næ fyrst í cost of living index töfluna, fæ þaðan nöfnin (dálkur "city")

costIndexE = getHTMLTables("https://www.numbeo.com/cost-of-living/region_rankings.jsp?title=2017&region=150")[0]
# costIndexE er dataframe með gögnunum úr costofliving fyrir Evrópu
qualityE = getHTMLTables("https://www.numbeo.com/quality-of-life/region_rankings.jsp?title=2017&region=150")
# qualityE er listi af data frames með quality of life indexana af Numbeo fyrir hverja borg í cityNamesE 

## ÞARF AÐ GÁ HVAÐA TÖFLUR ÞETTA ERU SEM KOMU OG GEYMA BARA ÞÆR SEM ERU RÉTTAR (hafa rétta headera)

print("cost index: ")
print(costIndexE)
#print(type(costIndexE[0]))
print(costIndexE['City'])
cityNamesE = list(map(beforeComma, costIndexE["City"]))

#print(cityNamesE)
# nöfnin á borgunum í Evrópu af Numbeo eru í cityNamesE

costE = []
# verðlagsgögnin fyrir borgirnar í cityNamesE verða í listanum af data frames costE

# index = 0
# for name in cityNamesE:
	# # verðlags gögnin fyrir fyrstu index borgirnar í cityNamesE eru í fyrstu index röðunum í costOfLivingE og qualityE
	# url = "https://www.numbeo.com/cost-of-living/in" + name 
	
	# costTables = getHTMLTables(url)
	# ## Hreinsa burt töflurnar sem eru óþarfi
	
	# costE.append(costTables)
	# index += 1
	
	


if len(cityNamesE) == len(costE):
	costE = dict(zip(cityNamesE, costE))
# costE is a dictionary with names of cities attached 
	







# data frameið sett í sqlite gagnagrunn

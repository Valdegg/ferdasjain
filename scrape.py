# scrape 
# nær í html töflur og vistar í gagnagrunn
# geymir verðlagið í gjaldeyrinum sem borgin notar. 
	# hægt að varpa á milli með töflunni sem er hér https://www.numbeo.com/common/currency_settings.jsp

# .

import requests
from bs4 import BeautifulSoup
import pandas as pd
import re 
import sqlite3 

# import locale 
# locale.setlocale( locale.LC_ALL, 'en_utf8' ) 
# locale.atoi('1,000,000') # 1000000 
# locale.atof('1,000,000.53') # 1000000.53 
# # nú ætti að vera hægt að breyta 2,234.20$ í 2234.20
# þarf kannski að fixa eitthvað? lesa um hvað locale.atoi gerir ef vesen 

print("import virkar")

# use: s = beforeComma(string)	
# before: string is a string that includes a comma 
# after: s is the part of string that's before the comma 
def beforeComma(string):
	return string.split(",")[0]


# ef keys eru ekki í fyrstu <td> röð þá 
	# skoða srome.github.io sem er með allar töflurnar á síðunni
	# table.find_all('table') skilar lista af <table> </table>
# use: list = getHTMLTabless(url)   # list of many? hverju skilar soup.find.find_all? lista af html lokuðum tag svigum 
# before: the url contains HTML tables
# after: df is a list of dataframes with data from tables from url, with column names as keys from tables from url
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
	
		
		headers = table.find_all('tr')[0].find_all('th')
		nrOfColumns = len( headers ) # number of column names 
	
		columns = [[] for _ in headers]
		
	
		if len(columns) > 0:
			# data is only loaded into the tables with keys 
		
			# data is stored in the columns
			nrOfRows = 0 
			# how many rows have been traversed
			for row in table.find_all('tr')[1:]:
				# first nrOfRows rows have been added to c[0..nrOfRows] where c are in columns
				rowData = row.find_all('td')
				nrOfRows += 1 
				if len(rowData) >0:
					for columnNr in range(nrOfColumns):
						
						if len(rowData[columnNr].contents) > 1:
							# some html stuff in this column 
							
							# í tilfellinu þar sem þetta er 'range':
							# tek það sem er á milli <span class="barTextLeft"> og </span>
							# og <span class="barTextRight"> og </span>
							# og greini á milli með "-"
							
							
							lowest = rowData[columnNr].contents[1].string
							highest = rowData[columnNr].contents[-1].string
							
							if(lowest is not None and highest is not None):
								# we can take substring og lowest 
								lowest = rowData[columnNr].contents[1].string[1:]								
								columns[columnNr].append(lowest + "-" + highest)
							else: 								
								columns[columnNr].append("")
							
							
						else: 
							columns[columnNr].append( str(rowData[columnNr].string) )
							
						
						
			
			# data in table has been loaded into columns 
			keys = []
			for header in headers:
				keys.append(header.string)
			
			res.append(pd.DataFrame(dict(zip(keys, columns))))
			# data frame with data from table with keys as key has been added to res
			nrOfTables += 1

	return res
	
	
# use: x = fixNames(cityNames)
# before: cityNames is a list of strings 
# after: x is cityNames with '(' and ')' removed and spaces replaced with '-', for scraping in Numbeo
def fixNames(cityNames):
	res = []
	for name in cityNames:
		res.append(name.replace(" ", "-").replace("(","").replace(")",""))
		
	for n, name in enumerate(res): 
		if name == 'The-Hague-Den-Haag':
			res[n] = 'The-Hague-Den-Haag-Netherlands'
	return res
	
#### Numbeo

# Fyrirsjáanleg nöfn
# dæmi: https://www.numbeo.com/crime/in/Reykjavik   https://www.numbeo.com/health-care/in/Reykjavik     https://www.numbeo.com/health-care/in/Berlin
# náum í verðlagið fyrir allar borgirnar og lífsgæðin fyrir hverja borg 



### Evropa, merkt með E í endann 

# næ fyrst í cost of living index töfluna, fæ þaðan nöfnin (dálkur "city")

costIndexE = getHTMLTables("https://www.numbeo.com/cost-of-living/region_rankings.jsp?title=2017&region=150")[0]
# costIndexE er dataframe með gögnunum úr costofliving fyrir Evrópu
qualityE = getHTMLTables("https://www.numbeo.com/quality-of-life/region_rankings.jsp?title=2017&region=150")[0]
# qualityE er listi af data frames með quality of life indexana af Numbeo fyrir hverja borg í cityNamesE 

## ÞARF AÐ GÁ HVAÐA TÖFLUR ÞETTA ERU SEM KOMU OG GEYMA BARA ÞÆR SEM ERU RÉTTAR (hafa rétta headera)
	# erum þegar bara með töflurnar sem eru með headera
	
	
# print("cost index: ")
# print(costIndexE)
# #print(type(costIndexE[0]))
# print(costIndexE[1:10])
cityNamesE = list(map(beforeComma, costIndexE["City"]))
print(cityNamesE)
#print(cityNamesE)
# nöfnin á borgunum í Evrópu af Numbeo eru í cityNamesE


costE = []
# verðlagsgögnin fyrir borgirnar í cityNamesE verða í listanum af data frames costE

index = 0
numberOfCities = len(cityNamesE)
scrapeFailures = [] #  price tables that didn't come through  
for name in fixNames(cityNamesE[0:numberOfCities]):
	# verðlags gögnin fyrir fyrstu index borgirnar í cityNamesE eru í fyrstu index röðunum í costE 
	url = "https://www.numbeo.com/cost-of-living/in/" + name + "?displayCurrency=EUR"
	print(cityNamesE[index])
	costTables = getHTMLTables(url)
	
	if(len(costTables) > 0):
		costTables = costTables[0]
		costTables.columns = ["Goods", "Prices", "Range"]
		costE.append(costTables)
	else: 
		
		scrapeFailures.append(name)
		scrapeFailures.append(costTables)
	## Hreinsa burt töflurnar sem eru óþarfi	?
	
	
	
	index += 1
	
# print("these are the") 
# print(scrapeFailures)

# print( "the scrape failures" )

# print("there are this many costTables in costE:" + str(len(costE)))

# for cities in costE:
	# print(cities.columns)

#if len(cityNamesE) == len(costE):
#	print('fáum dict')
costEdict = dict(zip(cityNamesE, costE))
# costE is a dictionary with names of cities attached 
	




# data framein sett upp til að bæt amegi í gagnagrunn. 
# So, for example, if a column is of type INTEGER and you try to insert a string into that column, SQLite will attempt to convert the string into an integer. If it can, it inserts the integer instead

nColumns = len(costIndexE.columns)
print(type(costIndexE.iloc[:, 2 : nColumns-1]))


# df contains columns called "city" and "rank"
def toNumeric(df):
	names = df.columns.tolist()
	names.remove("City")
	names.remove("Rank")
	for columnName in names:
		df[columnName] = pd.to_numeric(df[columnName])


cNames = costIndexE.columns.tolist()
cNames.remove("City")
cNames.remove("Rank")
print(cNames)
for columnName in cNames:
	costIndexE[columnName] = pd.to_numeric(costIndexE[columnName])

toNumeric(qualityE)
	


#costIndexE.iloc[:, 2 : nColumns-1].to_numeric
# allt nema Rank og City ætti að vera tölur núna 
# NEIB en skiptir ekki máli ?

def replaceEuro(df):
	for x in df.columns.tolist():
		df[x] = df[x].str.replace('€' , '')

for df in costE:
	replaceEuro(df)
 # evrutáknin ættu að vera farin úr töflunum í costTables 

print(costE[0]["Prices"])
print(cityNamesE[0])


con = sqlite3.connect("C:/Users/Valdi/Desktop/Ferdasja sumar/database.db")


# # data frameið sett í sqlite gagnagrunn:

# # dfin þurfa að hafa sömu dálkaheiti og töflurnar. 

costIndexE.to_sql("CostOfLivingIndex", con, if_exists="replace")
qualityE.to_sql("QualityOfLifeIndex", con, if_exists="replace")

# # indexatöflurnar hafa verið settar í sql

# for df in costE: 
# vil færa inn í prices
# en prices er með attribute fyrir hverja vöru, í 'goods'
# t.d. Banana 1kg 
# til að setja df í sql þurfa að vera sömu dálkaheiti, því það er búið til dict sem er hent inn 
	# Gæti ég tekið df-ið, og snúið því þ.a. df["Goods"] verði df.columns? 
	# get skrifað dict sem tengir df["Goods"] og dálkaheitin
# það sem ég vil gera: 

# fá töflu  
	# City      Meal Inexpensive    Meal for 2 mid-range 
	# Rvk          15					  85 
	
	
	# gerum ráð fyrir að þetta sé í sömu röð 
	# insert a
	
pricesAttributes = ["Meal Inexpensive" , "Meal for 2 mid-range three-course" , "McMeal" , "Domestic Beer 0.5L in Restaurant" ,"Imported Beer 0.33L Bottle in Restaurant" , "Cappucino" , "Coke/Pepsi" , "Water" , "Milk 1L" , "Bread 500g" , "Rice" , "Eggs 12" , "Cheese 1kg" , "Chicken Breast 1kg" , "Beef Round 1kg" , "Apples 1kg" , "Banana 1kg" , "Oranges 1kg" , "Tomato 1kg" , "Potato 1kg" , "Onion 1kg" , "Lettuce Head" , "Water 1.5L" , "Bottle of Wine" , "Domestic Beer Market 0.5L" , "Imported Beer Market 0.33L" , "Cigarettes" , "Transport One-Way" , "Monthly Pass" , "Taxi Start" , "Taxi 1km" , "Taxi 1hour Waiting" , "Gasoline 1L" , "Volkswagen Golf" , "Toyota Corolla" , "Basic Utilities" , "1min mobile" , "Internet" , "Fitness Club" , "Tennis Court Rent" , "Cinema" , "Preschool Month" , "Primary School Year" , "Jeans" , "Dress" , "Nike Shoes" , "Leather Shoes" ,"Rent 1 Bedroom Center" , "Rent 1 Bedroom Outside Center" , "Rent 3 Bedrooms Center" , "Rent 3 Bedrooms Outside Center" , "Price m2 Center", "Price m2 outside center", "Average Monthly Salary After Tax" , "Mortgage Interest Rate" ]

def afterComma(string):
	
	if string is not None:
		if len(string.split("-")) > 1:
			return string.split("-")[1] 
	
	
# Gögnin sett í gagnagrunn: 	

# removes first and last letter of string 
def removeFirst(string):
	return string[1:-1]
	
print(removeFirst("yobo"))



with con: 
	cur = con.cursor() 
	cityNumber = 0
	for city in fixNames(cityNamesE[0:numberOfCities]):
		# cityNumber cities have been added to the db. price and price range 
		
		
		prices = costE[cityNumber]["Prices"].values.tolist()
		
		prices = list(map(removeFirst,prices))
		prices.insert(0,city)
		print(prices)
		range = costE[cityNumber]["Range"]
		
		cityNumber += 1
		
		lowRange = list(map( lambda string: string.split("-")[0], range) )
		highRange = list(map(lambda x:  afterComma(x), range))
		lowRange.insert(0,city)
		lowRange.insert(1,0)
		highRange.insert(0,city)
		highRange.insert(1,1)
		if len(pricesAttributes) + 1 == len(prices):		
			# + 1 útaf city
			questionMarks = "?,"*(len(prices)-1)
			questionMarks += "?"
			values = tuple(prices)
			
			cur.execute("INSERT into Prices VALUES(" + questionMarks + ")", values)
			# verðgögnin komin inn í Prices 
			
			
			if len(lowRange) == len(highRange):
				
				# hendi fyrst út None sem er fyrir average salary því það er ekkert range
				
				# auka dálkur fyrir 'high/low"
				questionMarks += ",?"
				values= tuple(lowRange)
				# eyðum út 
				
				cur.execute("INSERT into PriceRange VALUES(" + questionMarks + ")", values)
				
				
				#highRange = [x for x in highRange if x is not 'None']
				values = tuple(highRange)
				cur.execute("INSERT into PriceRange VALUES(" + questionMarks + ")", values)
			# range gögnin komin inn í PriceRange 
		
		else:
			print("unequal lengths, not all attributes ")

			
			

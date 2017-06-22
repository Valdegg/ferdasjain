# prufur fyrir veðrið 


import requests
import json 
import pandas as pd 
import datetime
import time 
import sqlite3
import pickle 
import pycountry
from bs4 import BeautifulSoup



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
	
def beforeComma(string):
	return string.split(",")[0]

def afterComma(string):	
	if string is not None:
		if len(string.split(",")) > 1:
			return string.split(",")[1][1:] 
	

	#### Skilgreini dict á milli countries og WU codes 


country_to_iso = getHTMLTables("https://www.wunderground.com/weather/api/d/docs?d=resources/country-to-iso-matching&MR=1")
iso_codes = pd.concat(country_to_iso)


iso = iso_codes.to_dict()["ISO Code"]
print(len(iso_codes))
print(len(iso_codes["ISO Code"]))

# iso breytir tölu í iso code 
osi = {v: k for k, v in iso.items()}
# öfug vörpun 
wu = iso_codes.to_dict()["Wunderground Code"]
# wu[osi[ iso_code ] gefur wu code fyrir iso code 

with open("cityFix.txt", 'rb') as f:
	cityFix = pickle.load(f)
	
cityFix["Bolzano-Bozen"] = "00000.20.16020"
cityFix["The Hague (Den Haag)"] = "00000.12.06200"

# cityFix er dict sem úthlutar borg sem hafði sama nafn og aðrar borgir í planner apanum zmw kóða sem gerir kleift að finna veðrið í borginni 
	
# borg: strengur með landheiti og borg (fylki ef í US)
# dateFrom og dateTo:  strengur MMDD,   mest 30 dagar á milli
# output: weather predictions in borg on the era between dateFrom and dateTo. dictionary containing the information about weather , not weekday_short and all that craps
# if it failed, the city name is returned 
def weatherInCity(borg, dateFrom, dateTo):
	timabil = dateFrom + dateTo 
	base = "http://api.wunderground.com/api/e0d9599c3d3d3e3b/planner_"
	city = beforeComma(borg) 	
	#land = 	pycountry.countries.get(name= afterComma(borg))
	#wucode = wu[osi[ land.alpha_2 ] ]
	
	fyrirspurn = base + timabil + "/q/" + afterComma(borg) + "/" + city + ".json"
	print(fyrirspurn + "\n")
	
	response = requests.get(fyrirspurn)
	data = response.json()
	if len(data) > 1:
		# það eru 2 lyklar, 'response' og 'trip' í succesful fyrirspurnum 
		weatherData = data["trip"]
	
		# sleppum trip[period_of_record] en geymum rest 
		del weatherData["period_of_record"] 	

		return [borg, weatherData]
	else: 
		# g.r.f. að borgin sé ein af þeim sem búið er að skrifa í cityFix.txt
		zmw = cityFix[beforeComma(city)]
		fyrirspurn = base + timabil + "/q/" + "zmw:" + zmw + ".json"
		response = requests.get(fyrirspurn)	
		data = response.json()
		weatherData = data["trip"]
		# sleppum trip[period_of_record] en geymum rest 
		del weatherData["period_of_record"] 	

		return [borg, weatherData]
	

	
# use:  citiesWU = namesFix(citiesNumbeo)
# before: citiesNumbeo is a list of city names from a Numbeo table 
# after: citiesWU is the same list of names but with those names that had the wrong format for the WU API search now fixed so they work 

# returns a dictionary where keys are the cities, and values are the countries
def namesFixedForWU(cities):
	
	return cities 
	


# costIndexE = getHTMLTables("https://www.numbeo.com/cost-of-living/region_rankings.jsp?title=2017&region=150")[0]
# cityNamesE = list(map(beforeComma, costIndexE["City"]))


	
# with open("citiesEurope.txt", 'wb') as f:
	# pickle.dump(list(costIndexE["City"]), f)
# # citiesEurope.txt hefur landaheitin rétt eins og borgarheitin
	
	
#### nöfnin ættu núna að vera í citiesEurope.txt	svo nú þarf ekki að keyra þennan sækjanöfn hluta aftur 

with open("citiesEurope.txt", 'rb') as f:
	cities = pickle.load(f)

	
data = []
for city in cities[:12]: 
	# city inniheldur nafn borgar og lands, í data er veðrið fyrir borgirnar í cities[.. city]
	# nema það hafi verið fails þá er bara nafnið á borginni í data 

	data.append(weatherInCity(city,"0525","0530"))
	time.sleep(6)
	# geta verið margar borgir með sama nafn í sama landi !!! þá get ég úthlutað hverri fail-borg fylkinu sem hún er í. 
	
	
print(data)

# weather = []
# # geymir veðrið í borgunum sem virkuðu 
# cityFails = [] 
# # geymir borgirnar sem tókst ekki að ná í veðrið fyrir 
# for city in data: 
	# if type(city) == str:
		# cityFails.append(city)
	# else: 
		# weather.append(city)

#### í eftirfarandi kóða voru borgirnar sem feilaði að leita að fundnar og settar í cityFix.txt (zmw kóðinn): 
	# with open("cityFails.txt", 'rb') as f:
		# cityFails = pickle.load(f)
	# komið í skjal 
		
	
	
	# failIndex = [4, 5]  # index á borgirnar sem sem fengu engin svör  því hétu skrítnu nafni
	# vitlausNofn = [cityFails[i] for i in failIndex] # komu engin svör frá WU því þetta var rangt nafn 
	# failIndex.sort(reverse=True)

	# for i in failIndex: 
		# del cityFails[i]
	# #cityFails inniheldur ekki það sem hafði vitlaus nöfn heldur bara það sem var ónákvæmt

	# failStates= ["16", "LK", "AB", "FV",  "SR", "HH", "BNH", "CAM", "M", "BST", "C", "MAN", "GLG", "HAM", "NYK", "KS"]
	# failCodes = []
	# print(cityFails)
	# print("\n")

	# print(vitlausNofn)
	# reddad = False
	# i = 0
	# for city in cityFails:
		# fyrirspurn = base + timabil + "/q/" + afterComma(city) + "/" + beforeComma(city) + ".json"
		# response = requests.get(fyrirspurn)
		# data = response.json()["response"]["results"]
		# for city in data: 
			# if i < len(failStates) and city["state"] ==  failStates[i]:
				# failCodes.append( city["zmw"] )
				# reddad = True 
				# i += 1
		# if not reddad: 
			# print(data)
		# time.sleep(60/len(cityFails))
		# reddad = False
		
	# print(failCodes)



	# cityFix = dict(zip(list(map(beforeComma,cityFails[0:len(failCodes)])), failCodes)) # lykillinn er borgarheitið, valueið er ISO fyrir fylkið sem actual stórborgin er í


	# print("Bættu við restinni, sem var prentað í lykkjunni")
	# cityFix["Liverpool"] =  '00000.7.03316'
	# cityFix["Karlsruhe"] = "00000.80.10727"
	# cityFix["Leicester"] = '00000.78.03418'
	# cityFix["Leeds"] = '00000.27.03347'
	# cityFix["Nottingham"] = '00000.86.03354'
	# cityFix["Coventry"] = '00000.40.03541'
	# cityFix["Bilbao"] = '00000.496.08025'
	# cityFix["Cardiff"] = '00000.18.03717'
	# cityFix["Newcastle Upon Tyne"] = '00000.21.03246'
	# cityFix["Zaragoza"] = '00000.25.08160'
	# cityFix["Belfast"] = "00000.20.03924"
	# cityFix["Bremen"] = "00000.34.10945"
	# cityFix["Ljubljana"] = "00000.1.14015"
	# cityFix["Heraklion"] = "00000.1.16754"
	# cityFix["Valencia"] = "00000.68.08285"
	# cityFix["Rijeka"] = "00000.1.14216"
	# cityFix["Porto"] = "00000.18.08545"
	# cityFix["Coimbra"] = "00000.56.08548"
	# cityFix["Krakow"] = "00000.938.12566"
	# cityFix["Poznan"] = "00000.843.12330"
	# cityFix["Szczecin"] = "00000.35.12205"
	# cityFix["Lodz"] = "00000.102.12465"
	# cityFix["Skopje"] = "00000.113.13588"
	# cityFix["Iasi"] = "00000.133.15090"
	# cityFix["Chisinau"] = "00000.1.33815"
	# cityFix["Lviv"] = "00000.4.33393"

	# # cityFix inniheldur zmw kóða fyrir borgirnar sem fundust ekki þegar leitað var að borgarnafni og landi 
	# print(cityFix)


	# with open("cityFix.txt", "wb") as f:
		# pickle.dump(cityFix, f)
####		
	

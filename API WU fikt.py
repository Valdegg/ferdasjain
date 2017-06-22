# api fyrir Weather Underground 
# mun ná 

# To do : 
#	prófa að kalla á weatherInCity fyrir borginar í cities og sjá hvaða nöfn klikka
#	gera namesFixedForWU til að laga það 
#	prófa weatherAll
#	prófa fitWeatherCriteria
#	
#	






# Föll:
# weatherInCity(), citiesThatFit(), addWeatherToDFrame(), weatherAllWeeks(), weatherAllCities(), addWeatherToDB,   namesFixedForWU()

import requests
import json 

import pandas as pd 
import datetime
import time 

import sqlite3


# sql table stuff:

dbURL = "C:/Users/Valdi/Desktop/Ferdasja sumar/database.db"
con = sqlite3.connect(dbURL)
cur = con.cursor()

# db_df_W = pd.read_sql_table('WeatherEurope', con) # sæki weatherEurope úr dbURL yfir í dataframe 

# db_df_chances = pd.read_sql_table('WeatherChancesEurope', con) # sama fyrir chances 

# Sé til þess að nýju dfin og þau úr sql töflunni séu eins (sömu dálkaheiti og jafn margir dálkar):

wAttributes = list(map(lambda x: x[0] , con.execute('select * from WeatherEurope').description) )
cAttributes= list(map(lambda x: x[0] ,con.execute('select * from WeatherChancesEurope').description))




# city names: 

from scrape import getHTMLTables   
from scrape import beforeComma
costIndexE = getHTMLTables("https://www.numbeo.com/cost-of-living/region_rankings.jsp?title=2017&region=150")[0]
cityNamesE = list(map(beforeComma, costIndexE["City"]))


cities = namesFixedForWU(cities)


# 
	
# tests: 
# gögnin inn:
weatherdata = weatherInCity(cities[0],"0525", "0530") # testar fyrir staka borg 

dfs = weatherAllWeeks(cities[0]) # testar einum innra, náð í veðrið fyrir staka borg allt árið 

weatherAllCities(cities[0:3])  # testar "ysta" hluta # kröfur á gögnin:
# hvað væru röfur frá notanda? Ekki návæmar, að líkurnar áwindd ag sé < 20% 
# getum byrjað á No wind / windy day not so likely/ don't care 
# max 20% líkur á windy day  / ma x50% líkur / 
# munur er á líkum á t.d. vindi og hvort hann sé mikill. hægt að hafa kröfur um líkur og magn 

# Flokkum breyturar. . Vill ekki (vindur)   og vil ( sól). ÞÐð er  asmt mismunandi hvað fólk vill. 


# weatherInCity 

print(weatherInCity("Reykjavik", "0525", "0530"))

# MEGINMÁL FORRITSINS:

addWeatherToDB



# use:  citiesWU = namesFix(citiesNumbeo)
# before: citiesNumbeo is a list of city names from a Numbeo table 
# after: citiesWU is the same list of names but with those names that had the wrong format for the WU API search now fixed so they work 
def namesFixedForWU(cities):

# borg: strengur með landheiti og borg (fylki ef í US)
# dateFrom og dateTo:  strengur MMDD,   mest 30 dagar á milli
# output: weather predictions in borg on the era between dateFrom and dateTo. dictionary containing the information about weather , not weekday_short and all that craps
def weatherInCity(borg, dateFrom, dateTo):
	timabil = dateFrom + dateTo 
	base = "http://api.wunderground.com/api/e0d9599c3d3d3e3b/planner_"
	response = requests.get(base + timabil + "/q/" + borg + ".json")
	data = response.json()
	print(data.keys())
	weatherData = data["trip"]
	# sleppum trip[period_of_record] en geymum rest 
	del weatherData("period_of_record")

	return weatherData


# use: citiesThatFit = fitWeatherCriteria(criteria)
# before:
# criteria: dict of pairs (attribute, value)
        # something like (chanceofwindyday : (20%, max))
        # or (temp_high : (30, max)) or (temp_low : (10, min))
# weatherdata is stored in database with multiple results from Weather Underground Trip Planner, each of which is comes from calling weatherInCity(borg, dateFrom, dateTo)
# after: citiesThatFit is a list of the cities in weatherdata that fit the criteria
def fitWeatherCriteria(criteria, weatherdata):
	
	dbURL = "C:/Users/Valdi/Desktop/Ferdasja sumar/database.db"
	con = sqlite3.connect(dbURL)
	cur = con.cursor()
	
	db_df_W = pd.read_sql_table('WeatherEurope', con) # sæki weatherEurope úr dbURL yfir í dataframe 
	
	db_df_chances = pd.read_sql_table('WeatherChancesEurope', con) # sama fyrir chances 
	
	for crits in criteria: 
		
	
	# Í viðmótinu er ónákvæmt mat um veðrið. Það þarf þýðingu á milli
	critToNumbers # dict sem þýðir t.d. no wind í 0-max10% líkur á vind,  sunny í 
	minChanceOf # Listi af líkum fyrir breyturnar, minlíkur á t.d. sólardegi 
	maxchancesOf # Listi af líkum,  max líkur fyrir t.d. windy day. Dict svo hægt er að skrifa chanceOfMax["wind"] 
	minAmountOf # kröfur uum hámarks vindhraða eða klst af sól eða adgsljósi eða (?) mm rigningu 
	maxAmountOf
	
	with cur:
	# 
		
		# chances:
		select ciry  from WeatherChancesEurope where windy > chanceOfMin["wind"] &  windy < chanceOfMax["wind"] & ...
		
		# eather variables
	
		# búið er að ná í það sem uppfyllir úr gagnagrunninum, sem búið er að hlaða í
	# get notað þessi df? eða hef kannski bara sql inquiries

	
 
 # hleð fyrir hverja borg inn í df, sem er svo sett inn í gagnagrunninn (eftir að árið er komið fyrir borgina. tekur ca. 5 mín per borg)

 
# use: addWeatherToDFrame( df, weatherInCity )
# before: weatherInCity is a dictionary, e.g. weatherInCity(city, dateFrom, dateTo)
#	df is a dataframe that stores weather data (with columns city, week, chanceofwindyday, sunnyday, etc, same as in WeatherEurope and WeatherChancesEurope sqlite tables
# after: df 
def addWeatherToDFrame(df, weatherInCity)
	# 
	# df.addRow(weatherInCity
	df.concat([df, pd.DataFrame.from_dict(weatherInCity)]
	
# notkun: dfs = weatherAllWeeks(city)
# before: city er borgarnafn sem virkar í WU apann (gæti þurft að snyrta til áður en kallað er á)
# after: dfs is a list with 2 dataframes (weather and chances)  with 52 rows with the weather from WU for all weeks of the year for the city 
def weatherAllWeeks(city):
	
	dfWeather = pd.DataFrame(index="city", columns = wAttributes)
	dfChances = pd.DataFrame(index="city", columns = cAttributes)
	
	# dataframes with space for 52 weeks has been created 
	
	# get búið til dataframeið upprunalega mþa gera from_dict(weatherInWeek)
	
	dateOfVacation = datetime.date(2017,1,1)
	
	print(dateOfVacation.strftime("%m%d"))
	oneWeek = datetime.timedelta(weeks=1)
	
	# weatherInWeek = weatherInCity(city, dateOfVacation.strftime("%m%d"), (dateOfVacation+oneWeek).strftime("%m%d"))	
	# # is a dict 
	
	# dataframe = pd.from_dict(weatherInWeek)
	# dateOfVacation += oneWeek 
	
	numberOfWeeks = 0
	while( numberOfWeeks < 52 ):   # prófum fyrst <1 í prufukeyrslu
		# weather data for the first numberOfWeeks weeks has been added to dfWeather and dfChances
		# at least numberOfWeeks*7 seconds have passed 
		
		weatherInWeek = weatherInCity(city, dateOfVacation.strftime("%m%d"), (dateOfVacation+oneWeek).strftime("%m%d"))
		
		addWeatherToDFrame(dfChances, weatherInWeek["chance_of")
		del weatherInWeek["chance_of"]
		addWeatherToDFrame(dfWeather, weatherInWeek)
		
		
		# prófa prófa prófa 
		
		dateOfVacation += oneWeek 
		numberOfWeeks += 1 		
		time.sleep(7)
	
	return [dfWeather, dfChances]
	
	-
	# use: df = weatherAllCities(cities)
	# before: cities is a list of citynames, short list since it takes time
	# after: citynames have been searched for in the WU API and added to df which has the weather attributes as columns 
	# then it's possible to just df.to_sql()
# eða bæti bara í gagnagrunninn?
def weatherAllCities(cities):

# Köllum bara á fyrir litla lista 	
	
	
	# laga cities að WU nöfnunum
		# gert inni í namesFixedForWU
	for city in cities:
		allW = weatherAllWeeks(city)
		addWeatherToDB(allW)
		

	

# búum til gagnagrunninn í python frekar en í sqlite3.exe	

	# before: til er sqlite3 database 'database.db' í möppunni, með eigindi temp_high.min o.s.frv 
	# og database_uppsetning.py hefur verið keyrt 
	# dfs is a list of dataframes with same column names as attributes in the database, e.g. output from weatherAllWeeks
	# after: the data from dfs has been added to the two weather tables in database.db 
def addWeatherToDB(dfs):
		

	
	# db_df_W = pd.read_sql_table('WeatherEurope', con) # sæki weatherEurope úr dbURL yfir í dataframe 
	
	# db_df_chances = pd.read_sql_table('WeatherChancesEurope', con) # sama fyrir chances 
	
	# Sé til þess að nýju dfin og þau úr sql töflunni séu eins (sömu dálkaheiti og jafn margir dálkar):
	

	setW = set(wAttributes)
	setC = set(cAttributes)
	# same names?
	if setW == set(df[0].columns.tolist)
		# same attributes
		# newWDF = DataFrame.concat([db_df_W, dfs[0]])# bæti weather úr dfs í db_df_W
		df[0].to_sql("WeatherEurope", con, if_exists='append')
	else:
		print(df[0].columns.tolist)			
	if setC =  set(df[1].columns.tolist)
		# newChancesDF = DataFrame.concat([db_df_chances, dfs[1]])# bæti chances úr dfs í db_df_chances
		df[1].to_sql("WeatherEurope", con, if_exists='append')
	else: 
		print( df[1].columns.tolist )
		
	
	
	# yfirskrifar to_sql eða bætir við nýjum röðum? ef bætir við þá þarf ekki þetta concat dæmi 
	# if_exists = 'append' reddar þessu,   concatið	
	
	
	# 
	
	# breyti og bæti
	
	# erum með: 
	# trip: 
		# temp_high:
			# min: 'C'
			# avg:
			# max: 
		# temp_low:
			# -""-
		# precip: 
			# min: 'cm'
			# avg: 
			# max: 
		# dewpoint_high:
			# min: 'C'
			# avg: 
			# max:
		# dewpoint_low:
			# -""-
		# cloud_cover: 
			# 'cond':
			
		# chance_of: 
			# tempoversixty: 
				# name: 'warm'
				# description: 
				# percentage: 
			# chanceofwindyday: 
				# -""-
			# chanceofpartlycloudyday
				# -""-
			# chanceofsunnycloudyday
			# chanceofhumidday
			# chanceoffogday:
			# chanceofprecip:
			# tempoverninety:
				# name: 'Hot' 
				# -""-
			# chanceofrainday: 
			# chanceofcloudyday: 
			# chanceofsnowonground:
			# chanceofsultryday:
				# description: dew point over 21
			# tempbelowfreezing: 
			# tempoverfreezing: 
			# chanceofsnowday:
			
# use: string = formatWUAPI(date) 
# before: date is a date 
# after: string is the day and month from date in format MMDD
def formatWUAPI(date):
	# notum bara strftime
	
	
			
	








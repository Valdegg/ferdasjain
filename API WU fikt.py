# api test fyrir Weather Underground 
# mun ná 

print("yo")
import requests
import json 


base = "http://api.wunderground.com/api/e0d9599c3d3d3e3b/planner_"

# example: http://api.wunderground.com/api/e0d9599c3d3d3e3b/planner_07010731/q/CA/San_Francisco.json

timabil = "05100517";
# timabil er táknað MMDDMMDD

borg = "CA/San_Francisco"
borg = "UK/London"
borg = "IS/Reykjavik"

response = requests.get(base + timabil + "/q/" + borg + ".json")
print(response.status_code)
print(response.content)

data = response.json()
print(type(data))
print(data)

print(response.headers)

print(data["trip"]["temp_high"])



temp_high = data["trip"]["temp_high"]	
chance_of = data["trip"]["chance_of"]

co = "chanceof"
print(chance_of[ co + "humidday" ]["percentage"])


# borg: strengur með landheiti og borg (fylki ef í US)
# dateFrom og dateTo:  strengur MMDD,   mest 30 dagar á milli
# output: weather predictions in borg on the era between dateFrom and dateTo
def weatherInCity(borg, dateFrom, dateTo):
	timabil = dateFrom + dateTo 
	base = "http://api.wunderground.com/api/e0d9599c3d3d3e3b/planner_"
	response = requests.get(base + timabil + "/q/" + borg + ".json")
	data = response.json()
	print(type(data))
	print(data)
	print(response.headers)
	print(data["trip"]["temp_high"])

	temp_high = data["trip"]["temp_high"]	
	chance_of = data["trip"]["chance_of"]


# use: citiesThatFit = fitWeatherCriteria(criteria,weatherdata)
# criteria: dict of pairs (attribute, value)
        # something like (chanceofwindyday, (20%, max))
        # or (temp_high, (30, max)) or (temp_low, (10, min))
# weatherdata:  data with multiple results from Weather Underground Trip Planner
# output: citiesThatFit is a list of the cities in weatherdata that fit the criteria
def fitWeatherCriteria(criteria, weatherdata):
                        

 

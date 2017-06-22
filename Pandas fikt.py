import pandas as pd 
import sqlite3
pd.set_option('display.mpl_style', 'default') # gerir gröf fallegri
#figsize(15,5)

broken_df = pd.read_csv('C:/Users/Valdi/Google Drive/Sumar 2017/Pandas tutorial/bikes.csv')
print(type(broken_df))	
print(broken_df[:3])

fixed_df = pd.read_csv('C:/Users/Valdi/Google Drive/Sumar 2017/Pandas tutorial/bikes.csv', parse_dates=['Date'], dayfirst=True, index_col='Date')


# pandas cookbok tutorial 2 


pd.set_option('display.mpl_style', 'default') 
pd.set_option('display.width', 5000) 
pd.set_option('display.max_columns', 60) 


worldCities = pd.read_csv('world_cities.csv')
print(worldCities["lat"][20:25])
#print(worldCities["country"])
print(worldCities[['country', 'lat']][100:120])
print(worldCities['country'].value_counts()[1:10])
mostCities = worldCities['country'].value_counts()[1:10]
mostCities.plot(kind='bar')
print(worldCities['country']=="Denmark")
danishCities = worldCities[worldCities['country']=="Denmark"]
print(danishCities)
print(danishCities[danishCities['lng']==max(danishCities['lng'])])
print(danishCities[danishCities['lng']==min(danishCities['lng'])])

#print(type(danishCities[0:3]['population']))
over50k = worldCities['pop'] > 50000
isDanish = worldCities['country']=="Denmark"
bigCitiesDK = worldCities[over50k & isDanish]

print(bigCitiesDK['city'].values=="Aalborg")
print(pd.Series([1,2,3]).values)

print(bigCitiesDK['province'].value_counts())
print(type(bigCitiesDK[bigCitiesDK['city_ascii']=='Kobenhavn']['pop']))

print(bigCitiesDK[bigCitiesDK['city_ascii']=='Kobenhavn']['pop'].values)

print(bigCitiesDK['pop']/bigCitiesDK[bigCitiesDK['city_ascii']=='Kobenhavn']['pop'].values)
# kemur NaN 
#print(worldCities['country'])



print(fixed_df[:5])
berri_bikes = fixed_df[['Berri1']]

print(len(berri_bikes.index.values))
print(berri_bikes.index.weekday)
berri_bikes['weekday'] = berri_bikes.index.weekday
weekdayCount = berri_bikes.groupby('weekday').aggregate(min)
weekdayCount.index = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
print(weekdayCount)
weekdayCount.plot(kind='bar')

#print( berri_bikes.values==max(berri_bikes))

print(worldCities['country'].unique())
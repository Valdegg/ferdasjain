# sqlite3 gagnagrunns uppsetning
# sjá sqlite3 python á heimasíðu sqlite3
import sqlite3

con = sqlite3.connect("C:/Users/Valdi/Desktop/Ferdasja sumar/database.db")




with con: 

	cur = con.cursor()
	cur.execute("DROP TABLE Prices")
	cur.execute("DROP TABLE PriceRange")
	#cur.execute("CREATE TABLE WeatherEurope(city text, week date, temp_low_avg integer, temp_low_min integer, temp_low_max integer, temp_high_avg integer, temp_high_min integer, temp_high_max integer, precipitation_avg integer,  precipitation_min integer,  precipitation_max integer, dewpoint_high_avg integer, dewpoint_high_min integer, dewpoint_high_max integer, dewpoint_low_avg integer, dewpoint_low_min integer, dewpoint_low_max integer, cloud_cover text)")
	
	# WeatherEurope inniheldur spár um hita, úrkomu, rakastig
	# week er byrjunardagsetning vikunnar sem spáin gildir í 
	#cur.execute('CREATE TABLE WeatherChancesEurope(city text, week date, "temp over sixty" integer, "temp over ninety" integer, "temp below freezing" integer, "temp over freezing" integer, windy integer, "partly cloudy" integer, "sunny cloudy" integer, cloudy integer,  humid integer, fog integer, precipitation integer, rain integer, snow integer, "snow on ground" integer, sultry integer, thunder integer, tornado integer, hail integer)')
	# WeatherChancesEurope inniheldur líkindi í prósentum á að dagur í vikunni hafi tilteki ðveður, t.d. windyday, tempoversixty
	
	cur.execute('Create table Prices(City text, "Meal Inexpensive" real, "Meal for 2 mid-range three-course" real, "McMeal" real, "Domestic Beer 0.5L in Restaurant" real,"Imported Beer 0.33L Bottle in Restaurant" real, "Cappucino" real, "Coke/Pepsi" real, Water real, "Milk 1L" real, "Bread 500g" real, "Rice" real, "Eggs 12" real, "Cheese 1kg" real, "Chicken Breast 1kg" real, "Beef Round 1kg" real, "Apples 1kg" real, "Banana 1kg" real, "Oranges 1kg" real, "Tomato 1kg" real, "Potato 1kg" real, "Onion 1kg" real, "Lettuce Head" real, "Water 1.5L" real, "Bottle of Wine" real, "Domestic Beer Market 0.5L" real, "Imported Beer Market 0.33L" real, "Cigarettes" real, "Transport One-Way" real, "Monthly Pass" real, "Taxi Start" real, "Taxi 1km" real, "Taxi 1hour Waiting" real, "Gasoline 1L" real, "Volkswagen Golf" real, "Toyota Corolla" real, "Basic Utilities" real, "1min mobile" real, "Internet" real, "Fitness Club" real, "Tennis Court Rent" real, "Cinema" real, "Preschool Month" real, "Primary School Year" real, "Jeans" real, "Dress" real, "Nike Shoes" real, "Leather Shoes" real,"Rent 1 Bedroom Center" real, "Rent 1 Bedroom Outside Center" real, "Rent 3 Bedrooms Center" real, "Rent 3 Bedrooms Outside Center" real, "Price m2 Center" real, "Price m2 Outside Center" real,  "Average Monthly Salary After Tax" real, "Mortgage Interest Rate" real)')
	
	# PriceRange:  2 rows for every city. if high = 1, upper boundary of range, if hilo = 0, lower boundary of range 
	cur.execute('Create table PriceRange(city text, hilo integer, "Meal Inexpensive" real, "Meal for 2 mid-range three-course" real, "McMeal" real, "Domestic Beer 0.5L in Restaurant" real,"Imported Beer 0.33L Bottle in Restaurant" real, "Cappucino" real, "Coke/Pepsi" real, Water real, "Milk 1L" real, "Bread 500g" real, "Rice" real, "Eggs 12" real, "Cheese 1kg" real, "Chicken Breast 1kg" real, "Beef Round 1kg" real, "Apples 1kg" real, "Banana 1kg" real, "Oranges 1kg" real, "Tomato 1kg" real, "Potato 1kg" real, "Onion 1kg" real, "Lettuce Head" real, "Water 1.5L" real, "Bottle of Wine" real, "Domestic Beer Market 0.5L" real, "Imported Beer Market 0.33L" real, "Cigarettes" real, "Transport One-Way" real, "Monthly Pass" real, "Taxi Start" real, "Taxi 1km" real, "Taxi 1hour Waiting" real, "Gasoline 1L" real, "Volkswagen Golf" real, "Toyota Corolla" real, "Basic Utilities" real, "1min mobile" real, "Internet" real, "Fitness Club" real, "Tennis Court Rent" real, "Cinema" real, "Preschool Month" real, "Primary School Year" real, "Jeans" real, "Dress" real, "Nike Shoes" real, "Leather Shoes" real,"Rent 1 Bedroom Center" real, "Rent 1 Bedroom Outside Center" real, "Rent 3 Bedrooms Center" real, "Rent 3 Bedrooms Outside Center" real, "Price m2 Center" real, "Price m2 Outside Center" real, "Average Salary After Tax" text, "Mortgage Interest Rate" real)')
# er með ótal borgir og ótal tölur. Hef sér töflu PriceRanges
# og eigindi City og svo allt saaman 
	# cur.execute("Create table CostOfLivingIndex(City text, 'Cost Of Living Index' real, 'Rent Index' real, 'Cost Plus Rent Index' real, 'Groceries Index' real, 'Restaurant Price Index' real, 'Local Purchasing Power Index' real)")
	# cur.execute("Create table QualityOfLifeIndex(City text, 'Quality Of Life Index' real, 'Purchasing Power Index' real, 'Safety Index' real, 'Health Care Index' real, 'Cost Of Living Index' real, 'Property Price To Income Ratio' real, 'Traffic Commute Time Index' real, 'Pollution Index' real, 'Climate Index' real)")


		
		
	# erum með úr WU : 
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



def get_crime(cursor):
	crime = {}
	cursor.execute("SELECT * from crime")
	rows = cursor.fetchall()
	for row in rows:
		crime[row[0]] = row[1]
	return crime

def get_cities(cursor):
	city = {}
	cursor.execute("SELECT * from cities")
	rows = cursor.fetchall()
	for row in rows:
		city[row[0]] = row[1]
	return city

def get_walk(cursor):
	walk = {}
	cursor.execute("SELECT * from walk")
	rows = cursor.fetchall()
	for row in rows:
		walk[row[0]] = row[1]
	return walk

def get_school(cursor): 
	school = {}  
	cursor.execute("SELECT zip, score_median from schools")
	rows = cursor.fetchall()
	for row in rows:
		school[row[0]] = row[1]
	return school

def get_sales(cursor):
	sales = {}  
	cursor.execute("SELECT * from sales")
	rows = cursor.fetchall()
	for row in rows:
		sales[row[0]] = row[1]
	return sales

def get_rent(cursor):
	rent = {}  
	cursor.execute("SELECT * from rent")
	rows = cursor.fetchall()
	for row in rows:
		rent[row[0]] = row[1]
	return rent

def get_polygon(cursor):
	polygon = {}
	cursor.execute("SELECT * from polygon_big")
	rows = cursor.fetchall()
	for row in rows:
		array_huge = []
		array = []
		coords = row[1][2:-2].split('),(')
		i = 0
		match_num = 1000000
		first_coord = ''
		for coord in coords:
			i += 1
			longlat = coord.split(',')
			if coord == first_coord:
				match_num = i
			if i == match_num+2:
				array = []
				first_coord = coord
			if i == 1:
				first_coord = coord
			if i != match_num+1:  
				longlat[0] = float(longlat[0])
				longlat[1] = float(longlat[1])
				array.append(longlat)
			if i == match_num+1:
				array_huge.append(array)
		polygon[row[0]] = array_huge
	return polygon

def get_commute(cursor,zip):
	commute = {}
	cursor.execute("SELECT destination, time from dist_matrix WHERE origin = %s",(zip))
	rows = cursor.fetchall()
	for row in rows:
		commute[row[0]] = int(row[1])
	return commute
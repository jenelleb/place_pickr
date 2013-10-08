from flask import render_template, flash, redirect, url_for
from app import app
from forms import LoginForm
from flask import request
import MySQLdb
import sys
import numpy
import json
import scipy.stats
import db_functions
import scoring_functions

@app.route('/', methods = ['POST', 'GET'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		zip1 = form.zip1.data.split(',')[0]
		zip2 = form.zip2.data.split(',')[0]
		print zip1, zip2
		return redirect(url_for('results',zip1=zip1,zip2=zip2,housing=form.housing.data))
	return render_template('login.html',
		title = 'Zip Codes',
		form = form)

@app.route('/slideshow')
def slideshow():
	return render_template('slideshow.html')


@app.route('/results/<zip1>_<zip2>_<housing>')
def results(zip1,zip2,housing):  
# Map missing zip codes
	zip_mapping = {}
	zip_mapping['94597'] = '94596'
	zip_mapping['94582'] = '94583'
	zip_mapping['94551'] = '94550'
	zip_mapping['94528'] = '94526'
	zip_mapping['94503'] = '94589'
	zip_mapping['94531'] = '94509'
	zip_mapping['94534'] = '94585'
	zip_mapping['94085'] = '94086'
	zip_mapping['94599'] = '94558'
	zip_mapping['94305'] = '94301'
	zip_mapping['94720'] = '94704'
	
	zip1_orig = zip1
	zip2_orig = zip2
	if zip1 in zip_mapping:
		zip1 = zip_mapping[zip1]
	if zip2 in zip_mapping:
		zip2 = zip_mapping[zip2]
  
# Get data from database
  	db=MySQLdb.connect(user="root",db="zip_codes")
  	cursor=db.cursor()
  	crime = db_functions.get_crime(cursor)
  	walk = db_functions.get_walk(cursor)
  	school = db_functions.get_school(cursor)
  	sales = db_functions.get_sales(cursor)
  	rent = db_functions.get_rent(cursor)
  	city = db_functions.get_cities(cursor)
  	commute1 = db_functions.get_commute(cursor,zip1)
  	commute2 = db_functions.get_commute(cursor,zip2)
  	polygon = db_functions.get_polygon(cursor)
  		
# Calculate z_scores
  	crime_z = scoring_functions.zscore(crime)
  	walk_z = scoring_functions.zscore(walk)
  	school_z = scoring_functions.zscore(school)
  	sales_z = scoring_functions.zscore(sales)
  	rent_z = scoring_functions.zscore(rent)
  	commute1_z = scoring_functions.zscore(commute1)
  	commute2_z = scoring_functions.zscore(commute2)
  	
# Select rent or buy
	if housing == 'rent':
		price = {}
		zip_scores = scoring_functions.score_zips(crime_z,walk_z,school_z,rent_z,commute1_z,commute2_z)
		price_pcntl = scoring_functions.percentile_low(rent)
		for zip in sales.keys():
			price[zip] = int(rent[zip])
		price_z = rent_z
		housing_title = "Rent (1000 sqft)"
	if housing == 'buy':
		price = {}
		zip_scores = scoring_functions.score_zips(crime_z,walk_z,school_z,sales_z,commute1_z,commute2_z)
		price_pcntl = scoring_functions.percentile_low(sales)
		for zip in sales.keys():
			price[zip] = str(int(sales[zip]/1000)) + "K"
		price_z = sales_z
		housing_title = "House (2 Bed)"
    
# Calculate percentiles
	score_pcntl = scoring_functions.percentile_score(zip_scores)
  	commute1_pcntl = scoring_functions.percentile_low(commute1)
  	commute2_pcntl = scoring_functions.percentile_low(commute2)
  	school_pcntl = scoring_functions.percentile_high(school)
  	walk_pcntl = scoring_functions.percentile_high(walk)
  	crime_pcntl = scoring_functions.percentile_low(crime)
  	safety = scoring_functions.calc_safety(crime)
  	
# Calculate job coordinates	
  	zip1_lnglat = scoring_functions.calc_ave_lnglat(zip1,polygon[zip1])
  	zip2_lnglat = scoring_functions.calc_ave_lnglat(zip2,polygon[zip2])
  
# Make json object
  	zip_codes = []
  	for i in range(0,222):
		zip = zip_scores[i][0]
		commute1_mins = int(commute1[zip]/60)
		commute2_mins = int(commute2[zip]/60)
		zip_codes.append(
		{'zip':zip,'score':zip_scores[i][1],'score_pcntl':score_pcntl[zip],'city':city[zip],
		'crime':safety[zip],'crime_z':crime_z[zip],'walk':float(walk[zip])/10.0,'walk_z':walk_z[zip],
		'commute1':commute1[zip],'commute1_z':commute1_z[zip],'commute2':commute2[zip],
		'commute2_z':commute2_z[zip],'school':school[zip],'school_z':school_z[zip],
		'price':price[zip],'price_z':price_z[zip],'commute1_mins':commute1_mins,
		'commute2_mins':commute2_mins,'polygon':polygon[zip],'commute1_pcntl':commute1_pcntl[zip],
		'commute2_pcntl':commute2_pcntl[zip],'crime_pcntl':crime_pcntl[zip],'school_pcntl':school_pcntl[zip],
		'walk_pcntl':walk_pcntl[zip],'price_pcntl':price_pcntl[zip]}
		)
  
  	return render_template("results.html",
    	title = 'Results',
    	zip_codes = zip_codes,
    	jsonstr = json.dumps(zip_codes),
    	zip1 = zip1_orig,
    	zip2 = zip2_orig,
    	housing_title = housing_title,
    	zip1_lng = zip1_lnglat[0],
    	zip1_lat = zip1_lnglat[1],
    	zip2_lng = zip2_lnglat[0],
    	zip2_lat = zip2_lnglat[1])

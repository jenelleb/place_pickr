import numpy
import scipy

def score_zips(crime_z,walk_z,school_z,housing_z,commute1_z,commute2_z):
	score = {}
	zip_scores = {}
	for zip in crime_z.keys():
		score[zip] = -crime_z[zip]+walk_z[zip]+school_z[zip]-housing_z[zip]-2*commute1_z[zip]-2*commute2_z[zip]-2*abs(commute1_z[zip]-commute2_z[zip])
	i = 0
	for tuple in sorted(score.items(), key=lambda x:x[1], reverse = True):
		zip_scores[i] = tuple
		i += 1
	return zip_scores

def zscore(dict):
	zscores = {}
	scores_post = {}
	mean = numpy.mean(dict.values())
	std = numpy.std(dict.values())
	for zip in dict.keys():
		zscore = (dict[zip] - mean)/std
		if abs(zscore) < 3:
			scores_post[zip] = dict[zip]
	mean_fix = numpy.mean(scores_post.values())
	std_fix = numpy.std(scores_post.values())
	for zip in dict.keys():
		zscore_final = (dict[zip] - mean_fix)/std_fix
		zscores[zip] = zscore_final
	return zscores
    
def percentile_score(score):
	score_pcntl = {}
	score_array = []
	for (a,b) in score.values():
		score_array.append(b)
	for (a,b) in score.values():
		zip = a
		pcntl = scipy.stats.percentileofscore(score_array,b)/100
		score_pcntl[zip] = pcntl
	return score_pcntl
    
def percentile_low(feat):
	score_pcntl = {}
	for zip in feat.keys():
		pcntl = scipy.stats.percentileofscore(feat.values(),feat[zip])/100
		if pcntl > 0.66:
			score_pcntl[zip] = 'low'
		if pcntl <= 0.66 and pcntl > 0.33:
			score_pcntl[zip] = 'medium'
		if pcntl <= 0.33:
			score_pcntl[zip] = 'high'
	return score_pcntl
      
def percentile_high(feat):
	score_pcntl = {}
	for zip in feat.keys():
		pcntl = scipy.stats.percentileofscore(feat.values(),feat[zip])/100
		if pcntl > 0.66:
			score_pcntl[zip] = 'high'
		if pcntl <= 0.66 and pcntl > 0.33:
			score_pcntl[zip] = 'medium'
		if pcntl <= 0.33:
			score_pcntl[zip] = 'low'
	return score_pcntl    
    
def calc_safety(crime):
	safety = {}
	for zip in crime.keys():
		safety[zip] = 11-crime[zip];
	return safety
    
def calc_ave_lnglat(zip,coords):
	coords_first = coords[0]
	long = []
	lat = []
	lnglat = []
	for coord in coords_first:
		long.append(coord[0])
		lat.append(coord[1])
	long_ave = numpy.mean(long)
	lat_ave = numpy.mean(lat)
	lnglat.append(long_ave)
	lnglat.append(lat_ave)
	return lnglat
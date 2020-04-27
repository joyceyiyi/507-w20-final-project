from bs4 import BeautifulSoup
import requests
import sqlite3
import json

#base_url = "https://spotcrime.com/mi/ann+arbor/daily"
def open_cache():
    try:
        cache_file = open(CACHE_FILENAME,'r')
        cache_contents = cache_file.read()
        cache_dict = json.loads(cache_contents)
        cache_file.close()
    except:
        cache_dict = {}
    return cache_dict

def save_cache(cache_dict):
    dumped_json_cache = json.dumps(cache_dict)
    fw = open(CACHE_FILENAME,"w")
    fw.write(dumped_json_cache)
    fw.close()

def build_crime_url_dict():
	base_url = "https://spotcrime.com"
	response = requests.get(base_url+"/mi/ann+arbor/daily")
	soup = BeautifulSoup(response.text, 'html.parser')
	lists = soup.find(class_='list-unstyled').select('li')
	crime_dict = {}
	for l in lists:
		a = l.select('a')[0]
		crime_dict[a.string.split(" ")[0]]=base_url+a.attrs['href']
	return crime_dict

def date_convertor(d_str):
	m,d,y = d_str.split('/')
	y = '20'+y[:-1]
	m = y+'-'+m
	d = m+'-'+d
	return y,m,d

def get_crime_detail(crime_dict):
	crimes = []
	crime_type = set()
	for key in crime_dict:
		crime_case_url = crime_dict[key]
		if crime_case_url in CACHE_DICT.keys():
			text = CACHE_DICT[crime_case_url]
		else:
			response = requests.get(crime_case_url)
			text = response.text
			CACHE_DICT[crime_case_url] = text
			save_cache(CACHE_DICT)

		soup = BeautifulSoup(text,'html.parser')
		cases = soup.find(class_="table table-condensed table-striped table-hover text-left").select('tr')
		for i in range(1,len(cases)):
			case = cases[i]
			crimes.append({})
			items = case.select('td')
			try:
				crimes[-1]['index']=key+items[0].string
				crimes[-1]['type']=items[1].string
				crime_type.add(items[1].string)
				datetime = items[2].string.split(" ")
				crimes[-1]['date'] = datetime[0]
				crimes[-1]['year'],crimes[-1]['month'],crimes[-1]['day'] = date_convertor(datetime[0])
				crimes[-1]['hour'] = datetime[1].split(":")[0]
				crimes[-1]['address']=items[3].string
				crimes[-1]['link']="https://spotcrime.com"+case.select('a')[0].attrs['href']
			except TypeError as e:
				crimes.pop()
		print(key)
	return crimes,crime_type

def count_daily_crime(crimes,crime_type):
	count_crime = {}
	for case in crimes:
		date = case['date']
		if date in count_crime:
			count_crime[date][case['type']]+=1
		else:
			count_crime[date]={}
			for cat in crime_type:
				count_crime[date][cat]=0
	return count_crime


def create_connection(db_file):
	conn = None
	try:
		conn = sqlite3.connect(db_file)
	except Error as e:
		print(e)
	return conn

def create_crime_case(conn,case):
	sql = "INSERT INTO Crimes(Id,Type,Dates,Year,Month,Day,Hour,Address,Link)\
			VALUES(?,?,?,?,?,?,?,?,?)"
	cur = conn.cursor()
	cur.execute(sql,case)


def create_daliy_stats(conn,count):
	sql = "INSERT INTO DailyStats(Dates,Vandalism, Assault, Burglary, Robbery, Theft, Other, Arrest, Shooting)\
			VALUES(?,?,?,?,?,?,?,?,?)"
	cur = conn.cursor()
	cur.execute(sql,count)

def main():
	crime_dict = build_crime_url_dict()
	crimes,crime_type = get_crime_detail(crime_dict)
	count_crime = count_daily_crime(crimes,crime_type)
	print(crime_type)

	db_file = 'crime.db'
	conn = create_connection(db_file)
	with conn:
		for crime in crimes:
			case = (crime['index'],crime['type'],crime['date'],crime['year'],crime['month'],crime['day'],crime['hour'],crime['address'],crime['link'])
			create_crime_case(conn,case)
		for date in count_crime.keys():
			stats = count_crime[date]
			count = (date,stats['Vandalism'],stats['Assault'],stats['Burglary'],stats['Robbery'],stats['Theft'],stats['Other'],stats['Arrest'],stats['Shooting'])
			create_daliy_stats(conn,count)

CACHE_FILENAME = 'cache.json'
CACHE_DICT = open_cache()
if __name__=="__main__":
	main()


#print(len(crimes))


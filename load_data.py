import requests
from app import db
from models import Clinics, Quartet
import sys
import json
import random

def store_in_db(items, model):
	for d in items['data']:
		record = model(d)
		try:
			old_record=model.query.filter(\
				       model.name_1 == record.name_1 ,\
			 		   model.street_1 == record.street_1,\
			  		   model.city == record.city ,\
			  		   model.zip==record.zip).first()

			if old_record != None:
				for k in old_record.__dict__.keys():
					if k != 'id':
						setattr(old_record, k, getattr(record, k))
			else:
				db.session.add(record)
			db.session.commit()
		except:
			db.session.rollback()
			raise
		finally:
			db.session.close()

		

def get_data():
	items = {'data': []}
	base_url = "https://data.cityofnewyork.us/resource/8nqg-ia7v.json"
	print("Fetching data from " + base_url)
	r = requests.get(base_url).json()
	items['data'].extend(r)
	#print('Number of data found is ' + str(len(r)))

	return items



def init_quartet():
	items = {'data': []}
	base_url = "https://data.cityofnewyork.us/resource/8nqg-ia7v.json"
	print("Initializing quartet db ...")
	r = requests.get(base_url).json()
	items['data'].extend(random.sample(r, 100))

	return items

def batch_load():
    clinics_items = get_data()
    store_in_db(clinics_items, Clinics)

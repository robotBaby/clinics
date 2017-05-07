from app import db
from sqlalchemy.dialects.postgresql import JSON
import collections
import hashlib



class Clinics(db.Model, object):
    __tablename__ = 'clinics'
    id = db.Column(db.Integer, primary_key=True)
    name_2 = db.Column(db.String())
    name_1 = db.Column(db.String())
    city = db.Column(db.String())
    latitude = db.Column(db.String())
    longitude = db.Column(db.String())
    zip = db.Column(db.String())
    street_1 = db.Column(db.String())
    street_2 = db.Column(db.String())
    phone = db.Column(db.String())
    active = db.Column(db.Integer)
    
    def __init__(self, json):
        for key in json:
            setattr(self, key, json[key].lower())
        unique_string = json['name_1'].lower() +json['street_1'].lower()+ json['city'].lower() +json['zip'].lower()
        hashed_string = abs(hash(unique_string))%10**8
        setattr(self, 'id', hashed_string)
        #setattr(self, 'active', 0)
        active=Quartet.query.filter(\
           Quartet.name_1 == json['name_1'].lower() ,\
           Quartet.street_1 == json['street_1'].lower(),\
           Quartet.city == json['city'].lower() ,\
           Quartet.zip==json['zip'].lower()).first()
        setattr(self, 'active', int(active!=None))


class Quartet(db.Model, object):
    __tablename__ = 'quartet'
    id = db.Column(db.Integer, primary_key=True)
    name_2 = db.Column(db.String())
    name_1 = db.Column(db.String())
    city = db.Column(db.String())
    zip = db.Column(db.String())
    street_1 = db.Column(db.String())
    street_2 = db.Column(db.String())
    

    def __init__(self, json):
        for key in json:
            setattr(self, key, json[key].lower())
        unique_string = json['name_1'].lower() +json['street_1'].lower()+ json['city'].lower() +json['zip'].lower()
        hashed_string = abs(hash(unique_string))%10**8
        setattr(self, 'id', hashed_string)


   

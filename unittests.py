# Unit tests that check if the classes and methods are working as intended
from flask import Flask, render_template, jsonify, request
from flask.ext.sqlalchemy import SQLAlchemy
import unittest
from time import sleep
from datetime import datetime
from datetime import timedelta
import os
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database, drop_database
from load_data import get_data, init_quartet, batch_load, store_in_db
from models import Clinics, Quartet

import pandas as pd

from app import db

        
class TestClinics(unittest.TestCase):

    def setUp(self):
        db.session.close()
        db.drop_all()
        db.create_all()

    def test_active(self):
        """Testing active clinics"""
        print("test_active()")
        db.session.close()
        db.drop_all()
        db.create_all()
        quartest_items = init_quartet()
        store_in_db(quartest_items, Quartet)
        clinics = batch_load()
        L1 = len(Quartet.query.all())
        L2 = len(Clinics.query.filter(Clinics.active==1).all())
        self.assertEqual(L1, L2)

    def test_data_load(self):
        """Testing initial load"""
        print("test_data_load()")
        
        items = get_data()
        store_in_db(items, Clinics)
        p = pd.DataFrame(items['data'])
        p =p.apply(lambda x: [str(i).lower() for i in x])
        L1 = len(p.groupby(['name_1', 'street_1', 'city', 'zip']).count())
        L2 = len(Clinics.query.all())
        self.assertEqual(L1, L2)

    

   

        


    

def tearDownModule():
    """Deletes the temporary log after all the tests"""
    db.session.close()
    db.drop_all()

if __name__ == '__main__':
    unittest.main()


import unittest



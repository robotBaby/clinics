from load_data import batch_load, init_quartet, store_in_db
from models import Clinics, Quartet
import schedule
import time
import logging
logging.basicConfig(filename='clinics.log',level=logging.DEBUG, \
	format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',\
	datefmt="%d/%b/%Y:%H:%M:%S",)



quartest_items = init_quartet()
store_in_db(quartest_items, Quartet)


schedule.every(5).seconds.do(batch_load)
#schedule.every().day.at("00:00").do(get_data)

while 1:
    schedule.run_pending()
    time.sleep(1)

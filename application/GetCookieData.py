import datetime
from  config import *

def get_data_by_time(time=datetime.date.today().strftime('%y%m%d')):
    print(time)
    file = open(xss_data_path+'/'+xss_data_name.format(time),"a")
    data = file.read()
    data
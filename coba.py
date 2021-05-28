from module.database import Database
from flask import jsonify
from pprint import pprint
import ast
import numpy as np

from datetime import datetime
db = Database()
# datajumlah = db.jumlah(None)
# print(datajumlah[0]['jumlah'])
# pprint(datachart)


# db = Database()
# dataserver = db.readsmtp(None)
# def filter_key(item):
#     return item['konfigurasi_key'] == 'server'
# server = next(filter(lambda x:x['konfigurasi_key']=='mail_port', dataserver))['value']
# string =''.join([str(item) for item in dataserver])
# print(type(dataserver))
# print(string)

# dataset = open('warkop.txt', 'r', errors = 'Ignore')
# data = dataset.readjawab(None)
# dataserver =''.join([str(item) for item in dataserver])
# print(dataserver)
# print(type(dataserver))

# server = next(filter(lambda x:x['konfigurasi_key']=='server', dataserver))['value']
# mail_port = next(filter(lambda x:x['konfigurasi_key']=='mail_port', dataserver))['value']
# # tls = next(filter(lambda x:x['konfigurasi_key']=='tls', dataserver))['value']
# # # tls = False
# ssl = next(filter(lambda x:x['konfigurasi_key']=='ssl', dataserver))['value']
# tls = next(filter(lambda x:x['konfigurasi_key']=='tls', dataserver))['value']
# email = next(filter(lambda x:x['konfigurasi_key']=='email', dataserver))['value']
# password = next(filter(lambda x:x['konfigurasi_key']=='password', dataserver))['value']

# print(server)
# print(type(ssl))
# print(type(tls))
# print('port flask mail =' + mail_port )

# for i in dataserver:
#     print(dataserver[i]['value'])

# dataset = open('warkop.txt', 'r', errors = 'Ignore')
# data = dataset.read()
# print(type(data))

# dataset = db.readjawab(None)
# # dataset =''.join([str(item) for item in dataset])

# for i in dataset:
#      i['jawaban']

# dataset = db.readjawab(None)
# data = ''
# for i in dataset:
#     data = data + i['jawaban'] + '\n'
# data = data.lower()
# print(data)

# data = dataset.lower()
# for i in dataset:
#     print(dataset[i])
# pprint(datapengunjung)
# print(len(data))
# print(dataset[0]['jawaban'])
# import datetime
 

 
# def myconverter(datachart):
#     if isinstance(datachart['tanggal'], datetime.datetime):
#         return o.__str__()
 
# print(json.dumps(datachart, default = myconverter))

# import json
 
 
# print(type(datachart))

# str_conv = json.dumps(datachart)  # string
# data = datachart[0]['tanggal']
# print(json.dumps(data, default = defaultconverter))
# print(str_conv)
# import json
# import datetime
# from json import JSONEncoder

# employee = {
#     "id": 456,
#     "name": "William Smith",
#     "salary": 8000,
#     "joindate": datetime.datetime.now()
# }

# import json
# import datetime
# from json import JSONEncoder

# employee = {
#     "id": 456,
#     "name": "William Smith",
#     "salary": 8000,
#     "joindate": datetime.datetime.now()
# }

# subclass JSONEncoder
# class DateTimeEncoder(JSONEncoder):
#         #Override the default method
#         def default(self, obj):
#             if isinstance(obj, (datetime.date, datetime.datetime)):
#                 return obj.isoformat()

# print("Printing to check how it will look like")
# print(DateTimeEncoder().encode(datachart))

# print("Encode DateTime Object into JSON using custom JSONEncoder")
# employeeJSONData = json.dumps(datachart, indent=4, cls=DateTimeEncoder)
# print(employeeJSONData)

from datetime import date
today = date.today()
print(today)
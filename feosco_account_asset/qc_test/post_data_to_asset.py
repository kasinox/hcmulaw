import xmlrpclib
import json

username = 'admin'
pwd = 'admin'
dbname = 'demo_brother'

vals = [{"photo_name":"brother","photo_data":"","feosco_barcode_type":"","feosco_code":"D123456","name":"gggg","category":"Thi\u1ebft b\u1ecb","owner":"_none","status":"_none","department":"P.DICH VU 4","purchase_value":"1"}]

data = json.dumps(vals)
sock_common = xmlrpclib.ServerProxy ('http://localhost:6069/xmlrpc/common')
uid = sock_common.login(dbname, username, pwd)
sock = xmlrpclib.ServerProxy('http://localhost:6069/xmlrpc/object')
vals = sock.execute(dbname, uid, pwd, 'interface.response', 'post_data_to_asset', data)

print '-' * 100
print vals
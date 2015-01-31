import xmlrpclib
import json
#
username = 'admin' #the user
#pwd = 'P@ssw0rd'      #the password of the user
pwd = 'admin'
# dbname = 'demo_brother'    #the database
dbname = 'sample_account_asset_v61'
# # # Get the uid
# sock_common = xmlrpclib.ServerProxy ('http://man.feosco.com:8069/xmlrpc/common')
# print sock_common
# uid = sock_common.login(dbname, username, pwd)

#replace localhost with the address of the server
#sock = xmlrpclib.ServerProxy('http://man.feosco.com:8069/xmlrpc/object')
sock = xmlrpclib.ServerProxy('http://127.0.0.1:8069/xmlrpc/object')
print sock
data = {'barcode': '0000000000017'}

#get_all_asset
# get_all_asset = sock.execute(dbname, 1, pwd, 'interface.response', 'get_all_asset')
# print 'get_all_asset'
# print get_all_asset
#
# #get_data_from_barcode
# get_data_from_barcode = sock.execute(dbname, 1, pwd, 'interface.response', 'get_data_from_barcode', data)
# print 'get_data_from_barcode'
# print get_data_from_barcode
#
#
#
#location
get_all_location = sock.execute(dbname, 1, pwd, 'interface.response', 'get_all_location')
print 'get_all_location'
print get_all_location
#
#
# #scan
# scan_val = {"asset_id": 2, "status":"Not good"}
# get_data_from_app = sock.execute(dbname, 1, pwd, 'interface.response', 'get_data_from_app', json.dumps(scan_val))
# print 'get_data_from_app'
# print get_data_from_app

# get_all_status
# get_all_status = sock.execute(dbname, 1, pwd, 'interface.response', 'get_all_status')
# print 'get_all_status'
# print get_all_status

# interface_response.py
# vals = json.dumps([{"asset_id":"8","status":"Good"},{"asset_id":"9","status":"Checked"}])
# get_data_from_app = sock.execute(dbname, 1, pwd, 'interface.response', 'get_data_from_app', vals)
# print 'get_data_from_app'
# print get_data_from_app







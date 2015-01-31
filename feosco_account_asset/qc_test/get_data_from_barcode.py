import xmlrpclib
import json

username = 'admin'
pwd = 'admin'
dbname = 'demo_brother'

vals = {
    'barcode': '310100011957'
}

sock_common = xmlrpclib.ServerProxy ('http://localhost:6069/xmlrpc/common')
uid = sock_common.login(dbname, username, pwd)
sock = xmlrpclib.ServerProxy('http://localhost:6069/xmlrpc/object')
vals = sock.execute(dbname, uid, pwd, 'interface.response', 'get_data_from_barcode', vals)

print '-' * 100
print vals
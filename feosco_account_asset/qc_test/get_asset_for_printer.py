import xmlrpclib

username = 'admin'
pwd = '1'
dbname = 'feos_full'

sock_common = xmlrpclib.ServerProxy ('http://localhost:8069/xmlrpc/common')
uid = sock_common.login(dbname, username, pwd)
sock = xmlrpclib.ServerProxy('http://localhost:8069/xmlrpc/object')
vals = sock.execute(dbname, uid, pwd, 'feosco.print.asset', 'get_asset_for_printer')

print '-' * 100
print vals
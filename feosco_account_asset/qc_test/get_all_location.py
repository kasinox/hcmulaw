import xmlrpclib

username = 'admin'
pwd = 'admin'
dbname = 'demo_brother'

sock_common = xmlrpclib.ServerProxy ('http://localhost:6069/xmlrpc/common')
uid = sock_common.login(dbname, username, pwd)
sock = xmlrpclib.ServerProxy('http://localhost:6069/xmlrpc/object')
vals = sock.execute(dbname, uid, pwd, 'interface.response', 'get_all_location')

print '-' * 100
print vals
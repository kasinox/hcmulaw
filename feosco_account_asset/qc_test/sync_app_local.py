import xmlrpclib

username = 'admin' #the user
pwd = 'admin'      #the password of the user
dbname = 'demo_brother'    #the database

# Get the uid
sock_common = xmlrpclib.ServerProxy ('http://localhost:8069/xmlrpc/common')
uid = sock_common.login(dbname, username, pwd)

#replace localhost with the address of the server
sock = xmlrpclib.ServerProxy('http://localhost:8069/xmlrpc/object')

vals = sock.execute(dbname, uid, pwd, 'interface.response', 'sync_local_app', '/Volumes/workspace/source/gitlab/6-1/feosco_account_asset/template/sync_loacal_text.txt')

print vals
# -*- coding:utf-8 -*-
from openerp.osv import osv, fields

class stationery_order_limit(osv.osv):

    _name = "stationery.order.limit"

    _columns = {
        'stationery_id': fields.many2one('stationery.stationery', 'Stationery', required=True),
        'total_limit': fields.float('Total limit', required=True),
        'department_id': fields.many2one('feosco.asset.department', 'Department', required=True),
        'role_id': fields.many2one('stationery.stationery.role', 'Repeat', required=True),
    }

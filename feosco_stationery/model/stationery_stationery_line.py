# -*- coding:utf-8 -*-
from openerp.osv import osv, fields

class stationery_stationery_line(osv.Model):

    _name = "stationery.stationery.line"

    _columns = {
		'name': fields.char('Name', size=128),
		'stationery_id': fields.many2one('stationery.stationery', 'Stationery', required=True),
		'department_id': fields.many2one('feosco.asset.department', 'Department'),
		'qty': fields.float('Quantity', required=True),
		'customer_id': fields.many2one('res.partner', 'Order from'),
		'uom_id': fields.many2one('product.uom', 'Uom'),
		'type': fields.selection([
			('in', 'In'),
			('out', 'Out')
			], 'Type', readonly=True),
    }
    _defaults = {
        'name': '/'
    }

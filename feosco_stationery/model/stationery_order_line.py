# -*- coding:utf-8 -*-
from openerp.osv import osv, fields

class stationery_order_line(osv.Model):

    _name = "stationery.order.line"

    _columns = {
        'stationery_id': fields.many2one('stationery.stationery', 'Stationery', required=True),
        'tax_ids': fields.many2many('account.tax', 'stationery_order_line_tax', 'stationery_line_id', 'tax_id', 'Taxes'),
        'price': fields.float('Price', required=True),
        'discount': fields.float('Discount (%)'),
        'total': fields.float('Total', readonly=True),
        'qty': fields.float('Quantity', required=True),
        'order_id': fields.many2one('stationery.order', 'Order', required=True),
        'department_id': fields.many2one('feosco.asset.department', 'Department'),
    }

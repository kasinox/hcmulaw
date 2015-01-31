# -*- coding:utf-8 -*-
from openerp.osv import osv, fields

class stationery_request_line(osv.Model):

    _name = "stationery.request.line"

    _columns = {
        'create_date': fields.datetime('Create date', readonly=True),
        'create_uid': fields.many2one('res.users', 'User', readonly=True),
        'stationery_id': fields.many2one('stationery.stationery', 'Stationery', required=True),
        'request_id': fields.many2one('stationery.request', 'Request', required=True),
        'qty': fields.float('Qty'),
        'reason': fields.text('Reason'),
        'state': fields.selection([
            ('draft', 'Draft'),
            ('waiting', 'Wait'),
            ('done', 'Done'),
            ('pending', 'Pending'),
            ('cancel', 'Cancel'),
        ], 'State')
    }

    _defaults = {
        'state': 'draft',
    }
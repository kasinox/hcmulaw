# -*- coding:utf-8 -*-
from openerp.osv import osv, fields

class stationery_stationery(osv.Model):

    def _get_all_quantity(self, cr, uid, ids, fname, arg, context={}):
        res = {}
        for this in self.browse(cr, uid, ids):
            res[this.id] = {
                'qty': 0.00,
                'qty_use': 0.00,
                'qty_onhand': 0.00,
            }
            if this.line_ids:
                for line in this.line_ids:
                    res[this.id]['qty'] += line.qty
            if this.line_use_ids:
                for line in this.line_use_ids:
                    res[this.id]['qty_use'] += line.qty
            res[this.id]['qty_onhand'] = res[this.id]['qty'] - res[this.id]['qty_use']
        return res

    _name = "stationery.stationery"

    _columns = {
        'name': fields.char('Name', size=128, required=True),
        'code': fields.char('Code', size=128, required=True),
        'qty': fields.function(_get_all_quantity, type='float', string='Quantity Purchase', multi='get_qty'),
        'qty_use': fields.function(_get_all_quantity, type='float', string='Quantity Use', multi='get_qty'),
        'qty_onhand': fields.function(_get_all_quantity, type='float', string='Quantity On Hand', multi='get_qty'),
        'line_ids': fields.one2many('stationery.stationery.line', 'stationery_id', 'Purchase', readonly=True),
        'limit_ids': fields.one2many('stationery.order.limit', 'stationery_id', 'Limit'),
        'line_use_ids': fields.one2many('stationery.request.line', 'stationery_id', 'Used', readonly=True),
    }

stationery_stationery()
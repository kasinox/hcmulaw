# -*- coding:utf-8 -*-
from openerp.osv import osv, fields
from openerp.tools.translate import _

class stationery_request(osv.Model):

    _name = "stationery.request"

    _columns = {
        'name': fields.char('Name', required=True, readonly=True, states={'draft': [('readonly', False)]}),
        'date_confirm': fields.datetime('Date', readonly=True, states={'draft': [('readonly', False)]}),
        'reason': fields.text('Reason', readonly=True, states={'draft': [('readonly', False)]}),
        'type': fields.selection([('private', 'Private'), ('public', 'Public')], 'Type', readonly=True, states={'draft': [('readonly', False)]}),
        'line_ids': fields.one2many('stationery.request.line', 'request_id', 'Lines', readonly=True, states={'draft': [('readonly', False)]}),
        'department_id': fields.many2one('feosco.asset.department', 'Department', required=True, readonly=True, states={'draft': [('readonly', False)]}),
        'supplier_id': fields.many2one('res.partner', 'Supplier', domain=[('supplier', '=', True)]),
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
        'type': 'private',
    }

    def act_wait(self, cr, uid, ids, context={}):
        return self.write(cr, uid, ids, {'state': 'waiting'})

    def act_done(self, cr, uid, ids, context={}):
		order_pool = self.pool.get('stationery.order')
		self.write(cr, uid, ids, {'state': 'done'})
		for this in self.browse(cr, uid, ids):
			order_val = {
				'name': this.name,
				'user_id': uid,
				'request_id': this.id,
				'partner_id': this.supplier_id.id,
			    'type': 'in',
			}
			res_id = order_pool.create(cr, uid, order_val)
			return {
				'view_type': 'form',
				'view_mode': 'form',
				'res_model': 'stationery.order',
				'type': 'ir.actions.act_window',
			    'res_id': res_id,
				'target': 'self',
				'context': context,
				'nodestroy': True,
				}


    def act_pending(self, cr, uid, ids, context={}):

        return self.write(cr, uid, ids, {'state': 'pending'})

    def act_cancel(self, cr, uid, ids, context={}):

        return self.write(cr, uid, ids, {'state': 'cancel'})

    def act_reset(self, cr, uid, ids, context={}):

        return self.write(cr, uid, ids, {'state': 'draft'})
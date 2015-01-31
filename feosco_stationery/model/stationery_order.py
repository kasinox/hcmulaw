# -*- coding:utf-8 -*-
from openerp.osv import osv, fields
from openerp.tools.translate import _

class stationery_order(osv.Model):

    _name = "stationery.order"
    _inherit = ['mail.thread', 'ir.needaction_mixin']

    _columns = {
        'name': fields.char('Name', size=128, required=True, readonly=True, states={'draft': [('readonly', False)]}),
        'partner_id': fields.many2one('res.partner', 'Order from', domain=[('customer', '=', True)], readonly=True, states={'draft': [('readonly', False)]}),
        'shipment_id': fields.many2one('res.partner', 'Shipment to', readonly=True, states={'draft': [('readonly', False)]}),
        'request_id': fields.many2one('stationery.request', 'Request'),
        'date_order': fields.datetime('Purchase Order', readonly=True, states={'draft': [('readonly', False)]}),
        'line_ids': fields.one2many('stationery.order.line', 'order_id', 'Lines', required=True, readonly=True, states={'draft': [('readonly', False)]}),
        'amount_untaxed': fields.float('Sub', readonly=True, states={'draft': [('readonly', False)]}),
        'amount_tax': fields.float('Tax', readonly=True, states={'draft': [('readonly', False)]}),
        'amount_total': fields.float('Total', readonly=True, states={'draft': [('readonly', False)]}),
        'user_id': fields.many2one('res.users', 'User', readonly=True, states={'draft': [('readonly', False)]}),
        'type': fields.selection([
            ('in', 'In'),
            ('out', 'Out')
            ], 'Type', readonly=True, states={'draft': [('readonly', False)]}),

        'state': fields.selection([
            ('draft', 'Draft'),
            ('waiting', 'Waiting'),
            ('order', 'Order Customer'),
            ('incoming', 'Incoming Order'),
            ('done', 'Done'),
            ('cancel', 'Cancel'),
            ('pending', 'Pending'),
            ], 'State')
    }

    _defaults = {
        'state': 'draft',
        'type': 'in',
    }

    
    def act_wait(self, cr, uid, ids, context={}):
        amount_tax = 0
        amount_untaxed = 0
        amount_total = 0
        for this in self.browse(cr, uid, ids):
            if this.line_ids:
                for line in this.line_ids:
                    sum_tax = 0
                    for tax in line.tax_ids:
                        sum_tax += tax.amount
                    if not line.discount:
                        line['discount'] = 0
                    self.write(cr, uid, line.id, {
                        'total': line.qty * line.price - (line.qty * line.price * line.discount / 100) - (line.qty * line.price * sum_tax)
                    })
                    amount_tax += line.qty * line.price * sum_tax
                    amount_untaxed += line.qty * line.price
                    amount_total += line.qty * line.price - (line.qty * line.price * line.discount / 100) - (line.qty * line.price * sum_tax)
            else:
                raise osv.except_osv(_('Error'), _('Can not submit with empty lines'))

        return self.write(cr, uid, ids, {
            'state': 'waiting',
            'amount_tax': amount_tax,
            'amount_untaxed': amount_untaxed,
            'amount_total': amount_total
            })

    def act_order(self, cr, uid, ids, context={}):
        return self.write(cr, uid, ids, {'state': 'order'})

    def act_incoming(self, cr, uid, ids, context={}):
        return self.write(cr, uid, ids, {'state': 'incoming'})

    def act_done(self, cr, uid, ids, context={}):
        stationery_line_pool = self.pool.get('stationery.stationery.line')
        for this in self.browse(cr, uid, ids):
			for line in this.line_ids:
				stationery_line_pool.create(cr, uid, {
					'stationery_id': line.stationery_id.id,
					'qty': line.qty,
					'type': this.type
					})
        return self.write(cr, uid, ids, {'state': 'done'})

    def act_cancel(self, cr, uid, ids, context={}):
        return self.write(cr, uid, ids, {'state': 'cancel'})

    def act_pending(self, cr, uid, ids, context={}):
        return self.write(cr, uid, ids, {'state': 'pending'})

    def act_reset(self, cr, uid, ids, context={}):
        return self.write(cr, uid, ids, {'state': 'draft'})

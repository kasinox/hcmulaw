#-*- coding:utf-8 -*-
from openerp.osv import osv, fields

class feosco_print_selection(osv.osv_memory):
    _name = "feosco.print.selection"

    _columns = {
        'asset_ids': fields.many2many('account.asset.asset', 'fesco_print_rel', 'mem_id', 'asset_id', 'Assets', required=True),
        'state': fields.selection([('draft', 'Not print'), ('done', 'Printed')], 'State'),
        'print_type': fields.selection([('chopped', 'Cut'), ('ligature', 'Not cut')],  'Type', required=True),
        'qty': fields.integer('Quantity'),
    }
    _defaults = {
                 'state': 'draft',
                 'print_type':'ligature',
                 'qty': 1
    }

    def act_print(self, cr, uid, ids, context={}):
        for this in self.browse(cr, uid, ids):
            print_ids = []
            asset_ids = this.asset_ids
            if asset_ids:
                for ass in asset_ids:
                    print_ids.append(ass.id)
                if print_ids:
                    i = 0
                    for i in range(0, this.qty):
                        self.pool.get('feosco.print.asset').record_asset_to_print(cr, uid, print_ids, this.print_type, context=context)
                    return self.write(cr, uid, [this.id], {'state': 'done'})
            else:
                return self.write(cr, uid, [this.id], {'state': 'done'})

feosco_print_selection()
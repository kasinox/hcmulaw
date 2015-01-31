#-*- coding:utf-8 -*-
from openerp.osv import osv, fields

class feosco_account_asset_print_all(osv.osv_memory):
    _name = "feosco.asset.print.all"
    
    _columns = {
                'print_type': fields.selection([('chopped', 'Cut'), ('ligature', 'Not cut')], 'Type', required=True),
                'qty': fields.integer('Quantity'),
    }
    _defaults = {
        'print_type': 'ligature',
        'qty': 1
    }
    
    def action_print_all(self, cr, uid, ids, context={}):
        this = self.browse(cr, uid, ids)
        if context:
            asset_ids = context.get('active_ids') if (context.has_key('active_ids') and context.get('active_ids')) else None
            if asset_ids:
                for i in range(0, this[0].qty):
                    self.pool.get('feosco.print.asset').record_asset_to_print(cr, uid, asset_ids, this[0].print_type, context=context)
        return {'type': 'ir.actions.act_window_close'}
                
feosco_account_asset_print_all()
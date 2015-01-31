#-*- coding:utf-8 -*-

from openerp.osv import  osv, fields
from openerp.tools.translate import _

class account_asset_category(osv.osv):

    _inherit = "account.asset.category"

    def name_get(self, cr, uid, ids, context=None):
        if isinstance(ids, (list, tuple)) and not len(ids):
            return []
        if isinstance(ids, (long, int)):
            ids = [ids]

        reads = self.read(cr, uid, ids, ['name', 'feosco_parent_id'], context=context)

        res = []
        for record in reads:
            name = record['name']
            if record['feosco_parent_id']:
                name = record['feosco_parent_id'][1]+' / '+name
            res.append((record['id'], name))


        return res

    def name_search(self, cr, uid, name, args=None, operator='ilike', context=None, limit=100):
        if not args:
            args = []
        if not context:
            context = {}
        if name:
            # Be sure name_search is symetric to name_get
            name = name.split(' / ')[-1]
            ids = self.search(cr, uid, [('name', operator, name)] + args, limit=limit, context=context)
        else:
            ids = self.search(cr, uid, args, limit=limit, context=context)
        return self.name_get(cr, uid, ids, context)

    _columns = {
        'method_time': fields.selection([
            ('number', 'Number of Depreciations'),
            ('end', 'Ending Date'),
            ('percent', 'Percent (%) / Year'),
        ], 'Time Method', required=True),
        'feosco_percent': fields.float('Percent (%) of year'),
        'feosco_parent_id': fields.many2one('account.asset.category', 'Parent'),
        'feosco_child_ids': fields.one2many('account.asset.category', 'feosco_parent_id', 'Childs'),
    }
    _defaults = {
        'method_time': 'percent',
    }

    _order = "name"

    def create(self, cr, uid, vals, context=None):
        return super(account_asset_category, self).create(cr, uid, vals, context=context)


account_asset_category()
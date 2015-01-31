#-*- coding:utf-8 -*-
from openerp.osv import osv, fields

class feosco_asset_department(osv.osv):

    _name = "feosco.asset.department"

    def _get_sum(self, cr, uid, ids, f_name, arg, context={}):
        res = {}
        if ids:
            for this in self.browse(cr, uid, ids):
                res[this.id] = 0
                if this.asset_ids:
                    for asset in this.asset_ids:
                        res[this.id] += 1
        return res


    def name_get(self, cr, uid, ids, context=None):
        if not ids:
            return []
        if isinstance(ids, (int, long)):
                    ids = [ids]
        reads = self.read(cr, uid, ids, ['name', 'code'], context=context)
        res = []
        for record in reads:
            name = record['name']
            if record['code']:
                name = record['code'] + ' ' + name
            res.append((record['id'], name))
        return res


    _columns = {
        'name': fields.char('Department Name', size=128, required=True),
        'parent_id': fields.many2one('feosco.asset.department', 'Department Parent'),
        'code': fields.char('Reference Code', size=128),
        'company_id': fields.many2one('res.company', 'Company', required=True),
        'note': fields.text('Notes'),
        'limit': fields.integer('Limit'),
        'phone': fields.char('Phone', required=True),
        'asset_ids': fields.one2many('account.asset.asset', 'feosco_asset_department_id', 'Asset'),
        'sum': fields.function(_get_sum, type='integer', string='Sum total'),
    }

    _defaults = {
        'company_id': lambda self, cr, uid, context: self.pool.get('res.company')._company_default_get(cr, uid, 'account.asset.category', context=context),
    }

feosco_asset_department()
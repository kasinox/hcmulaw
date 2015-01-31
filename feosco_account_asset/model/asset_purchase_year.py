#-*- coding:utf-8 -*-
from openerp.osv import osv, fields

class feosco_purchase_year(osv.Model):

    _name = "feosco.purchase.year"

    _columns = {
        'name': fields.char('No.', size=128, required=True),
        'code': fields.char('Code', size=128, required=True),
        'default': fields.boolean('Default', help='Defaul for Asset'),
    }

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
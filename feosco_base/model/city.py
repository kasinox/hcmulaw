# -*- coding: utf-8 -*-

from openerp.osv import fields, osv

class feosco_city(osv.osv):

    _name = "feosco.city"

    _description = "this is module master city"
    
    def _get_country_id(self, cr, uid, ids, context=None):
        country_ids = self.pool.get('res.country').search(cr, uid, [('code', '=', 'VN')], context=context)
        return country_ids[0] if country_ids else False
    
    _columns = {
        'name': fields.char('Name', size=256,),
        'code': fields.char('Code', size=64,),
        'country_id': fields.many2one('res.country', string='Country', domain="[('code', '=', 'VN')]"),
    }
    
    _defaults = { 
        'country_id': _get_country_id,
    }
    
    sql_constraints = [
                    ('name', 'unique(name)', 'The key must be unique'),
                    ('code', 'unique(code)', 'The code must be unique')
    ]

feosco_city()


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

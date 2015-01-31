# -*- coding: utf-8 -*-

from openerp.osv import fields, osv

class res_partner_bank(osv.osv):
    
    _inherit="res.partner.bank"
    
    _columns = {
                'city_id': fields.many2one('feosco.city', 'City', domain="[('country_id.code', '=', 'VN')]"),
                'feosco_district_id': fields.many2one('feosco.district', 'District', domain="[('city_id.id', '=', city_id)]"),
                }
    
    def onchange_partner_id(self, cr, uid, id, partner_id, context=None):
        result = {}
        if partner_id:
            part = self.pool.get('res.partner').browse(cr, uid, partner_id, context=context)
            result['owner_name'] = part.name
            result['street'] = part.street or False
            result['feosco_district_id'] = part.feosco_district_id.id or False
            result['city_id'] = part.city_id.id or False
            result['zip'] = part.zip or False
            result['country_id'] = part.country_id.id
            result['state_id'] = part.state_id.id
        return {'value': result}

res_partner_bank()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

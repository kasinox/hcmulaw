# -*- coding: utf-8 -*-

from openerp.osv import fields, osv

class res_company(osv.Model):


    _inherit="res.company"
    
    def _get_address_data(self, cr, uid, ids, field_names, arg, context=None):
        
        return super(res_company, self)._get_address_data(cr, uid, ids, field_names, arg, context=context)
    
    def _set_address_data(self, cr, uid, company_id, name, value, arg, context=None):
        
        return super(res_company, self)._set_address_data(cr, uid, company_id, name, value, arg, context=context)
    
    #return default country is Viet Nam
    def _get_country_id(self, cr, uid, ids, context=None):
        country_ids = self.pool.get('res.country').search(cr, uid, [('code','=','VN')])
        return country_ids[0] if country_ids else False
    

    
    _columns = {
        'feosco_district_id': fields.function(_get_address_data, fnct_inv=_set_address_data, type='many2one', relation='feosco.district', string="District", multi='address'),
        'feosco_city_id': fields.function(_get_address_data, fnct_inv=_set_address_data, type='many2one', relation='feosco.city', string="City", multi='address'),
    }

    _defaults = {
        'country_id': _get_country_id,
    }

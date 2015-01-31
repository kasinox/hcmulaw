# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from datetime import datetime

from openerp.osv import fields, osv


class res_partner(osv.osv):
    _name = "res.partner"
    _inherit="res.partner"
    
    def _get_country_id(self, cr, uid, ids, context=None):
        search_country = [('code', '=', 'VN')]
        country_ids = self.pool.get('res.country').search(cr, uid, search_country)
        return country_ids[0] if country_ids else False

    def event_country_change(self, cr, uid, ids, country_id, context={}):
        if country_id:
            return {'value': {'city': None, 'district_id': None}}

    def event_city_change(self, cr, uid, ids, city, context={}):
        if city:
            return {'value': {'feosco_district_id': None}}
        else:
            return {}

    _columns = {
        'feosco_city_id': fields.many2one('feosco.city', u'Thành phố'),
        'feosco_district_id':  fields.many2one('feosco.district', u'Quận (huyện)', domain="[('city_id', '=', feosco_city_id)]"),
        'feosco_birthday': fields.date(u'Sinh nhật'),
        'feosco_business_license': fields.char(u'Giấy phép kinh doanh', size=128),
        'feosco_account_num': fields.char(u'Mã số thuế', size=128),
        'feosco_business_type': fields.char(u'Loại hình kinh doanh'),
        'country_id': fields.many2one('res.country', u'Quốc gia', domain="[('code', '=', 'VN')]"),
    }

    _defaults = {
        'country_id': _get_country_id,
    }
    
        
    
res_partner()
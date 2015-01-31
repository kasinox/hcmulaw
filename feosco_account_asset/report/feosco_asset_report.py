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

from openerp import tools
from openerp.osv import fields,osv

class feosco_asset_report(osv.osv):
    _name = "feosco.asset.report"
    _description = "Print report Asset"
    _auto = False
    _columns = {
        'name': fields.char('Name', readonly=True),
        'department': fields.char('Department', readonly=True),
        'num': fields.char('num', readonly=True),
        'qr': fields.char('qr', readonly=True),
        'year': fields.char('year', readonly=True),
        'user': fields.char('user', readonly=True),
        'qty': fields.float('Quantity', readonly=True),
    }
    def init(self, cr):
        tools.drop_view_if_exists(cr, 'feosco_asset_report')
        cr.execute("""
            create or replace view feosco_asset_report as (
                 select
					min(aaa.id) as id,
					aaa.feosco_qty as qty,
					aaa.name as name,
					fad.name as department,
					aaa.feosco_num as num,
					aaa.code as qr,
					fpy.name as year,
					rp.name as user
					from
					account_asset_asset aaa,
					product_uom pu,
					feosco_purchase_year fpy,
					res_users ru,
					res_partner rp,
					feosco_asset_department fad
					where
					aaa.feosco_uom_id=pu.id and
					aaa.feosco_purchase_year_id=fpy.id and
					aaa.feosco_user_id=ru.id and
					rp.id=ru.partner_id and
					fad.id=aaa.feosco_asset_department_id
					group by
					aaa.name,
					fad.name,
					aaa.feosco_num,
					aaa.code,
					fpy.name,
					rp.name,
					aaa.feosco_qty
					order by department

            )
        """)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

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


from openerp.osv import fields, osv
from openerp.tools.translate import _

class feosco_barcode_type(osv.osv):
    _name = "feosco.barcode.type"
    _description = "Barcode Type"

    _columns = {
        'name': fields.char('Name', size=256, ),
        'code': fields.char('Code', size=256, ),
        'active': fields.boolean('Active'),
    }

    sql_constraints = [
        ('name', 'unique(name)', 'The key must be unique'),
        ('code', 'unique(code)', 'The code must be unique')
    ]

    _defaults = {
        'active': True
    }

    def unlink(self, cr, uid, ids, context=None):
        raise osv.except_osv(_('Error !'), _('Barcode Type can not be deleted. Please deactivate it. '))


feosco_barcode_type()


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

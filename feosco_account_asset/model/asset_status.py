# -*- encoding: utf-8 -*-
from openerp.osv import osv, fields

class feosco_asset_status(osv.osv):

    _name = 'feosco.asset.status'
    _description = 'Asset Status Management'

    _columns = {
        'name': fields.char('Status', size=64, required=True)
    }

    _sql_constraints = [
        ('name_uniq', 'unique (name)', 'The Status must be unique !')
    ]

feosco_asset_status()

# -*- coding:utf-8 -*-
from openerp.osv import osv, fields

class stationery_stationery_role(osv.Model):

    _name = "stationery.stationery.role"

    _columns = {
        'name': fields.char('Name', required=True),
        'dt_from': fields.datetime('From', requried=True),
        'dt_to': fields.datetime('To', requried=True),
        'active': fields.boolean('Active'),
    }

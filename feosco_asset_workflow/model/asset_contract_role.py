# -*- coding: utf-8 -*-
from openerp.osv import osv, fields

class asset_contract_role(osv.Model):
	_name = "asset.contract.role"

	_columns = {
		'name': fields.char('Tên', required=True),
		'note': fields.text('Ghi chú rỏ', required=True),
	    'active': fields.boolean(u'Kích hoạt'),
	}
	_defaults = {
		'active': True
	}
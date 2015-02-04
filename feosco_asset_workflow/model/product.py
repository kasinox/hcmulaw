#-*- coding:utf-8 -*-
from openerp.osv import osv, fields

class productTemplate(osv.Model):
	_inherit = "product.template"
	_columns = {
		'asset_id': fields.many2one('account.asset.asset', u'Tài sản'),
		'asset': fields.boolean(u'Là tài sản ?')
	}
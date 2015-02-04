#-*- coding:utf-8 -*-

from openerp.osv import osv, fields

class accountInvoice(osv.Model):

	_inherit = "account.invoice"
	_columns = {
		'contract_id': fields.many2one('asset.contract', u'Hợp đồng'),
	}

	def change_contract_id(self, cr, uid, ids, contract_id, context={}):
		vals = {}
		return vals
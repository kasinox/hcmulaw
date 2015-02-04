# -*- coding: utf-8 -*-
from openerp.osv import osv, fields
import datetime
from openerp.tools.translate import _

class asset_stock (osv.Model):
	_name = "asset.stock"
	_inherit = "mail.thread"
	_columns = {
		'name': fields.char(u'Tên', readonly=True, states={'draft': [('readonly', False)]}),
		'date': fields.datetime(u'Ngày nghiệm thu', required=True, readonly=True, states={'draft': [('readonly', False)]}),
		'location_ids': fields.many2many('feosco.asset.department', 'asset_stock_department_rel', 'stock_id', 'department_id', u'Phòng', readonly=True, states={'draft': [('readonly', False)]}),
		'line_ids': fields.one2many('asset.contract.line', 'stock_id', string=u'Tài sản', readonly=True, states={'draft': [('readonly', False)]}),
		'contract_id': fields.many2one('asset.contract', u'Từ hợp đồng', readonly=True, states={'draft': [('readonly', False)]}),
		'state': fields.selection([
			('draft', u'Phác thảo'),
			('done', u'Hoàn tất'),
			], string=u'Trạng thái'),
		'asset_ids': fields.one2many('account.asset.asset', 'stock_id', u'Tài sản', readonly=True),
	}

	_defaults = {
		'state': 'draft'
	}

	_sql_constraints = [
		('contract_id_uniq', 'unique (contract_id)', u'1 nghiệm thu chỉ tương ứng với 1 hợp đồng duy nhất, đã có bản nghiệm thu của hợp đồng này tồn tại'),
	]

	def event_change_contract(self, cr, uid, ids, contract_id, context={}):
		contract_pool = self.pool.get('asset.contract')
		if contract_id:
			contract = contract_pool.browse(cr, uid, contract_id, context=context)
			return {'value': {'name': 'NT/%s' % contract.name}}
		else:
			return {'value': {}}


	def _compare_date(self, date_from, date_to):
		DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
		from_dt = datetime.datetime.strptime(date_from, DATETIME_FORMAT)
		to_dt = datetime.datetime.strptime(date_to, DATETIME_FORMAT)
		if to_dt < from_dt:
			raise osv.except_osv(_(u'Lổi'), _(u'Ngày nghiệm thu phải sau ngày ký hợp đồng: %s' % from_dt))
		else:
			return True

	def create(self, cr, uid, vals, context={}):
		res_id = super(asset_stock, self).create(cr, uid, vals, context=context)
		line_pool = self.pool.get('asset.contract.line')
		contract_pool = self.pool.get('asset.contract')
		if vals['contract_id']:
			contract = contract_pool.browse(cr, uid, vals.get('contract_id'))
			self._compare_date(contract.contract_date, vals['date'])
			if contract:
				for line in contract.line_ids:
					line_pool.write(cr, uid, [line.id], {'stock_id': res_id})

		return res_id

	def act_done(self, cr, uid, ids, context={}):
		asset_pool = self.pool.get('account.asset.asset')
		categ_pool = self.pool.get('account.asset.category')
		categ_ids = categ_pool.search(cr, uid, [('name', '=', 'Máy móc, thiết bị')])
		for this in self.browse(cr, uid, ids):
			if this.line_ids:
				for line in this.line_ids:
					val = {
						'name': line.name,
						'purchase_value': line.price,
						'feosco_asset_department_id': line.department_id.id if line.department_id else None,
						'feosco_user_id': line.user_id.id if line.user_id else None,
						'feosco_qty': line.qty if line.qty else 1,
						'category_id': line.category_id.id if line.category_id else categ_ids[0] if categ_ids else None,
						'stock_id': this.id
					}

					asset_id = asset_pool.create(cr, uid, val, context=context)
					if val['feosco_user_id']:
						asset_pool.write(cr, uid, [asset_id], {'state': 'open'})
		return self.write(cr, uid, ids, {'state': 'done'})

	def act_reset(self, cr, uid, ids, context={}):
		return self.write(cr, uid, ids, {'state': 'draft'})

	def write(self, cr, uid, ids, vals, context={}):
		if vals.has_key('date') and vals['date']:
			for this in self.browse(cr, uid, ids):
				self._compare_date(this.contract_id.contract_date, vals['date'])
		return super(asset_stock ,self).write(cr, uid, ids, vals, context=context)


class account_asset_asset(osv.Model):
	_inherit = "account.asset.asset"
	_columns = {
		'stock_id': fields.many2one('asset.stock', u'Nghiệm thu'),
	}

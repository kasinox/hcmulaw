# -*- coding: utf-8 -*-
from openerp.osv import osv, fields
from openerp.tools.translate import _

class asset_contract(osv.Model):
	_name = "asset.contract"
	_inherit = "mail.thread"

	def _get_total(self, cr, uid, ids, fname, arg, context={}):
		res = {}
		if not ids:
			return res
		else:
			for this in self.browse(cr, uid, ids):
				res[this.id] = {
					'amount_tax': 0.00,
					'amount_discount': 0.00,
					'amount_total': 0.00,
					'amount_sub': 0.00,
					'payment_before_total': 0.00,
					'amount_sum': 0.00
				}
				if this.line_ids:
					amount_tax = 0
					amount_discount = 0
					amount_sub = 0
					payment_before_total = 0
					amount_sum = 0
					for line in this.line_ids:
						amount_sub += line.qty * line.price
						if line.tax_ids:
							for tax in line.tax_ids:
								amount_tax += line.price * line.qty * tax.amount
						if line.discount:
							amount_discount += line.discount/100 * line.qty * line.price
					amount_total = amount_sub + amount_tax - amount_discount
					if this.type == 'before':
						payment_before_total = amount_total * this.payment_before / 100
						amount_sum = amount_total - payment_before_total
					else:
						amount_sum = amount_total
					res[this.id] = {
						'amount_tax': amount_tax,
						'amount_discount': amount_discount,
						'amount_total': amount_total,
						'amount_sub': amount_sub,
					    'amount_sum': amount_sum,
					    'payment_before_total': payment_before_total,
					}
			return res

	_columns = {
		'name': fields.char(u'Số Hợp đồng', required=True, readonly=True, states={'new': [('readonly', False)]}),
		'contract_date': fields.datetime(u'Ngày ký', track_visibility='onchange', readonly=True, states={'new': [('readonly', False)]}, required=True),
		'representative_id': fields.many2one('res.company', u'Trường', readonly=True, states={'new': [('readonly', False)]}),
		'customer_id': fields.many2one('res.partner', u'Nhà cung cấp', domain=[('supplier', '=', True)], track_visibility='onchange', readonly=True, states={'new': [('readonly', False)]}, required=True),
		'sum_char': fields.text(u'Tổng tiền (bằng chử)', track_visibility='onchange', readonly=True, states={'new': [('readonly', False)]}),
		'user_approved_id': fields.many2one('res.users', u'Người lập', track_visibility='onchange', readonly=True, states={'new': [('readonly', False)]}),
		'discount_total': fields.float(u'Giảm giá %', readonly=True, states={'new': [('readonly', False)]}),
		'amount_tax': fields.function(_get_total, type='float', string=u'VAT', multi='get_total', readonly=True, states={'new': [('readonly', False)]}),
		'amount_discount': fields.function(_get_total, type='float', string=u'Giảm giá', multi='get_total', readonly=True, states={'new': [('readonly', False)]}),
		'amount_total': fields.function(_get_total, type='float', string=u'Phải chi', multi='get_total', readonly=True, states={'new': [('readonly', False)]}),
		'amount_sub': fields.function(_get_total, type='float', string=u'Trước thuế', multi='get_total', readonly=True, states={'new': [('readonly', False)]}),
		'role_ids': fields.many2many('asset.contract.role', 'asset_contract_role_rel', 'contract_id', 'role_id', u'Điều khoản', readonly=True, states={'new': [('readonly', False)]}),
		'line_ids': fields.one2many('asset.contract.line', 'contract_id', u'Sản phẩm mua', required=True, readonly=True, states={'new': [('readonly', False)]}),
		'state': fields.selection([('new', u'Phác thảo'), ('active', u'Đã ký'), ('cancel', u'Đã huỷ')], u'Trạng thái'),
		'type': fields.selection([('before', u'Có ứng trước'), ('after', u'Thanh toán 1 lần sau khi nghiệm thu tài sản')], u'Kiểu thanh toán'),
		'payment_before': fields.float(u'Số tiền tạm ứng (%) / Tổng HĐ'),
		'payment_before_total': fields.function(_get_total, type='float', string=u'Đã tạm ứng', multi='get_total', readonly=True, states={'new': [('readonly', False)]}),
		'amount_sum': fields.function(_get_total, type='float', string=u'Số còn lại', multi='get_total', readonly=True, states={'new': [('readonly', False)]}),
	}

	_sql_constraints = [
		('contract_uni_name', 'unique (name)', u'Đã tồn tại Số Hợp Đồng này. Vui lòng kiểm tra lại số Hợp Đồng'),
	]
	_defaults = {'state': 'new', 'type': 'after'}

	def act_active(self, cr, uid, ids, context={}):
		for this in self.browse(cr, uid, ids):
			if not this.line_ids:
				raise osv.except_osv(_(u'Lổi'),_(u'Vui lòng thực hiện nhập liệu các sản phẩm mua của hợp đồng này.'))
			else:
				for line in this.line_ids:
					if line.qty == 0:
						raise osv.except_osv(_(u'Lổi'),_(u'Số lượng mua không thể là 0, Vui lòng thay đổi số lượng mua cho : %s, và lưu dữ liệu lại rồi Xác nhận ký' % line.name))
					if line.price <= 0:
						raise osv.except_osv(_(u'Lổi'),_(u'Giá thành không thể nhỏ hơn 0, Vui lòng thay đổi giá mua cho : %s, và lưu dữ liệu lại rồi Xác nhận ký' % line.name))
		return self.write(cr, uid, ids, {'state': 'active'}, context=context)

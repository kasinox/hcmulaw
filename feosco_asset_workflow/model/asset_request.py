# -*- coding: utf-8 -*-
from openerp.osv import osv, fields
from openerp.tools.translate import _

class asset_request(osv.Model):
	_name = "asset.request"
	_inherit = "mail.thread"
	_columns = {
		'create_date': fields.datetime(u'Ngày tạo', readonly=True),
	    'user_id': fields.many2one('res.users', u'Người đề nghị'),
	    'purchase_user_id': fields.many2one('res.users', u'Người đi mua', readonly=True, states={'approved1': [('readonly', False)]}),
		'name': fields.char(u'Tên', required=True, readonly=True, states={'draft': [('readonly', False)]}),
		'department_id': fields.many2one('feosco.asset.department', u'Phòng ban cần', readonly=True, states={'draft': [('readonly', False)]}),
		'note': fields.text(u'Ghi chú', readonly=True, states={'draft': [('readonly', False)]}),
		'line_ids': fields.one2many('asset.request.line', 'request_id', u'Các tài sản Y/C', readonly=True, states={'draft': [('readonly', False)]}),
		'request_date': fields.date(u'Ngày Yêu cầu', readonly=True, states={'draft': [('readonly', False)]}),
	    'reject_reson': fields.text(u'Lý do từ chối', readonly=True, states={'approved1': [('readonly', False)],'approved2': [('readonly', False)],'approved3': [('readonly', False)]}),
		'state': fields.selection([
									('draft', u'Bản thảo'),
									('approved1', u'QT TB duyệt'),
									('approved2', u'BGH đã duyệt'),
									('approved3', u'QT TB Đang mua'),
									('done', u'Hoàn tất cấp TB'),
									('cancel', u'Từ chối')
								], u'Trạng thái', track_visibility='onchange')
	}

	_defaults = {
		'state': 'draft',
		'user_id': lambda obj, cr, uid, context: uid,
		'name': lambda self,cr,uid,ctx=None: self.pool.get('ir.sequence').get(cr, uid, 'asset.request.type', context=ctx) or '/',
	}
	_order = "create_date DESC, state DESC"

	def act_confirm(self, cr, uid, ids, context={}):
		line_pool = self.pool.get('asset.request.line')
		for this in self.browse(cr, uid, ids):
			if not this.line_ids:
				raise osv.except_osv(_(u'Lổi'), _(u'Vui lòng nhập liệu các yêu cầu tài sản trước khi đề xuất lên.'))
			else:
				line_ids = []
				for line in this.line_ids:
					line_ids.append(line.id)
				line_pool.act_confirm(cr, uid, line_ids, context=context)
		return self.write(cr, uid, ids, {'state': 'approved1'}, context=context)

	def act_approved1(self, cr, uid, ids, context={}):
		line_pool = self.pool.get('asset.request.line')
		for this in self.browse(cr, uid, ids):
			if not this.purchase_user_id:
				raise osv.except_osv(_(u'Cảnh báo'), _(u'Vui lòng chọn nhân viên đi mua thiết bị'))
			if not this.line_ids:
				raise osv.except_osv(_(u'Lổi'), _(u'Vui lòng nhập liệu các yêu cầu tài sản trước khi đề xuất lên.'))
			else:
				line_ids = []
				for line in this.line_ids:
					line_ids.append(line.id)
				line_pool.act_approved1(cr, uid, line_ids, context=context)
		return self.write(cr, uid, ids, {'state': 'approved2'}, context=context)

	def act_approved2(self, cr, uid, ids, context={}):
		line_pool = self.pool.get('asset.request.line')
		for this in self.browse(cr, uid, ids):
			if not this.line_ids:
				raise osv.except_osv(_(u'Lổi'), _(u'Vui lòng nhập liệu các yêu cầu tài sản trước khi đề xuất lên.'))
			else:
				line_ids = []
				for line in this.line_ids:
					line_ids.append(line.id)
				line_pool.act_approved2(cr, uid, line_ids, context=context)
		return self.write(cr, uid, ids, {'state': 'approved3'}, context=context)

	def act_approved3(self, cr, uid, ids, context={}):
		line_pool = self.pool.get('asset.request.line')
		for this in self.browse(cr, uid, ids):
			if not this.line_ids:
				raise osv.except_osv(_(u'Lổi'), _(u'Vui lòng nhập liệu các yêu cầu tài sản trước khi đề xuất lên.'))
			else:
				line_ids = []
				for line in this.line_ids:
					line_ids.append(line.id)
				line_pool.act_approved3(cr, uid, line_ids, context=context)
		return self.write(cr, uid, ids, {'state': 'done'}, context=context)

	def act_cancel(self, cr, uid, ids, context={}):
		line_pool = self.pool.get('asset.request.line')
		for this in self.browse(cr, uid, ids):
			if not this.reject_reson:
				raise osv.except_osv(_(u'Cảnh báo !!!'), _(u'Vui lòng đưa lý do từ chối vào mẩu.'))
			if not this.line_ids:
				raise osv.except_osv(_(u'Lổi'), _(u'Vui lòng nhập liệu các yêu cầu tài sản trước khi đề xuất lên.'))
			else:
				line_ids = []
				for line in this.line_ids:
					line_ids.append(line.id)
				line_pool.act_cancel(cr, uid, line_ids, context=context)
		for this in self.browse(cr, uid, ids):
			if this.state == 'approved1':
				self.write(cr, uid, [this.id], {'state': 'draft'}, context=context)
			if this.state == 'approved2':
				self.write(cr, uid, [this.id], {'state': 'approved1'}, context=context)
		return True

	def act_reset(self, cr, uid, ids, context={}):
		line_pool = self.pool.get('asset.request.line')
		for this in self.browse(cr, uid, ids):
			if not this.line_ids:
				raise osv.except_osv(_(u'Lổi'), _(u'Vui lòng nhập liệu các yêu cầu tài sản trước khi đề xuất lên.'))
			else:
				line_ids = []
				for line in this.line_ids:
					line_ids.append(line.id)
				line_pool.act_reset(cr, uid, line_ids, context=context)
		return self.write(cr, uid, ids, {'state': 'draft'}, context=context)

	def unlink(self, cr, uid, ids, context={}):
		for this in self.browse(cr, uid, ids):
			if this.state in ['approved1', 'approved2', 'approved3', 'done', 'cancel']:
				raise osv.except_osv(_(u'Cảnh báo !!!'),_(u'Không được xoá khi không ở trạng thái Bản Thảo'))
		return super(asset_request, self).unlink(cr, uid, ids, context=context)

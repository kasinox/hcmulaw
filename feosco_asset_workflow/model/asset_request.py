# -*- coding: utf-8 -*-
from openerp.osv import osv, fields
from openerp.tools.translate import _

class asset_request(osv.Model):
	_name = "asset.request"
	_inherit = "mail.thread"
	_columns = {
		'create_date': fields.datetime(u'Ngày tạo', readonly=True),
		'name': fields.char(u'Tên', required=True, readonly=True, states={'draft': [('readonly', False)]}),
		'department_id': fields.many2one('feosco.asset.department', u'Phòng ban cần', readonly=True, states={'draft': [('readonly', False)]}),
		'note': fields.text(u'Ghi chú', readonly=True, states={'draft': [('readonly', False)]}),
		'line_ids': fields.one2many('asset.request.line', 'request_id', u'Các tài sản Y/C', readonly=True, states={'draft': [('readonly', False)]}),
		'request_date': fields.date(u'Ngày y/c', readonly=True, states={'draft': [('readonly', False)]}),
		'state': fields.selection([
									('draft', u'Bản thảo'),
									('approved1', u'Chờ QT TB duyệt'),
									('approved2', u'Chờ BGH đã duyệt'),
									('approved3', u'Chờ mua'),
									('done', u'Hoàn tất'),
									('cancel', u'Từ chối')
								], u'Trạng thái', track_visibility='onchange')
	}

	_defaults = {
		'state': 'draft'
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
			if not this.line_ids:
				raise osv.except_osv(_(u'Lổi'), _(u'Vui lòng nhập liệu các yêu cầu tài sản trước khi đề xuất lên.'))
			else:
				line_ids = []
				for line in this.line_ids:
					line_ids.append(line.id)
				line_pool.act_confirm(cr, uid, line_ids, context=context)
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
				line_pool.act_confirm(cr, uid, line_ids, context=context)
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
				line_pool.act_confirm(cr, uid, line_ids, context=context)
		return self.write(cr, uid, ids, {'state': 'done'}, context=context)

	def act_cancel(self, cr, uid, ids, context={}):
		line_pool = self.pool.get('asset.request.line')
		for this in self.browse(cr, uid, ids):
			if not this.line_ids:
				raise osv.except_osv(_(u'Lổi'), _(u'Vui lòng nhập liệu các yêu cầu tài sản trước khi đề xuất lên.'))
			else:
				line_ids = []
				for line in this.line_ids:
					line_ids.append(line.id)
				line_pool.act_confirm(cr, uid, line_ids, context=context)
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
				line_pool.act_confirm(cr, uid, line_ids, context=context)
		return self.write(cr, uid, ids, {'state': 'draft'}, context=context)


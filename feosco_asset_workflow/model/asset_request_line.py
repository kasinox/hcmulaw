# -*- coding: utf-8 -*-
from openerp.osv import osv, fields
from openerp.tools.translate import _

class asset_request_line(osv.Model):
	_name = "asset.request.line"
	_columns = {
		'name': fields.char(u'Tên', required=True),
		'type': fields.selection([('new', u'Mới'), ('repair', u'Sữa chửa')], u'Loại đề nghị', required=True),
		'qty': fields.float(u'Số lượng', required=True),
		'reason': fields.text(u'Lý do', required=True),
		'request_id': fields.many2one('asset.request', u'Yêu cầu', required=True, ondelete='cascade'),
		'state': fields.selection([
			('draft', u'Bản thảo'),
			('approved1', u'QT TB duyệt'),
			('approved2', u'BGH đã duyệt'),
			('approved3', u'QT TB Đang mua'),
			('done', u'Hoàn tất cấp TB'),
			('cancel', u'Từ chối')
				], u'Trạng thái', track_visibility='onchange'),
	}

	_defaults = {
		'state': 'draft'
	}

	def act_confirm(self, cr, uid, ids, context={}):
		return self.write(cr, uid, ids, {'state': 'approved1'}, context=context)

	def act_approved1(self, cr, uid, ids, context={}):
		return self.write(cr, uid, ids, {'state': 'approved2'}, context=context)

	def act_approved2(self, cr, uid, ids, context={}):
		return self.write(cr, uid, ids, {'state': 'approved3'}, context=context)

	def act_approved3(self, cr, uid, ids, context={}):
		return self.write(cr, uid, ids, {'state': 'done'}, context=context)

	def act_cancel(self, cr, uid, ids, context={}):
		for this in self.browse(cr, uid, ids):
			if this.state == 'approved1':
				self.write(cr, uid, [this.id], {'state': 'draft'}, context=context)
			if this.state == 'approved2':
				self.write(cr, uid, [this.id], {'state': 'approved1'}, context=context)
			if this.state == 'approved3':
				self.write(cr, uid, [this.id], {'state': 'approved2'}, context=context)
		return True

	def act_reset(self, cr, uid, ids, context={}):
		return self.write(cr, uid, ids, {'state': 'draft'}, context=context)

	def unlink(self, cr, uid, ids, context={}):
		for this in self.browse(cr, uid, ids):
			if this.state in ['approved1', 'approved2', 'approved3', 'done', 'cancel']:
				raise osv.except_osv(_(u'Cảnh báo !!!'),_(u'Không được xoá khi không ở trạng thái Bản Thảo'))
		return super(asset_request_line, self).unlink(cr, uid, ids, context=context)

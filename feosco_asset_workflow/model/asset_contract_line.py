# -*- coding: utf-8 -*-
from openerp.osv import osv, fields

class asset_contract_line(osv.Model):

	_name = "asset.contract.line"

	_columns = {
		'name': fields.char(u'Tên tài sản', required=True),
		'uom_id': fields.many2one('product.uom', u'Đơn vị tính', required=True),
		'qty': fields.float(u'Số lượng', required=True),
		'price': fields.float(u'Giá thành'),
		'tax_ids': fields.many2many('account.tax', 'asset_contract_line_tax_rel', 'line_id', 'tax_id', u'Thuế'),
		'discount': fields.float(u'Giảm giá % (nếu có)'),
		'contract_id': fields.many2one('asset.contract', u'Hợp đồng', required=True, ondelete='cascade'),
		'stock_id': fields.many2one('asset.stock', u'Biên bản nghiệm thu'),
		'department_id': fields.many2one('feosco.asset.department', u'Phòng ban nhận'),
		'status': fields.char('Tình trạng hoạt động'),
		'type': fields.selection([('new', u'Trang bị mới'), ('repair', u'Sửa chữa')], u'Loại'),
		'total_time': fields.integer(u'Thời hạn bảo hành ( tháng )'),
		'user_id': fields.many2one('res.users', u'Cấp cho nhân viên'),
		'category_id': fields.many2one('account.asset.category', u'Danh mục tài sản'),
	}

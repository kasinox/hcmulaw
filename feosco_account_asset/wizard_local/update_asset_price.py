#-*- coding:utf-8 -*-
from openerp.osv import osv, fields
from openerp.tools.translate import _

class wiz_update_asset_price(osv.osv_memory):
	_name = "wiz.update.asset.price"
	_columns = {
		'purchase_value': fields.float(u'Giá mua ban đầu'),
		'salvage_value': fields.float(u'Giá trị không khấu hao', help=u'Đây là giá trị thiết lập không khấu hao, Ví dụ thiết lập tài sản A giá trị mua về là 10,000,000 VNĐ, nếu bạn muốn tài sản khấu hao 9,000,000 VNĐ và còn 1,000,000 dùng thanh lý thì thiết lập con số này là 1,000,000 VNĐ'),
		'percent': fields.float(u'Bao nhiêu % trên năm '),
		'depreciated': fields.float(u'Đã khấu hao nhiêu %'),
	}

	def update_asset_price(self, cr, uid, ids, context={}):
		if context and context.has_key('active_id'):
			if ids:
				this = self.browse(cr, uid, ids[0])
				if this.percent == 0:
					raise osv.except_osv(_(u'Cảnh báo !!!'),_(u'Không thể tính khấu hao mà % trên năm là 0'))
				cr.execute("update account_asset_asset SET purchase_value=%s , salvage_value=%s , feosco_percent=%s , feosco_depreciated=%s WHERE id=%s" % (this.purchase_value, this.salvage_value, this.percent, this.depreciated, context.get('active_id')))
				cr.commit()
				return self.pool.get('account.asset.asset').compute_depreciation_board(cr, uid, [context.get('active_id')])
			else:
				return False
		else:
			return False


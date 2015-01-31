#coding:utf-8
from openerp.osv import osv, fields
import logging
import base64
import os
from openerp.tools.translate import _
import datetime


class feosco_export_import(osv.osv_memory):

    _name = "feosco.export.import"

    __logger = logging.getLogger(_name)

    _columns = {
        'file': fields.binary('File'),
        'state': fields.selection([
            ('default', 'Not action'),
            ('succed', 'Finish')
                                  ],
            'State', readonly=True, states={'default': [('readonly', False)]}),
        'action': fields.selection([
           ('import', 'Import'),
           ('export', 'Export')],
           'Action', required=True, readonly=True, states={'default': [('readonly', False)]}),
        'excel_format': fields.char('Format', readonly=True),
        'path_image': fields.char('Path Image Folder', size = 256),
        'output_type': fields.selection([
            ('all', 'All'),
            ('scan', 'Inventoried'),
            ('not_scan', 'Not inventoried'),
        ], 'Condition'),
        'scan_time_id': fields.many2one('feosco.scan.time', 'Periodic'),
        'barcode_type_id': fields.many2one('feosco.barcode.type', 'Barcode'),
        'department_id': fields.many2one('feosco.asset.department', 'Department'),
        'user_id': fields.many2one('res.users', 'User'),
    }

    _defaults = {
        'output_type': 'all',
        'state': 'default',
        'action': 'export',
        'excel_format':'https://mega.co.nz/#!ElsAHKzY!fmFGjKSjbJK8PTpDQ5HVkOxvH6QUk4WcC7jmjRBkv78'
    }

    def action_change(self, cr, uid, ids, action, context={}):
        if action:
            if action == 'import':
                return {
                    'value': {'name': 'Import.xls'}
                }
            else:
                return {
                    'value': {'name': 'Export.xls'}
                }

    def export_excel(self, cr, uid, ids, context={}):
        tool = self.pool.get('feosco.excel')
        asset_pool = self.pool.get('account.asset.asset')
        for wiz in self.browse(cr, uid, ids):

            label = [u'Số Thứ Tự', u'Phòng ban', u'Mã', u'Tên', u'Đơn Vị', u'Số lượng', u'Năm sử dụng', u'Người sử dụng']
            condition = []
            if wiz.output_type in ['scan', 'not_scan']:
                condition = [('feosco_scan_time_id', '=', wiz.scan_time_id.id)]
            if wiz.output_type == 'all':
                condition = []
            if wiz.department_id:
                condition.append(('feosco_asset_department_id', '=', wiz.department_id.id))
            if wiz.user_id:
                condition.append(('feosco_user_id', '=', wiz.user_id.id))
            asset_ids = asset_pool.search(cr, uid, condition)
            if not asset_ids:
                raise osv.except_osv(_('Error'), _('Can not find data with your parameter'))
            list_tuple_data = []
            for asset in asset_pool.browse(cr, uid, asset_ids):
                tup = (asset.feosco_num, )
                if asset.feosco_asset_department_id:
                    tup += (asset.feosco_asset_department_id.name, )
                else:
                    tup += ('',)
                if asset.code:
                    tup += (asset.code, )
                else:
                    tup += ('', )
                if asset.name:
                    tup += (asset.name, )
                else:
                    tup += ('',)
                if asset.feosco_uom_id:
                    tup += (asset.feosco_uom_id.name, )
                else:
                    tup += ('', )
                if asset.feosco_qty:
                    tup += (asset.feosco_qty, )
                else:
                    tup += ('',)
                if asset.feosco_purchase_year_id:
                    tup += (asset.feosco_purchase_year_id.code, )
                else:
                    tup += ('',)
                if asset.feosco_user_id:
                    tup += (asset.feosco_user_id.name, )
                else:
                    tup += ('',)

                list_tuple_data.append(tup)

            attach_id = self.pool.get('ir.attachment').create(cr, uid,{
                'name': 'asset.xls',
                'datas': tool.export_data(label, list_tuple_data),
                'datas_fname': 'asset.xls',
                }, context=context)

            data_obj = self.pool.get('ir.model.data')
            form_view_id = data_obj._get_id(cr, uid, 'feosco_account_asset', 'extend_view_attachment_form')
            form_view = data_obj.read(cr, uid, form_view_id, ['res_id'])
            self.__logger.info('form_view_id: %s' % form_view)
            self.__logger.info("===> END: export_data()")
            return {
                'name': _('Dowload file'),
                'res_model': 'ir.attachment',
                'view_mode': 'form',
                'view_type': 'form',
                'views':  [(form_view['res_id'], 'form')],
                'type': 'ir.actions.act_window',
                'res_id': attach_id,
                'nodestroy': True,
                'target': 'new',
            }


    def _get_data(self, cr, uid, value):

        feosco_user_ids = self.pool.get('res.users').search(cr, uid, [('name', '=', value.get('feosco_user_id'))])
        categ_ids = self.pool.get('account.asset.category').search(cr, uid, [('name', '=', value.get('category_id'))])
        feosco_barcode_types = self.pool.get('feosco.barcode.type').search(cr, uid, [('name', '=', value.get('feosco_barcode_type'))])

        return {
            'category_id': categ_ids[0] if categ_ids else None,
            'feosco_barcode_type': feosco_barcode_types[0] if feosco_barcode_types else None,
            'feosco_user_id': feosco_user_ids[0] if feosco_user_ids else None,

            }



    def import_excel(self, cr, uid, ids, context={}):
        """
        ===================================================
        val[0]: Mã barcode
        val[1]: Tên
        val[2]: Serial Tham chiếu
        val[3]: Phòng ban (*)
        val[4]: Ngày mua về
        val[5]: Giá mua về
        val[6]: Kiểu định dạng barcode (*)
        val[7]: Người sử dụng (*)
        val[8]: Hình ảnh cần import (*)
        val[9]: Danh mục TS (*)
        ===================================================
        Code: barcode ex: 123456789
        name: Tên ex: Máy In Barcode
        category: danh mục TS ex: Hàng mua về
        Purchase value: giá mua vào ex: 100000000
        Purchase Date (YYYY-MM-DD): ngày nhập về 12-12-2014
        method_time: thời gian khấu hao ex: number
        method_number: số lần khấu hao ex: 10
        method_period: 3
        method: linear
        prorata:
        feosco_barcode_type: loại barcode ex: QR
        feosco_user_id: người sử dụng
        code: số seri ( tham chiếu )
        image: tên hình ảnh
        =================================================
        1. Mã barcode
        2. Tên TS
        3. Tham chiếu (code)
        4. Phòng ban.
        5. Ngày mua về
        6. Giá mua về.
        7. Định dạng barcode
        8. Trạng thái sử dụng
        9. Số lượng phân bổ.

        """
        self.__logger.info('===> begin import_excel')

        orm_excel = self.pool.get('feosco.excel')
        orm_asset = self.pool.get('account.asset.asset')
        orm_categ = self.pool.get('account.asset.category')
        orm_barcode = self.pool.get('feosco.barcode.type')
        orm_department = self.pool.get('feosco.asset.department')
        orm_user = self.pool.get('res.users')

        for wiz in self.browse(cr, uid, ids):
            barcode_id = wiz.barcode_type_id.id if wiz.barcode_type_id else None

            path = os.path.dirname(os.path.abspath(__file__)) + "/data.xls"
            f = open(path, "w")
            try:
                strDecodeToByte = base64.b64decode(wiz.file)
                f.write(strDecodeToByte)
                f.close()
                self.__logger.info('...saving to: %s' % path)
            except Exception, ex:
                self.__logger.error('error: %s' % ex)


            dataDictReturn = orm_excel.import_data(path)

            self.__logger.info('...return sheet by sheet.....')
            index = 0
            for sheet, value in dataDictReturn.iteritems():
                del value[0]

                for val in value:

                    self.__logger.info('...merge data: %s and len %s' % (val, len(val)))
                    purchase_date = ''
                    try:
                        purchase_date = datetime.datetime.strptime(val[4], "%Y-%m-%d") if val[4] else None
                    except:
                        raise osv.except_osv(_('Error'),_('Purchase Date from excel file error, please validate this and move format col to character'))
                    valNew = {
                        'feosco_code': val[0],
                        'name': val[1],
                        'code': val[2],
                        'purchase_date': purchase_date,
                        'purchase_value': val[5],
                        'state': 'open',
                        'feosco_qty': val[9] if val[9] else 1,
                    }
                    checkAsset_ids = orm_asset.search(cr, uid, [('feosco_code', '=', val[0])])
                    if not val[0]:
                        self.__logger.error(': Ma code khong duoc dua vao')
                        continue
                    if checkAsset_ids:
                        self.__logger.error(': TS da co trong he thong tuong ung vs ma code: %s' % val[0])
                        continue
                    else:
                        department_ids = orm_department.search(cr, uid, [('name', '=', val[3])])
                        if department_ids:
                            valNew.update({'feosco_asset_department_id': department_ids[0]})
                        else:
                            valNew.update({'feosco_asset_department_id': orm_department.create(cr, uid, {'name': val[3]})})
                        barcodeType_ids = orm_barcode.search(cr, uid, [('name', '=', val[6])])
                        if barcode_id:
                            valNew.update({'feosco_barcode_type': barcode_id})
                        else:
                            if not barcodeType_ids:
                                # default barcode Code128
                                barcodeType_ids = orm_barcode.search(cr, uid, [('name', '=', 'Code128')])
                                valNew.update({'feosco_barcode_type': barcodeType_ids[0]})
                            else:
                                valNew.update({'feosco_barcode_type': barcodeType_ids[0]})
                        if val[7]:
                            user_ids = orm_user.search(cr, uid, [('name', '=', val[7])])
                            if user_ids:
                                valNew.update({'feosco_user_id': user_ids[0]})
                            else:
                                valNew.update({'feosco_user_id': orm_user.create(cr, uid, {'name': val[7], 'login': val[7]})})
                        if val[8]:
                            categ_ids = orm_categ.search(cr, uid, [('name', '=', val[8])])
                            if categ_ids:
                                valNew.update({'category_id': categ_ids[0]})
                            else:
                                valNew.update({'category_id': orm_categ.search(cr, uid, [])[0] if orm_categ.search(cr, uid, []) else None})
                        else:
                            valNew.update({'category_id': orm_categ.search(cr, uid, [])[0] if orm_categ.search(cr, uid, []) else None})
                        # ============= remove image asset on server =================
                        # if val[8]:
                        #     try:
                        #         imagePath = wiz.path_image + "%s" % val[8] + ".png"
                        #         with open(imagePath, "rb") as image_file:
                        #             imageBaseString = base64.b64encode(image_file.read())
                        #             valNew.update({
                        #                'feosco_image': imageBaseString,
                        #             })
                        #     except:
                        #         raise osv.except_osv((u'Lỗi '),(u'Không tìm thấy thư mục chứa hình hoặc ko tìm thấy hình.'))
                        #=============================================================
                        if not valNew.has_key('purchase_date') or not valNew.get('purchase_date'):
                            valNew.update({'purchase_date': datetime.datetime.today()})
                        self.__logger.info('valNew: %s' % valNew)
                        orm_asset.create(cr, uid, valNew)
                        index += 1
            self.__logger.info('...insert total: [ %s ]' % index)
            self.write(cr, uid, [wiz.id], {'state': 'succed'})
            self.__logger.info('===> end import_excel')
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'feosco.export.import',
                'view_mode': 'form',
                'view_type': 'form',
                'res_id': wiz.id,
                'views': [(False, 'form')],
                'target': 'new',
                'name': 'Import Done'
            }


feosco_export_import()
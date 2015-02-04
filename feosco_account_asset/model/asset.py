# coding:utf-8

from openerp.osv import osv, fields
from openerp.tools.translate import _
import logging
from datetime import datetime
from dateutil.relativedelta import relativedelta

class account_asset_asset(osv.osv):

    _inherit = 'account.asset.asset'

    __logger = logging.getLogger(_inherit)

    def default_get(self, cr, uid, fields_list, context={}):
        default_vals = super(account_asset_asset, self).default_get(cr, uid, fields_list, context=context)
        return default_vals


    def _get_barcode(self, cr, uid, type='EAN13', context=None):
        if type == 'EAN13':
            return self.pool.get('ean13').generate_ean13(cr, uid, context=context)
        elif type == 'EAN8':
            return self.pool.get('ean8').generate_ean8(cr, uid, context=context)
        else:
            return False

    def _default_currency(self, cr, uid, context=None):
        currency_pool = self.pool.get('res.currency')
        currency_ids = currency_pool.search(cr, uid, [('name', '=', 'VND')], context=context)
        if not currency_ids:
            currency_ids = currency_pool.search(cr, uid, [], context=context)
        return currency_ids[0]

    def create_role(self, cr, uid, vals, context={}):
        feosco_barcode_type_id = vals.get('feosco_barcode_type', False)
        orm_bctype = self.pool.get('feosco.barcode.type')
        barcode_type = orm_bctype.browse(cr, uid, feosco_barcode_type_id)
        barcode = vals.get('feosco_code', False)
        if barcode_type and not barcode:
            vals.update({'feosco_code': self._get_barcode(cr, uid, barcode_type.code, context=context)})
        return True

    def act_print_barcode_PT9700(self, cr, uid, ids, context={}):
        print_type="chopped"
        return self.pool.get('feosco.print.asset').record_asset_to_print(cr, uid, ids, print_type, context=context)

    def action_reset(self, cr, uid, ids, context={}):
        if ids:
            return self.write(cr, uid, ids, {'state': 'draft'})
        else:
            return False



    def create(self, cr, uid, vals, context=None):
        self.__logger.info('create() BEGIN')
        self.create_role(cr, uid, vals, context=context)
        self.__logger.info(vals)

        if not vals.get('code'):

            feosco_barcode_type_ids = self.pool.get('feosco.barcode.type').search(cr, uid, [('code', '=', 'QR')])
            if feosco_barcode_type_ids:
                vals['feosco_barcode_type'] = feosco_barcode_type_ids[0]
            else:
                raise osv.except_osv(_('Error'), _('Missing QR code type in system'))

            gross_pool = self.pool.get('feosco.asset.gross.from')
            purchase_year_pool = self.pool.get('feosco.purchase.year')
            asset_type = self.pool.get('feosco.asset.type')
            if not vals.has_key('feosco_asset_gross_from_id') or not vals.get('feosco_asset_gross_from_id'):
                gross_ids = gross_pool.search(cr, uid, [('default', '=', True)])
                if gross_ids:
                    vals['feosco_asset_gross_from_id'] = gross_ids[0]
                else:
                    raise osv.except_osv(_('Error'), _('Contact admin default Gross from'))
            if not vals.has_key('feosco_purchase_year_id') or not vals.get('feosco_purchase_year_id'):
                year_ids = purchase_year_pool.search(cr, uid, [('default', '=', True)])
                if year_ids:
                    vals['feosco_purchase_year_id'] = year_ids[0]
                else:
                    raise osv.except_osv(_('Error'), _('Contact admin default Purchase Year'))
            if not vals.has_key('feosco_asset_type_id') or not vals.get('feosco_asset_type_id'):
                type_ids = asset_type.search(cr, uid, [('default', '=', True)])
                if type_ids:
                    vals['feosco_asset_type_id'] = type_ids[0]
                else:
                    raise osv.except_osv(_('Error'), _('Contact admin default Asset Type'))
            vals['code'] = ''
            vals['code'] += gross_pool.browse(cr, uid, vals['feosco_asset_gross_from_id']).name
            vals['code'] += '.'
            vals['code'] += purchase_year_pool.browse(cr, uid, vals['feosco_purchase_year_id']).name
            vals['code'] += '.'
            vals['code'] += asset_type.browse(cr, uid, vals['feosco_asset_type_id']).name
            department_pool = self.pool.get('feosco.asset.department')
            if vals.has_key('feosco_asset_department_id') and vals['feosco_asset_department_id']:
                vals['code'] += '.'
                vals['code'] += department_pool.browse(cr, uid, vals['feosco_asset_department_id']).phone
            else:
                vals['code'] += '.xxx'
            vals['code'] += '.'
            vals['code'] += str(self._get_serial_num(cr, uid))

            qr_pool = self.pool.get('ir.qrcode')
            image64 = qr_pool.general_qrcode(cr, uid, {
                'id': str(self._get_serial_num(cr, uid)),
                'code': vals['code'],
                'name': vals['name']
            })
            if image64:
                vals['feosco_barcode_image'] = image64





        self.__logger.info('create() END')
        return super(account_asset_asset, self).create(cr, uid, vals, context=context)

    def _get_scan_info(self, cr, uid, ids, fname, arg, context={}):
        self.__logger.info('_get_scan_info')
        res = {}
        orm_scan = self.pool.get('feosco.asset.scan')
        for this in self.browse(cr, uid, ids):
            res[this.id] = {
                'feosco_scan': False,
                'feosco_scan_date': None,
            }
            scan_ids = orm_scan.search(cr, uid, [('asset_id', '=', this.id)])
            if scan_ids:
                scan_ids.sort()
                scan_id = scan_ids.pop()
                res[this.id] = {
                    'feosco_scan': True,
                    'feosco_scan_date': orm_scan.browse(cr, uid, scan_id).create_date,
                }
        self.__logger.info(res)
        self.__logger.info('_get_scan_info')
        return res


    def validate(self, cr, uid, ids, context={}):
        context.update({'active_ids': ids})
        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'feosco.wizard.asset.assign',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': context,
            'nodestroy': True,
        }

    def _get_serial_num(self, cr, uid, context={}):
        count_ids = self.search(cr, uid, [])
        num_list = self.read(cr, uid, count_ids, ['feosco_num'])
        array_list = []
        for num in num_list:
            array_list.append(num.get('feosco_num'))
        array_list.sort()
        if array_list:
            return array_list.pop() + 1
        else:
            return 1

    def name_get(self, cr, uid, ids, context=None):
        if isinstance(ids, (list, tuple)) and not len(ids):
            return []
        if isinstance(ids, (long, int)):
            ids = [ids]
        reads = self.read(cr, uid, ids, ['name','parent_id'], context=context)
        res = []
        for record in reads:
            name = record['name']
            if record['parent_id']:
                name = record['parent_id'][1]+' / '+name
            res.append((record['id'], name))
        return res

    def _amount_residual(self, cr, uid, ids, name, args, context=None):
        cr.execute("""SELECT
                l.asset_id as id, SUM(abs(l.debit-l.credit)) AS amount
            FROM
                account_move_line l
            WHERE
                l.asset_id IN %s GROUP BY l.asset_id """, (tuple(ids),))
        res=dict(cr.fetchall())
        for asset in self.browse(cr, uid, ids, context):
            res[asset.id] = asset.purchase_value - res.get(asset.id, 0.0) - asset.salvage_value
        for id in ids:
            res.setdefault(id, 0.0)
        return res

    _columns = {

        'feosco_asset_gross_from_id': fields.many2one('feosco.asset.gross.from', 'Gross from', track_visibility='onchange', readonly=True, states={'draft': [('readonly', False)]}),
        'feosco_purchase_year_id': fields.many2one('feosco.purchase.year', 'Purchase Year', track_visibility='onchange', readonly=True, states={'draft': [('readonly', False)]}),
        'feosco_asset_type_id': fields.many2one('feosco.asset.type', 'Type', readonly=True, states={'draft': [('readonly', False)]}),

        'feosco_num': fields.integer('No .', readonly=True, states={'draft': [('readonly', False)]}),
        'feosco_asset_department_id': fields.many2one('feosco.asset.department', 'Department', track_visibility='onchange', readonly=True, states={'draft': [('readonly', False)]}),
        'feosco_qty': fields.integer('Quantity', track_visibility='onchange', readonly=True, states={'draft': [('readonly', False)]}),
        'feosco_code': fields.char('Code', size=64, readonly=True, states={'draft':[('readonly', False)]}),
        'feosco_image': fields.binary('Image', readonly=True, states={'draft': [('readonly', False)]}),
        'feosco_print': fields.boolean('Print', readonly=True, states={'draft': [('readonly', False)]}),
        'feosco_history_ids': fields.one2many('feosco.asset.history', 'asset_id', 'History',
                                              readonly=True,
                                              states={'draft': [('readonly', False)]}),
        'feosco_scan_ids': fields.one2many('feosco.asset.scan', 'asset_id', 'Scans'),
        'feosco_barcode_type': fields.many2one('feosco.barcode.type', 'Barcode Type',
                                               readonly=True,
                                               states={'draft': [('readonly',False)]}, track_visibility='onchange'),
        'feosco_user_id': fields.many2one('res.users', 'User', readonly=True, states={'draft':[('readonly',False)]},  track_visibility='onchange'),
        'feosco_status_id': fields.many2one('feosco.asset.status', 'Status', readonly=True),
        'feosco_image_his': fields.binary('Image old', readonly=True, states={'draft': [('readonly',False)]}),
        'feosco_location': fields.char('Location Use', readonly=True, states={'draft': [('readonly', False)]}),
        'feosco_uom_id': fields.many2one('product.uom', 'Uom', track_visibility='onchange', readonly=True, states={'draft': [('readonly', False)]}),
        'feosco_scan_time_id': fields.many2one('feosco.scan.time', 'Scan schedule'),
        'method_time': fields.selection([
                                            ('number', 'Number of Depreciations'),
                                            ('end', 'Ending Date'),
                                            ('percent', 'Percent (%) / Year'),
                                            ], 'Time Method', required=True),
        'method_period': fields.integer('Period Length' , track_visibility='onchange', readonly=True, states={'draft': [('readonly', False)]}),
        'feosco_percent': fields.float('Percent (%) of year', track_visibility='onchange', readonly=True, states={'draft': [('readonly', False)]}),
        'feosco_depreciated': fields.float('Depreciated (%)', track_visibility='onchange', readonly=True, states={'draft': [('readonly', False)]}),
        'feosco_barcode_image': fields.binary('QR code', readonly=True),
    }

    _defaults = {
        'feosco_percent': 10.00,
        'feosco_depreciated': 0.00,
        'feosco_qty': 1.0,
        'feosco_num': _get_serial_num,
        'method_time': 'percent',
    }

    def _needaction_domain_get(self, cr, uid, context={}):
        scan_time_pool = self.pool.get('feosco.scan.time')
        scan_time_ids = scan_time_pool.search(cr, uid, [('active_scan', '=', True)])
        dom = []
        if scan_time_ids:
            dom.append(('feosco_scan_time_id', '!=', scan_time_ids[0]))
        else:
            dom.append(('feosco_scan_time_id', '=', None))
        return dom

    def compute_depreciation_board(self, cr, uid, ids, context=None):
        depreciation_lin_obj = self.pool.get('account.asset.depreciation.line')
        res = super(account_asset_asset, self).compute_depreciation_board(cr, uid, ids, context=context)
        for this in self.browse(cr, uid, ids):
            if this.method_time == 'percent':
                sql = 'delete from account_asset_depreciation_line where asset_id=%s' % this.id
                cr.execute(sql)
                purchase_value = this.purchase_value
                if this.feosco_depreciated != 0:
                    feosco_depreciation = this.purchase_value / 100 * this.feosco_depreciated
                else:
                    feosco_depreciation = this.purchase_value / 100
                current_value = purchase_value - feosco_depreciation
                count = (100 - this.feosco_depreciated) / this.feosco_percent
                count_int = int(count)
                j = 0
                remaining_value = current_value
                depreciated_value = 0
                for i in range(count_int):
                    j += 1
                    depreciation_date = datetime(2014, 1, 1) + relativedelta(months = 12 + 12 * i)
                    depreciated_value += current_value / count
                    remaining_value = current_value - depreciated_value
                    vals = {
                        'amount': current_value / count,
                        'asset_id': this.id,
                        'sequence': i + 1,
                        'name': str(this.id) +'/' + str(i),
                        'remaining_value': remaining_value,
                        'depreciated_value': depreciated_value,
                        'depreciation_date': depreciation_date.strftime('%Y-%m-%d'),
                    }
                    depreciation_lin_obj.create(cr, uid, vals, context=context)
                if count_int < count:

                    depreciation_date = datetime(2014, 1, 1) + relativedelta(months = 12 + 12 * j)

                    vals = {
                        'amount': current_value - depreciated_value,
                        'asset_id': this.id,
                        'sequence': j + 1,
                        'name': str(this.id) + '/' + str(i),
                        'remaining_value': 0,
                        'depreciated_value': current_value,
                        'depreciation_date': depreciation_date.strftime('%Y-%m-%d'),
                    }
                    depreciation_lin_obj.create(cr, uid, vals, context=context)
        return res


account_asset_asset()


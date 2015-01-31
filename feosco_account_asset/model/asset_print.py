#-*- coding:utf-8 -*-
from openerp.osv import osv, fields
import json
import logging

class feosco_print_asset(osv.osv):
    _name = "feosco.print.asset"
    __logger = logging.getLogger(_name)
    _columns = {
                'create_uid': fields.many2one('res.users', 'User Action', readonly=True),
                'create_date': fields.datetime('Create on', readonly=True),
                'asset_id': fields.many2one('account.asset.asset', 'Asset'),
                'print_type': fields.selection([('chopped', 'Slip'), ('ligature', 'Not Slip')], string='Print Type'),
                'company_id': fields.many2one('res.company', 'Company', required=True),
                'state': fields.selection([
                    ('waiting', 'Waiting Printer Call'),
                    ('done', 'Send Printer is succed'),
                ], string='State')
                }

    _defaults = {
        'company_id': lambda self, cr, uid, context: self.pool.get('res.company')._company_default_get(cr, uid, 'account.asset.category', context=context),
        'state': 'waiting',
    }

    _order = "create_date desc"
    
    def get_asset_for_printer(self, cr, uid, context={}):
        self.__logger.info('get_asset_for_printer BEGIN')
        self_ids = self.search(cr, uid, [('create_uid', '=', uid), ('state', '=', 'waiting')])
        vals = []
        for object in self.browse(cr, uid, self_ids):
            vals.append({
                'name': object.asset_id.name,
                'code': object.asset_id.code,
                'purchase_date': object.asset_id.purchase_date,
                'print_type': object.print_type,
                'department': object.asset_id.feosco_asset_department_id.name if object.asset_id.feosco_asset_department_id else '',
                'location': object.asset_id.feosco_location if object.asset_id.feosco_location else '',
                'User': object.asset_id.feosco_user_id.name if object.asset_id.feosco_user_id else ''

            })
        self.write(cr, uid, self_ids, {'state': 'done'})
        self.__logger.info('return vals: %s' % vals)
        self.__logger.info('get_asset_for_printer END')
        return json.dumps(vals)


    def record_asset_to_print(self, cr, uid, asset_ids, print_type, context=None):
        if asset_ids:
            # # Check if this asset already to run by this users, if there, remove it
            # search_args = [
            #     ('create_uid','=',uid),
            #     ('asset_id', 'in', asset_ids),
            #     ('state', '=', 'waiting')
            # ]
            # res_id = self.search(cr, uid, search_args, context=context)
            # if res_id:
            #     existed_assets = self.read(cr, uid, res_id, ['asset_id'])
            #     existed_asset_ids = [existed_asset_id['asset_id'][0] for existed_asset_id in existed_assets]
            #     new_asset_ids = filter(lambda x: x not in existed_asset_ids, asset_ids)
            #     asset_ids = new_asset_ids
            #
            # # If not exits, create to print
            for asset_id in asset_ids:
                self.create(cr, uid, {'asset_id': asset_id, 'print_type':print_type})
                
        return True
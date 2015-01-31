# -*- coding:utf-8 -*-
from openerp.osv import osv, fields
import logging

class feosco_move_department(osv.osv_memory):

    _name = "feosco.move.department"

    _logger = logging.getLogger(_name)

    _columns = {
        'department_id': fields.many2one('feosco.asset.department', 'Department', required=True),
        'user_id': fields.many2one('res.users', 'User'),
    }

    def moving(self, cr, uid, ids, context={}):
        self._logger.info('moving begin')
        if context.has_key('active_ids'):
            orm_asset = self.pool.get('account.asset.asset')
            his_pool = self.pool.get('feosco.asset.history')
            avai_ids = context.get('active_ids')
            for wiz in self.browse(cr, uid, ids):
                depart_id = wiz.department_id.id
                val = {'feosco_asset_department_id': depart_id}
                if wiz.user_id:
                    val.update({'feosco_user_id': wiz.user_id.id})
                orm_asset.write(cr, uid, avai_ids, val)

                self._logger.info(val)
                for ass_id in avai_ids:
                    his_val = {
                        'asset_id': ass_id,
                        'user_id': uid,
                    }
                    act = u'Chuyển phòng cho tài sản: %s \n' % wiz.department_id.name
                    if wiz.user_id:
                        asset = orm_asset.browse(cr, uid, ass_id)
                        if asset.feosco_user_id:
                            act += u'Chuyển tài sản từ người dùng: '+  asset.feosco_user_id.name  + u' sang cho người dùng :' + wiz.user_id.name
                        else:
                            act += u'Chuyển tài sản cho người dùng: ' + wiz.user_id.name
                    his_val.update({'action': act})
                    his_pool.create(cr, uid, his_val)


                self._logger.info('moving end')
                return {'type': 'ir.actions.act_window_close'}

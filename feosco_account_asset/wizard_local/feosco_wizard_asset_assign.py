#coding:utf-8
from openerp.osv import osv, fields
from openerp.tools.translate import _

class feosco_wizard_asset_assign(osv.osv_memory):
    
    _name = 'feosco.wizard.asset.assign'
    
    _columns = {
        'user_id': fields.many2one('res.users', 'User'),
        'public': fields.boolean('Public Asset', help='If asset have not owner, but this asset use for all.'),
    }

    def action_assign(self, cr, uid, ids, context={}):

        asset_orm = self.pool.get('account.asset.asset')
        if not context or not context.has_key('active_ids'):
            raise osv.except_osv(_('Error, can not find Employee Assign'), _(''))
        else:
            asset_ids = context.get('active_ids')
            if ids:
                wiz_id = ids[0]
                wiz = self.browse(cr, uid, wiz_id)
                if wiz.public == False:
                    user_id = self.browse(cr, uid, wiz_id).user_id.id

                    for asset in asset_orm.browse(cr, uid, asset_ids):
                        val_up = {
                            'feosco_user_id': user_id
                        }
                        if asset.state == 'draft':
                            val_up.update({'state': 'open'})
                        asset_orm.write(cr, uid, asset_ids, val_up)
                    for aset_id in asset_ids:
                        self.pool.get('feosco.asset.history').create(cr, uid, {
                            'user_id': uid,
                            'asset_id': aset_id,
                            'action': 'Assigned Asset'})
                    return {'type': 'ir.actions.act_window_close'}
                else:
                    asset_orm.write(cr, uid, asset_ids, {'state': 'open'})
                    for aset_id in asset_ids:
                        self.pool.get('feosco.asset.history').create(cr, uid, {
                            'user_id': uid,
                            'asset_id': aset_id,
                            'action': 'Public Asset'})
                    return {'type': 'ir.actions.act_window_close'}



            else:
                raise osv.except_osv(_('Error, can not find Employee Assign'), _(''))

feosco_wizard_asset_assign()


#coding:utf-8

from openerp.osv import osv, fields


class feosco_asset_history(osv.osv):

    _name = 'feosco.asset.history'

    _columns = {
        'asset_id': fields.many2one('account.asset.asset', 'Asset', required=True, ondelete="cascade"),
        'user_id': fields.many2one('res.users', 'User'),
        'create_uid': fields.many2one('res.users', 'Create by', readonly=True),
        'create_date': fields.datetime('Create on', readonly=True),
        'action': fields.text('Action', required=True),
    }
    _order = 'create_date desc'

    _defaults = {
    }

feosco_asset_history()

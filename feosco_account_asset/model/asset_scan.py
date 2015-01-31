#-*- coding:utf-8-*-
from openerp.osv import osv, fields

class feosco_asset_scan(osv.osv):

    _name = "feosco.asset.scan"

    _columns = {
        'name': fields.char('Name', size=128),
        'create_date': fields.datetime('Scan on', readonly=True),
        'note': fields.text('Note', required=True),
        'asset_id': fields.many2one('account.asset.asset', 'Asset', required=True, ondelete="cascade"),
        'scan_time_id': fields.related('asset_id', 'feosco_scan_time_id', relation="feosco.scan.time", string = "Schedule time"),
        'image': fields.binary('Image'),
    }

    _order = 'create_date DESC'


feosco_asset_scan()
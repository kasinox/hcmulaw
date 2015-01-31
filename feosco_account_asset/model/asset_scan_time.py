#-*- coding:utf-8 -*-
from openerp.osv import osv, fields
import datetime
from openerp.tools.translate import _

class feosco_scan_time(osv.osv):
    _name = "feosco.scan.time"

    def _get_active(self, cr, uid, ids, fName, arg, context={}):
        res = {}
        for this in self.browse(cr, uid, ids):
            DATETIME_FORMAT = "%Y-%m-%d"
            dt_from = datetime.datetime.strptime(this.dt_from, DATETIME_FORMAT)
            dt_to = datetime.datetime.strptime(this.dt_to, DATETIME_FORMAT)
            now = datetime.datetime.today()
            if dt_from <= now <= dt_to:
                res[this.id] = True
            else:
                res[this.id] = False
        return res

    _columns = {
        'name': fields.char('Name', size=128, required=True),
        'dt_from': fields.date('From date', required=True),
        'dt_to': fields.date('To date', required=True),
        'active_scan': fields.function(_get_active, type='boolean', string='Active', store = {
            'feosco.scan.time': (lambda self, cr, uid, ids, c={}: ids, ['dt_from', 'dt_to'], 10),
        })
    }

    def create(self, cr, uid, vals, context={}):
        old_ids = self.search(cr, uid, [])
        for this in self.browse(cr, uid, old_ids):
            DATETIME_FORMAT = "%Y-%m-%d"
            dt_from = datetime.datetime.strptime(this.dt_from, DATETIME_FORMAT)
            dt_to = datetime.datetime.strptime(this.dt_to, DATETIME_FORMAT)
            val_from = datetime.datetime.strptime(vals['dt_from'], DATETIME_FORMAT)
            val_to = datetime.datetime.strptime(vals['dt_to'], DATETIME_FORMAT)
            if dt_from <= val_from <= dt_to:
                raise osv.except_osv(_('Error'),_('From and to date is not equal %s' % this.name))
            if dt_from <= val_to <= dt_to:
                raise osv.except_osv(_('Error'),_('From and to date is not equal %s' % this.name))
        return super(feosco_scan_time, self).create(cr, uid, vals, context=context)
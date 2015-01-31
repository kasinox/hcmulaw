# -*- coding: utf-8 -*-

from openerp.osv import fields,osv
from openerp.osv.orm import except_orm
from openerp.tools.translate import _


def isodd(x):
    return bool(x % 2)


class ean13(osv.osv):
    _name = 'ean13'
    _auto = False

    def _get_ean_next_code(self, cr, uid, context=None):
        if context is None:
            context = {}
        sequence_obj = self.pool.get('ir.sequence')
        ean = sequence_obj.next_by_code(cr, uid, 'asset.ean13.code', context=context)
        if not ean or len(ean) > 12:
            raise except_orm(_("Configuration Error!"),
                                 _("There next sequence is upper than 12 characters. This can't work."
                                   "You will have to redefine the sequence or create a new one"))
        else:
            ean = (len(ean[0:6]) == 6 and ean[0:6] or ean[0:6].ljust(6, '0')) + ean[6:].rjust(6, '0')
        return ean

    def _get_ean_key(self, code):
        sum = 0
        for i in range(12):
            if isodd(i):
                sum += 3 * int(code[i])
            else:
                sum += int(code[i])
        key = (10 - sum % 10) % 10
        return str(key)

    def generate_ean13(self, cr, uid, context=None):
        ean13 = False
        if context is None:
            context = {}
        ean = self._get_ean_next_code(cr, uid, context=context)
        if len(ean) != 12:
            raise except_orm(_("Configuration Error!"),
                                 _("This sequence is different than 12 characters. This can't work."
                                   "You will have to redefine the sequence or create a new one"))
        key = self._get_ean_key(ean)
        ean13 = ean + key
        return ean13

    def un_link(self, cr, uid, ids, context={}):
        raise osv.except_osv(_('Error'), _('Can not delete this'))
        return super(ean13, self).un_link(cr, uid, ids, context=context)

class ean8(osv.osv):
    _name = 'ean8'
    _auto = False

    def _get_ean_next_code(self, cr, uid, context=None):
        if context is None:
            context = {}
        sequence_obj = self.pool.get('ir.sequence')
        ean = sequence_obj.next_by_code(cr, uid, 'asset.ean8.code', context=context)
        if not ean or len(ean) > 7:
            raise except_orm(_("Configuration Error!"),
                                 _("There next sequence is upper than 4 characters. This can't work."
                                   "You will have to redefine the sequence or create a new one"))
        else:
            ean = (len(ean[0:3]) == 3 and ean[0:3] or ean[0:3].ljust(3, '0')) + ean[3:].rjust(4, '0')
        return ean

    def _get_ean_key(self, code):
        sum = 0
        for i in range(7):
            if not isodd(i):
                sum += 3 * int(code[i])
            else:
                sum += int(code[i])
        key = (10 - sum % 10) % 10
        return str(key)

    def generate_ean8(self, cr, uid, context=None):
        ean8 = False
        if context is None:
            context = {}
        ean = self._get_ean_next_code(cr, uid, context=context)
        if len(ean) != 7:
            raise except_orm(_("Configuration Error!"),
                                 _("This sequence is different than 7 characters. This can't work."
                                   "You will have to redefine the sequence or create a new one"))
        key = self._get_ean_key(ean)
        ean8 = ean + key
        return ean8
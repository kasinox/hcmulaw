# -*- coding:utf-8 -*-

import logging
import unicodedata

from openerp import tools
import openerp.modules
import subprocess
from openerp.osv import fields, osv
from openerp.tools.translate import _


_logger = logging.getLogger(__name__)


class feosco_translate(osv.osv_memory):

    _name = "feosco.translate"



    def act_translate(self, cr, uid, ids, context={}):
        _logger.info('act_translate() BEGIN')
        modpath = openerp.modules.get_module_path('translate')
        cr.execute("delete from ir_translation")
        cr.commit
        arg = '*.po'
        paths = subprocess.check_output(['find', modpath, '-name', arg], shell=False)
        paths = paths.split('\n')
        for path in paths:
            _logger.info('Begin loading and translate file: %s' % path)
            context = {'overwrite': True}
            tools.trans_load(cr, path, u'vi_VN', False, path.split("/").pop().split('.')[0] , context=context)
        _logger.info('act_translate() END')
        return True

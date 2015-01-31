#-*- coding:utf-8 -*-

from openerp.osv import osv
import base64
import openerp
import logging

class update_logo(osv.osv_memory):

	_name = "update.logo"
	__logger = logging.getLogger(_name)


	def update_logo_company(self, cr, uid, context={}):
		para_pool = self.pool.get('ir.config_parameter')
		company_pool = self.pool.get('res.company')
		insert_ids = para_pool.search(cr, uid, [('key', '=', 'vietnam')])
		if not insert_ids:
			para_pool.create(cr, uid, {'key': 'vietnam', 'value': 'vietnam'})
			yourCompany_ids = company_pool.search(cr, uid, [])
			if yourCompany_ids:
				modpath = openerp.modules.get_module_path('web_remove_odoo')
				path_core = openerp.modules.get_module_path('web')

				path_logo = modpath + '/logo/' + 'company.png'
				fn = open(path_logo, 'r')
				company_pool.write(cr, uid, yourCompany_ids, {'logo': base64.encodestring(fn.read())})
				fn.close()

				from_file01 = modpath + '/html/database_manager.html'
				from_file02 = modpath + '/html/database_selector.html'
				from_file03 = modpath + '/static/src/img/favicon.ico'
				from_file04 = modpath + '/static/src/img/logo.png'
				from_file05 = modpath + '/static/src/img/logo2.png'
				from_file06 = modpath + '/static/src/img/nologo.png'



				to_file01 = path_core + '/views/database_manager.html'
				to_file02 = path_core + '/views/database_selector.html'
				to_file03 = path_core + '/static/src/img/favicon.ico'
				to_file04 = path_core + '/static/src/img/logo.png'
				to_file05 = path_core + '/static/src/img/logo2.png'
				to_file06 = path_core + '/static/src/img/nologo.png'


				vals = {
					from_file01: to_file01,
					from_file02: to_file02,
					from_file03: to_file03,
					from_file04: to_file04,
					from_file05: to_file05,
					from_file06: to_file06,
				}
				self.update_file_core_odoo(cr, uid, vals)




		else:
			return True

	def update_file_core_odoo(self, cr, uid, vals, context={}):
		for from_file, to_file in vals.iteritems():
			self.__logger.info('start replace from: %s to : %s' % (from_file, to_file))
			f = open(from_file, 'r')
			file_str = f.read()
			with open(to_file, "w") as fn:
				fn.write(file_str)
			self.__logger.info('end replace.')
		return True


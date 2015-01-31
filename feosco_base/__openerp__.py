# -*- coding: utf-8 -*-
{
    'name': 'FEOSCO Base Module',
    'version': '1.1',
    'author': 'Feosco',
    'category': 'Feosco',
    'website': 'http://www.feosco.com',
    'description': """
        Feosco Base Module: This module contain all data, base function that used in feosco modules
    """,
    'author': 'Feosco',
    'website': 'http://www.openerp.com',
    'images': [
    ],
    'depends': ['base', 'fetchmail'],
    'data': [
		'security/ir.model.access.csv',
		'view/menu.xml',
		'view/master_data_view.xml',
		'view/res_partner_view.xml',
		'view/res_bank_view.xml',
		'view/res_company_view.xml',
		'view/city_view.xml',
		'view/district_view.xml',
		'view/res_users_view.xml',
		'view/ir_attachment_view.xml',
		'data/data.xml'
    ],
    'demo': [],
    'test': [
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'css': [],
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

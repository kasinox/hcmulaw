#-*- coding:utf-8 -*-
{
    'name': 'Remove all Odoo',
    'author': 'thanhchatvn@gmail.com',
    'description': """
    -  Module overide all function: \n
        Odoo	=>	Hcmulaw \n
        OpenERP  =>  Hcmulaw \n
        openerp.com => Hcmulaw.edu.vn \n
        oddo.com  => Hcmulaw.com \n
        sales@odoo.com and support@feosco.com  => sales@Hcmulaw.com and support@Hcmulaw.com \n
        ...etc \n
    """,
    'version': '1.0',
    'depends': [
        'web',
        'im_odoo_support',
    ],
    'auto_install': True,
    'data': [
        'views/main.xml',
        'model/update_logo_company.xml',
    ],
    'qweb' : [
        "static/src/xml/*.xml",
    ],
    'auto_install': True,
}
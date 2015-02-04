# -*- encoding: utf-8 -*-
{
    "name": "FEOS: Assets Management",
    "version": "1.0",
    "depends": [
        "account_asset",
        "feosco_qrcode",
        "feosco_base",
        "feosco_translate",
        "feosco_account_asset_category_vietnam",
        ],
    "author": "Feosco",
    "description": """Asset management.
    This Module manages the assets owned by a company or an individual. It will keep track of depreciation's occurred on
    those assets. And it allows to create Move's of the depreciation lines.
    """,
    "website": "http://www.feosco.com",
    "category": "Feosco",
    'images': [],
    "sequence": 32,
    "init_xml": [
    ],
    "demo_xml": [
    ],
    'test': [
    ],
    "data": [
        'security/security.xml',
        'security/ir.model.access.csv',
        'wizard_local/account_asset_print_all.xml',
        'wizard_local/feosco_wizard_asset_assign_view.xml',
        'wizard_local/export_import_view.xml',
        'wizard_local/print_selection_view.xml',
        'wizard_local/move_department.xml',
        'wizard_local/update_asset_price.xml',
        'datas/master_data.xml',
        'views/asset_main_menu.xml',
        'views/asset_view.xml',
        'views/asset_barcode_view.xml',
        'views/asset_report_view.xml',
        'views/asset_status.xml',
        'views/asset_print.xml',
        'views/asset_scan_view.xml',
        'views/asset_department.xml',
        'views/asset_scan_time.xml',
        'views/asset_gross_from.xml',
        'views/asset_purchase_year.xml',
        'views/asset_type.xml',
        'report/feosco_asset_report_view.xml',
        'report/qweb_report_by_department.xml',
        'ir/ir_attachment_view.xml',
    ],
    "auto_install": False,
    "installable": True,
    "application": False,
}



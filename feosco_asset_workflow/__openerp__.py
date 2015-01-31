# -*- encoding: utf-8 -*-
{
    "name": "FEOS: Workflow for Asset Management",
    "version": "1.0",
    "depends": ["feosco_account_asset"],
    "author": "Feosco",
    "description": """Workflow for Asset Management""",
    "website": "http://www.feosco.com",
    "category": "Feosco",
    "init_xml": [],
    "demo_xml": [],
    'test': [],
    "data": [
        'security/ir.model.access.csv',
        'view/asset_contract.xml',
        'view/asset_contract_line.xml',
        'view/asset_request.xml',
        'view/asset_request_line.xml',
        'view/asset_stock.xml',
        'view/asset_contract_role.xml',
        'view/main_menu.xml',
    ],
    "auto_install": False,
    "installable": True,
    "application": False,
}


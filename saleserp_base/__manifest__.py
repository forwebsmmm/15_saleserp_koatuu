# -*- coding: utf-8 -*-
# Copyright (C) 2016-TODAY SalesERP <https://saleserp.pro/>
# Part of SalesERP Base addon for Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'SalesERP Base',

    'summary': '''
Base for SalesERP
    ''',

    'description': '''
Add Menu, User Groups, etc. for SalesERP
    ''',

    'author': 'SalesERP',
    'website': 'https://saleserp.pro/',
    'category': 'SalesERP',
    'version': '0.1',

    'depends': [
        'base',
    ],

    'data': [
        'security/saleserp_base_groups.xml',
        'views/saleserp_base_views.xml',
    ],

    'installable': True,
    'application': False,
    'auto_install': False,
}

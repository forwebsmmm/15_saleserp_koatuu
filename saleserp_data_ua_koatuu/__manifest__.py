# -*- coding: utf-8 -*-
# Copyright (C) 2016-TODAY SalesERP <https://saleserp.pro/>
# Part of SalesERP KOATUU addon for Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'SalesERP KOATUU',

    'summary': '''
KOATUU Json Import
    ''',

    'description': '''
Import KOATUU Classifier from Json File
    ''',

    'author': 'SalesERP',
    'website': 'https://saleserp.pro/',
    'category': 'SalesERP',
    'version': '0.1',

    'depends': [
        'saleserp_base',
    ],

    'data': [
        'security/ir.model.access.csv',
        'views/koatuu_import_wizard_view.xml',
        'views/saleserp_cities_hierarchy.xml',
        # 'views/backend_assets.xml'
    ],

    'assets': {
        'web.assets_backend': {
            '/saleserp_data_ua_koatuu/static/src/js/upgrade_action_call.js'
        },

        'web.assets_qweb': {
            '/saleserp_data_ua_koatuu/static/src/xml/upload_button.xml'
        },
    },

    # 'qweb': [
    #     'static/src/xml/upload_button.xml',
    # ],

    'installable': True,
    'auto_install': False,
}

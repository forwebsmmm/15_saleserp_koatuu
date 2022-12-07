# -*- coding: utf-8 -*-
# Copyright (C) 2016-TODAY SalesERP <https://saleserp.pro/>
# Part of SalesERP KOATUU addon for Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api
from odoo.exceptions import UserError

import json
import base64


# import logging
# _logger = logging.getLogger(__name__)


class JsonImport(models.TransientModel):
    _name = 'saleserp.json.import'
    _description = 'KOATUU JSON Import'

    json_file = fields.Binary(
        'JSON File',
        required=True,
        help='Upload an JSON file.',
    )
    json_filename = fields.Char('Filename')
    line_ids = fields.One2many('saleserp.json.import.lines',
                               'saleserp_json_import_id',
                               'KOATUU JSON Import Lines')

    @api.onchange('json_file')
    def _onchange_json_file(self):
        if not self.json_file:
            return False

        lines = self.env['saleserp.json.import.lines']

        if '.json' in self.json_filename:
            data = json.loads(base64.b64decode(self.json_file).decode('utf-8'))
            for d in data:
                lines.create({
                    'saleserp_json_import_id': self.id,
                    'first_lvl': d['Перший рівень'],
                    'second_lvl': d['Другий рівень'],
                    'third_lvl': d['Третій рівень'],
                    'fourth_lvl': d['Четвертий рівень'],
                    'category': d['Категорія'],
                    'object_name': d["Назва об'єкта українською мовою"],
                })
        else:
            raise UserError('Wrong file extension.')

    def json_import_button(self):
        record_list = self.line_ids
        cities_hierarchy = self.env['saleserp.cities.hierarchy'].sudo()
        for r in record_list:
            parent_id = None
            code = r.first_lvl
            if r.fourth_lvl:
                parent_id = cities_hierarchy.search([('code', '=', r.third_lvl)]).id
                code = r.fourth_lvl
            elif r.third_lvl:
                parent_id = cities_hierarchy.search([('code', '=', r.second_lvl)]).id
                code = r.third_lvl
            elif r.second_lvl:
                parent_id = cities_hierarchy.search([('code', '=', r.first_lvl)]).id
                code = r.second_lvl
            cities = cities_hierarchy.search([('code', '=', code)])
            if cities:
                cities.write({
                    'name': r.object_name,
                    'parent_id': parent_id,
                    'category': r.category,
                    'state_code': r.first_lvl,
                    'second_lvl_ls': r.second_lvl[2:],
                    'second_lvl': r.second_lvl,
                    'third_lvl': r.third_lvl,
                    'fourth_lvl': r.fourth_lvl,
                })
            else:
                cities_hierarchy.create({
                    'code': code,
                    'name': r.object_name,
                    'parent_id': parent_id,
                    'category': r.category,
                    'state_code': r.first_lvl,
                    'second_lvl_ls': r.second_lvl[2:],
                    'second_lvl': r.second_lvl,
                    'third_lvl': r.third_lvl,
                    'fourth_lvl': r.fourth_lvl,
                })
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }


class JsonImportLines(models.TransientModel):
    _name = 'saleserp.json.import.lines'

    saleserp_json_import_id = fields.Many2one('saleserp.json.import', 'JSON Import', index=True)

    first_lvl = fields.Char('First Level')
    second_lvl = fields.Char('Second Level')
    third_lvl = fields.Char('Third Level')
    fourth_lvl = fields.Char('Fourth Level')
    category = fields.Char('Сategory')
    object_name = fields.Char('Object Name')

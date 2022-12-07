# -*- coding: utf-8 -*-
# Copyright (C) 2016-TODAY SalesERP <https://saleserp.pro/>
# Part of SalesERP KOATUU addon for Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class SaleserpCitiesHierarchy(models.Model):
    _name = 'saleserp.cities.hierarchy'
    _description = 'Saleserp Cities Hierarchy'
    _order = 'complete_name'
    _rec_name = 'complete_name'

    name = fields.Char('Name', required=True)
    complete_name = fields.Char('Complete Name', compute='_compute_complete_name', store=True, recursive=True)
    parent_id = fields.Many2one('saleserp.cities.hierarchy', string='Parent Name', index=True)
    child_ids = fields.One2many('saleserp.cities.hierarchy', 'parent_id', string='Child Name')
    code = fields.Char('Code', required=True, index=True)
    category = fields.Char('Category')
    state_code = fields.Char('State Code')
    second_lvl_ls = fields.Char('Second Lvl Last Symbols')
    second_lvl = fields.Char('Second Lvl')
    third_lvl = fields.Char('Third Lvl')
    fourth_lvl = fields.Char('Fourth Lvl')

    def name_get(self):
        if not self.env.context.get('hierarchical_naming', True):
            return [(record.id, record.name) for record in self]
        return super(SaleserpCitiesHierarchy, self).name_get()

    @api.model
    def name_create(self, name):
        return self.create({'name': name}).name_get()[0]

    @api.depends('name', 'parent_id.complete_name')
    def _compute_complete_name(self):
        for record in self:
            if record.parent_id:
                record.complete_name = '%s / %s' % (record.parent_id.complete_name, record.name)
            else:
                record.complete_name = record.name

    @api.constrains('parent_id')
    def _check_parent_id(self):
        if not self._check_recursion():
            raise ValidationError(_('You cannot create recursive cities.'))
